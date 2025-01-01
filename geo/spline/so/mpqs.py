#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/294893/optimizing-sieving-code-for-the-multiple-polynomial-quadratic-sieve

from math import ceil, exp, isqrt, log, log2, sqrt
import logging
import time

from numpy.typing import NDArray
from sympy import nextprime
import numpy as np

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


_known_primes = [2, 3]


def init_known_primes(limit: int = 1000) -> None:
    global _known_primes
    _known_primes += [x for x in range(5, limit, 2) if is_prime(x)]
    logger.info(
        "Initialized _known_primes up to %d. Total known primes: %d",
        limit,
        len(_known_primes),
    )


def _try_composite(a: int, d: int, n: int, s: int) -> bool:
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n - 1:
            return False
    return True


def is_prime(n: int, _precision_for_huge_n: int = 16) -> bool:
    if n in _known_primes:
        return True
    if any((n % p) == 0 for p in _known_primes) or n in (0, 1):
        return n in _known_primes

    d, s = n - 1, 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))

    return not any(
        _try_composite(a, d, n, s) for a in _known_primes[:_precision_for_huge_n]
    )


class QuadraticSieve:
    def __init__(self, M: int = 200000, B: int = 10000, T: int = 1):
        self.logger = logging.getLogger(__name__)
        self.prime_log_map: dict[int, int] = {}
        self.root_map: dict[int, int] = {}

        # Store hyperparameters
        self.M = M
        self.B = B
        self.T = T

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Compute GCD of two integers using Euclid's Algorithm."""
        a, b = abs(a), abs(b)
        while a:
            a, b = b % a, a
        return b

    @staticmethod
    def legendre(n: int, p: int) -> int:
        """Compute the Legendre symbol (n/p)."""
        val = pow(n, (p - 1) // 2, p)
        return val - p if val > 1 else val

    @staticmethod
    def jacobi(a: int, m: int) -> int:
        """Compute the Jacobi symbol (a/m)."""
        a = a % m
        t = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if m % 8 in [3, 5]:
                    t = -t
            a, m = m, a
            if a % 4 == 3 and m % 4 == 3:
                t = -t
            a %= m
        return t if m == 1 else 0

    @staticmethod
    def modinv(n: int, p: int) -> int:
        return pow(n, -1, p)

    @staticmethod
    def hensel(r: int, p: int, n: int) -> float:
        x = (n - r * r) / p  # f(b) = b ^ 2 - n
        z = QuadraticSieve.modinv(2 * r, p) % p  # f'(b) = 2b
        y = (-x * z) % p
        return r + y * p

    def factorise_fast(
        self, value: int, factor_base: list[int]
    ) -> tuple[list[int], int]:
        """Factor a number over the given factor base."""
        factors = []
        if value < 0:
            factors.append(-1)
            value = -value
        for factor in factor_base[1:]:
            while value % factor == 0:
                factors.append(factor)
                value //= factor
        return sorted(factors), value

    @staticmethod
    def tonelli_shanks(a: int, p: int) -> tuple[int, int]:
        """Solve x^2 ≡ a (mod p) for x using the Tonelli-Shanks algorithm."""
        a %= p
        if p % 8 in [3, 7]:
            x = pow(a, (p + 1) // 4, p)
            return x, p - x

        if p % 8 == 5:
            x = pow(a, (p + 3) // 8, p)
            if pow(x, 2, p) != a % p:
                x = (x * pow(2, (p - 1) // 4, p)) % p
            return x, p - x

        d = 2
        symb = 0
        while symb != -1:
            symb = QuadraticSieve.jacobi(d, p)
            d += 1
        d -= 1

        n = p - 1
        s = 0
        while n % 2 == 0:
            n //= 2
            s += 1
        t = n

        A = pow(a, t, p)
        D = pow(d, t, p)
        m = 0
        for i in range(s):
            i1 = pow(2, s - 1 - i)
            i2 = (A * pow(D, m, p)) % p
            i3 = pow(i2, i1, p)
            if i3 == p - 1:
                m += pow(2, i)
        x = (pow(a, (t + 1) // 2, p) * pow(D, m // 2, p)) % p
        return x, p - x

    @staticmethod
    def gauss_elim(x: NDArray[np.int64]) -> tuple[NDArray[np.int64], list[int]]:
        """Perform Gaussian elimination on a binary matrix over GF(2)"""
        x = x.astype(bool, copy=False)
        n, m = x.shape
        marks = []

        for i in range(n):
            row = x[i]
            ones = np.flatnonzero(row)
            if ones.size == 0:
                continue

            pivot = ones[0]
            marks.append(pivot)

            mask = x[:, pivot].copy()
            mask[i] = False

            x[mask] ^= row

        return x.astype(np.int8, copy=False), sorted(marks)

    @staticmethod
    def find_null_space_GF2(
        reduced_matrix: NDArray[np.int64], pivot_rows: list[int]
    ) -> NDArray[np.int8]:
        """Find null space vectors of the reduced binary matrix over GF(2)"""
        n, m = reduced_matrix.shape
        nulls = []
        free_rows = [row for row in range(n) if row not in pivot_rows]
        k = 0
        for row in free_rows:
            ones = np.where(reduced_matrix[row] == 1)[0]
            null = np.zeros(n)
            null[row] = 1

            mask = np.isin(np.arange(n), pivot_rows)
            relevant_cols = reduced_matrix[:, ones]
            matching_rows = np.any(relevant_cols == 1, axis=1)
            null[mask & matching_rows] = 1

            nulls.append(null)
            k += 1
            if k == 4:  # no need to find entire null space, just a few values will do
                break

        return np.asarray(nulls, dtype=np.int8)

    @staticmethod
    def prime_sieve(n: int) -> list[int]:
        """Return list of primes up to n using Sieve of Eratosthenes."""
        sieve_array = np.ones((n + 1,), dtype=bool)
        sieve_array[0], sieve_array[1] = False, False
        for i in range(2, int(n**0.5) + 1):
            if sieve_array[i]:
                sieve_array[i * 2 :: i] = False
        ret = np.where(sieve_array)[0].tolist()
        assert isinstance(ret, list)
        assert all(isinstance(x, int) for x in ret)
        return ret

    def find_b(self, N: int) -> int:
        """Determine the factor base bound B"""
        x = ceil(exp(sqrt(0.5 * log(N) * log(log(N))))) + 1
        return x

    def get_smooth_b(self, N: int, B: int) -> list[int]:
        """Build the factor base of primes p ≤ B where (N/p) = 1."""
        primes = self.prime_sieve(B)
        factor_base = [-1, 2]
        self.prime_log_map[2] = 1
        for p in primes[1:]:
            if self.legendre(N, p) == 1:
                factor_base.append(p)
                self.prime_log_map[p] = round(log2(p))
                self.root_map[p] = self.tonelli_shanks(N, p)
        return factor_base

    def decide_bound(self, N: int, B=None) -> int:
        """Decide on bound B using heuristic if none provided."""
        if B is None:
            B = self.find_b(N)
        self.logger.info("Using B = %d", B)
        return B

    def build_factor_base(self, N, B):
        """Build factor base for Quadratic Sieve."""
        fb = self.get_smooth_b(N, B)
        self.logger.info("Factor base size: %d", len(fb))
        return fb

    def sieve_interval(self, N, a, b, c, factor_base, M):
        sieve_values = [0] * (2 * M + 1)
        for p in factor_base:
            if p < 20:
                continue
            ainv = self.modinv(a, p)

            r1, r2 = self.root_map[p]
            r1 = int((ainv * (r1 - b)) % p)
            r2 = int((ainv * (r2 - b)) % p)
            r1 = (r1 + M) % p
            r2 = (r2 + M) % p

            for r in [r1, r2]:
                for i in range(r, 2 * M + 1, p):
                    sieve_values[i] += self.prime_log_map[p]

        return sieve_values

    def sieve(self, N, B, factor_base, M, partial=True):

        fb_len = len(factor_base)
        zero_row = [0] * fb_len
        error = 30

        # large prime stuff
        large_prime_bound = B * 128
        partials = {}
        lp_found = 0
        num_relations = 0

        target_relations = fb_len + self.T
        d = int(sqrt(sqrt(2 * N) / M))
        interval = 2 * M

        threshold = int(log2(M * sqrt(N)) - error)
        num_poly = 0
        matrix = []
        relations = []
        roots = []
        while len(relations) < target_relations:
            print(str(round(len(relations) / target_relations * 100, 2)) + "% done")
            num_poly += 1
            d = nextprime(d)
            while self.legendre(N, d) != 1:
                d = nextprime(d)
            a = d * d
            b = self.tonelli_shanks(N, d)[0]
            b = (b + (N - b * b) * QuadraticSieve.modinv(b + b, d)) % a
            c = (b * b - N) // a

            sieve_values = self.sieve_interval(N, a, b, c, factor_base, M)
            i = 0 - 1
            x = -M - 1
            while i < interval:
                i += 1
                x += 1
                val = sieve_values[i]
                if val > threshold:
                    relation = a * x + b
                    mark = False
                    poly_val = int(a * x * x + 2 * b * x + c)
                    local_factors, value = self.factorise_fast(poly_val, factor_base)

                    if not partial and value != 1:
                        continue

                    if partial and value != 1 and value < large_prime_bound:
                        if value not in partials:
                            partials[value] = (relation, local_factors, poly_val * a)
                            continue
                        else:
                            lp_found += 1
                            relation = relation * partials[value][0]
                            local_factors += partials[value][1]
                            poly_val = poly_val * partials[value][2]
                            mark = True
                    elif partial and value != 1:
                        continue

                    row = zero_row.copy()
                    counts = {}
                    for fac in local_factors:
                        counts[fac] = counts.get(fac, 0) + 1

                    for idx, prime in enumerate(factor_base):
                        row[idx] = counts.get(prime, 0) % 2

                    matrix.append(row)
                    relations.append(relation)
                    roots.append(poly_val * a)

        return matrix, relations, roots

    def solve_dependencies(self, matrix):
        """Solve for dependencies in GF(2)."""
        self.logger.info("Solving linear system in GF(2).")
        matrix = np.array(matrix).T
        reduced_matrix, marks = self.gauss_elim(matrix)
        null_basis = self.find_null_space_GF2(reduced_matrix.T, marks)
        return null_basis

    def extract_factors(self, N, relations, roots, dep_vectors):
        """Extract factors using dependency vectors."""
        for r in dep_vectors:
            prod_left = 1
            prod_right = 1
            for idx, bit in enumerate(r):
                if bit == 1:
                    prod_left *= relations[idx]
                    prod_right *= roots[idx]

            sqrt_right = isqrt(prod_right)
            prod_left = prod_left % N
            sqrt_right = sqrt_right % N
            factor_candidate = self.gcd(N, prod_left - sqrt_right)

            if factor_candidate not in (1, N):
                other_factor = N // factor_candidate
                self.logger.info(
                    "Found factors: %d, %d", factor_candidate, other_factor
                )
                return factor_candidate, other_factor

        return 0, 0

    def factor(self, N, B=None):
        """Main factorization method using the Quadratic Sieve algorithm."""
        overall_start = time.time()
        self.logger.info("========== Quadratic Sieve V4 Start ==========")
        self.logger.info("Factoring N = %d", N)

        # Step 1: Decide Bound
        step_start = time.time()
        B = self.decide_bound(N, self.B)
        step_end = time.time()
        self.logger.info(
            "Step 1 (Decide Bound) took %.3f seconds", step_end - step_start
        )

        # Step 2: Build Factor Base
        step_start = time.time()
        factor_base = self.build_factor_base(N, B)
        step_end = time.time()
        self.logger.info(
            "Step 2 (Build Factor Base) took %.3f seconds", step_end - step_start
        )

        # Step 3: Sieve Phase

        step_start = time.time()
        matrix, relations, roots = self.sieve(N, B, factor_base, self.M)
        step_end = time.time()
        self.logger.info(
            "Step 3 (Sieve Interval) took %.3f seconds", step_end - step_start
        )

        if len(matrix) < len(factor_base) + 1:
            self.logger.warning(
                "Not enough smooth relations found. Try increasing the sieve interval."
            )
            return 0, 0

        # Step 4: Solve for Dependencies
        step_start = time.time()
        dep_vectors = self.solve_dependencies(matrix)
        step_end = time.time()
        self.logger.info(
            "Step 5 (Solve Dependencies) took %.3f seconds", step_end - step_start
        )

        # Step 5: Extract Factors
        step_start = time.time()
        f1, f2 = self.extract_factors(N, relations, roots, dep_vectors)
        step_end = time.time()
        self.logger.info(
            "Step 6 (Extract Factors) took %.3f seconds", step_end - step_start
        )

        if f1 and f2:
            self.logger.info("Quadratic Sieve successful: %d * %d = %d", f1, f2, N)
        else:
            self.logger.warning(
                "No non-trivial factors found with the current settings."
            )

        overall_end = time.time()
        self.logger.info(
            "Total time for Quadratic Sieve: %.3f seconds", overall_end - overall_start
        )
        self.logger.info("========== Quadratic Sieve End ==========")

        return f1, f2


if __name__ == "__main__":
    N = 97245170828229363259 * 49966345331749027373
    qs = QuadraticSieve(B=11812, M=59060, T=1)

    factor1, factor2 = qs.factor(N)

    if factor1 and factor2:
        print(f"Factors of N: {factor1} * {factor2} = {N}")
    else:
        print("Failed to factorize N with the current settings.")
