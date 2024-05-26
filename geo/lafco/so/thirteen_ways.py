#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# see https://codereview.stackexchange.com/questions/291896/performance-tuning-project-euler-566-cake-icing-puzzle
# which cites https://medium.com/@nirmalya.ghosh/13-ways-to-speedup-python-loops-e3ee56cd6b73
# and https://colab.research.google.com/drive/1fPJv4zt_zQIBX1okJ0-IGW0JRxpj9yI
from itertools import filterfalse
import functools
import random
import timeit

from faker import Faker
import numpy as np

num_runs = 10
num_loops = 100000
num_loops_default = 100000

num_ns_per_sec = 100000000  # Nanoseconds per second

# List of numbers, used for various tests
num100 = np.arange(100, 201).tolist()
num500 = np.arange(100, 601).tolist()
num1K = np.arange(1, 1001).tolist()
num10K = np.arange(1, 10001).tolist()
num50K = np.arange(1, 50001).tolist()


# Helper functions
def calculate_and_display_test_run_numbers(result_ns, num_loops_used_for_tests):
    test_avg = sum(result_ns) / num_runs
    # test_95p = np.percentile(result_ns, 95)
    print(
        f"{num_runs} runs. Numbers below are calculated per run, each with {num_loops_used_for_tests} loops"
    )
    print("{:>7} {:>12.0f} nanoseconds".format("Minimum", min(result_ns)))
    print("{:>7} {:>12.0f} nanoseconds".format("Maximum", max(result_ns)))
    print(
        "{:>7} {:>12.0f} nanoseconds ({:.3f} per loop)".format(
            "Average", test_avg, test_avg / num_loops_used_for_tests
        )
    )
    # print("- 95 percentile {:>12.0f} nanoseconds".format(test_95p))
    return test_avg


def compare_test_0_with_test_1(test_0_avg, test_1_avg, num_loops_used_for_tests):
    # Helper function used to compare Test 0 with Test 1
    # Assumption: test_0_avg and test_1_avg are expressed in nanoseconds
    baseline_avg_per_loop = test_0_avg / num_loops_used_for_tests
    improved_avg_per_loop = test_1_avg / num_loops_used_for_tests
    improvement_avg = baseline_avg_per_loop - improved_avg_per_loop
    improvement_avg_pct = (improvement_avg / baseline_avg_per_loop) * 100
    # Calculate the speedup
    speedup = baseline_avg_per_loop / improved_avg_per_loop

    # Format V1
    # # print("{:>44} : {}".format("Number of loops used for these tests", num_loops_used_for_tests))
    # print("{:>44} : {:.3f} nanoseconds".format("Baseline measured on average (per loop)", baseline_avg_per_loop))
    # print("{:>44} : {:.3f} nanoseconds".format("Improved measured on average (per loop)", improved_avg_per_loop))
    # print("{:>44} : {:.1f} %".format("% Improvement measured on average (per loop)", improvement_avg_pct))
    # print("{:>44} : {:.2f}x".format("Speedup", speedup))

    # Format V2 (compact)
    print("{:>13}: {:.3f} ns per loop".format("Baseline", baseline_avg_per_loop))
    print("{:>13}: {:.3f} ns per loop".format("Improved", improved_avg_per_loop))
    print("{:>13}: {:.1f} %".format("% Improvement", improvement_avg_pct))
    print("{:>13}: {:.2f}x".format("Speedup", speedup))


def generate_fake_names(count: int = 10000):
    fake = Faker()
    output_list = []
    for _ in range(count):
        output_list.append(fake.name())
    return output_list


fake_names = generate_fake_names(count=9995)


## #3. Use sets for scenarios you'd otherwise use for loops for comparisons

cs_majors = ["John", "Jack", "Jerry", "Mary", "Richard"]
ee_majors = ["Mary", "Sriram", "Ahmed", "Peter", "Nick"]
cs_majors.extend(fake_names)
random.shuffle(cs_majors)
ee_majors.extend(fake_names)
random.shuffle(ee_majors)


def test_03_v0(list_1, list_2):
    # Baseline version (Inefficient way)
    # (nested lookups using for loop)
    def _test_03_v0():
        common_items = []
        for item in list_1:
            if item in list_2:
                common_items.append(item)
        return common_items

    return _test_03_v0


def test_03_v1(list_1, list_2):
    # Improved version
    # (use sets to replace the nested lookups)
    def _test_03_v1():
        set_1 = set(list_1)
        set_2 = set(list_2)
        common_items = set_1.intersection(set_2)
        return common_items

    return _test_03_v1


def tip03_use_sets():
    # Run the test 0 (nested lookups using for loop)

    t = timeit.Timer(test_03_v0(list_1=cs_majors, list_2=ee_majors))
    result_0 = t.repeat(repeat=num_runs, number=num_runs)
    result_0_np = np.array(result_0) * num_ns_per_sec
    result_0_ns = result_0_np.tolist()  # Convert back to list
    test_0_avg = calculate_and_display_test_run_numbers(
        result_ns=result_0_ns, num_loops_used_for_tests=num_loops
    )

    t = timeit.Timer(test_03_v1(list_1=cs_majors, list_2=ee_majors))
    result_1 = t.repeat(repeat=num_runs, number=num_runs)
    result_1_np = np.array(result_1) * num_ns_per_sec
    result_1_ns = result_1_np.tolist()  # Convert back to list
    test_1_avg = calculate_and_display_test_run_numbers(
        result_ns=result_1_ns, num_loops_used_for_tests=num_loops
    )

    # Compare Test 0 with Test 1
    compare_test_0_with_test_1(
        test_0_avg, test_1_avg, num_loops_used_for_tests=num_loops
    )


## #10. Use Memoization


def fibonacci(n):
    if n == 0 or n == 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@functools.lru_cache()
def fibonacci_v2(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_v2(n - 1) + fibonacci_v2(n - 2)


def test_10_v0(numbers):
    # Baseline version (Inefficient way)
    def _test_10_v0():
        output = []
        for i in numbers:
            output.append(fibonacci(i))

        return output

    return _test_10_v0


def test_10_v1(numbers):
    # Improved version
    # (Using functools' lru_cache function)
    def _test_10_v1():
        output = []
        for i in numbers:
            output.append(fibonacci_v2(i))

        return output

    return _test_10_v1


def tip10_memoize():

    num_loops = 1500  # Reduce this from the usual 100K loops, since the tests (for this tip) take too long

    # Run the test 0 (inefficient version)

    t = timeit.Timer(test_10_v0(numbers=range(10)))
    result_0 = t.repeat(repeat=num_runs, number=num_runs)
    result_0_np = np.array(result_0) * num_ns_per_sec
    result_0_ns = result_0_np.tolist()  # Convert back to list
    test_0_avg = calculate_and_display_test_run_numbers(
        result_ns=result_0_ns, num_loops_used_for_tests=num_loops
    )

    # Run the test 1 (efficient version)
    # Using functools' lru_cache function

    t = timeit.Timer(test_10_v1(numbers=range(10)))
    result_1 = t.repeat(repeat=num_runs, number=num_runs)
    result_1_np = np.array(result_1) * num_ns_per_sec
    result_1_ns = result_1_np.tolist()  # Convert back to list
    test_1_avg = calculate_and_display_test_run_numbers(
        result_ns=result_1_ns, num_loops_used_for_tests=num_loops
    )

    # Compare Test 0 with Test 1
    compare_test_0_with_test_1(
        test_0_avg, test_1_avg, num_loops_used_for_tests=num_loops
    )


# Reset it back to the usual 100K loops - it was reduced since the tests (for this tip) take too long
num_loops = num_loops_default

## 12. Avoid Creating Intermediate Lists
# not much speedup, but less memory


def test_12_v0(numbers):
    # Baseline version (Inefficient way)
    def _test_12_v0():
        filtered_data = []
        for i in numbers:
            filtered_data.extend(list(filter(lambda x: x % 5 == 0, range(1, i**2))))

        return filtered_data

    return _test_12_v0


def test_12_v1(numbers):
    # Improved version
    # (using filterfalse)
    def _test_12_v1():
        filtered_data = []
        for i in numbers:
            filtered_data.extend(
                list(filterfalse(lambda x: x % 5 != 0, range(1, i**2)))
            )
        return filtered_data

    return _test_12_v1


def test_12_v2(numbers):
    # Trial version
    def _test_12_v1():
        filtered_data = []
        for i in [x for x in numbers if x % 5 == 0]:
            filtered_data.append(i)

        return filtered_data

    return _test_12_v1


def tip12_filterfalse_no_intermediate_lists():

    # Reduce this from the usual 100K loops, since the tests (for this tip) take too long
    num_loops = 1000

    # Run the test 0 (inefficient version)

    t = timeit.Timer(
        test_12_v0(numbers=num100)
    )  # NOTE: takes a long time when try with 500, 1K, ...
    result_0 = t.repeat(repeat=num_runs, number=num_runs)
    result_0_np = np.array(result_0) * num_ns_per_sec
    result_0_ns = result_0_np.tolist()  # Convert back to list
    test_0_avg = calculate_and_display_test_run_numbers(
        result_ns=result_0_ns, num_loops_used_for_tests=num_loops
    )

    # Run the test 1 (efficient version)

    t = timeit.Timer(test_12_v1(numbers=num100))
    result_1 = t.repeat(repeat=num_runs, number=num_runs)
    result_1_np = np.array(result_1) * num_ns_per_sec
    result_1_ns = result_1_np.tolist()  # Convert back to list
    test_1_avg = calculate_and_display_test_run_numbers(
        result_ns=result_1_ns, num_loops_used_for_tests=num_loops
    )

    # Compare Test 0 with Test 1
    compare_test_0_with_test_1(
        test_0_avg, test_1_avg, num_loops_used_for_tests=num_loops
    )


## #9. Use Python's built-in map() function


def some_function_performing_some_logic(x):
    # This would normally be a function containing application logic which
    # required it to be made into a separate function (for test, return square)
    return x**2


def test_09_v0(numbers):
    # Baseline version (Inefficient way)
    def _test_09_v0():
        output = []
        for i in numbers:
            output.append(some_function_performing_some_logic(i))

        return output

    return _test_09_v0


def test_09_v1(numbers):
    # Improved version
    # (Using Python's built-in map() function)
    def _test_09_v1():
        output = map(some_function_performing_some_logic, numbers)
        return list(output)

    return _test_09_v1


def tip9_map():
    # Run the test 0 (inefficient version)

    t = timeit.Timer(test_09_v0(numbers=num1K))
    result_0 = t.repeat(repeat=num_runs, number=num_runs)
    result_0_np = np.array(result_0) * num_ns_per_sec
    result_0_ns = result_0_np.tolist()  # Convert back to list
    test_0_avg = calculate_and_display_test_run_numbers(
        result_ns=result_0_ns, num_loops_used_for_tests=num_loops
    )

    # Run the test 1 (efficient version)
    # Using Python's built-in map() function

    t = timeit.Timer(test_09_v1(numbers=num1K))
    result_1 = t.repeat(repeat=num_runs, number=num_runs)
    result_1_np = np.array(result_1) * num_ns_per_sec
    result_1_ns = result_1_np.tolist()  # Convert back to list
    test_1_avg = calculate_and_display_test_run_numbers(
        result_ns=result_1_ns, num_loops_used_for_tests=num_loops
    )

    # Compare Test 0 with Test 1
    compare_test_0_with_test_1(
        test_0_avg, test_1_avg, num_loops_used_for_tests=num_loops
    )


num_loops = num_loops_default  # Reset it back to the usual 100K loops - it was reduce since the tests (for this tip) take too long

if __name__ == "__main__":
    # tip03_use_sets()
    # tip10_memoize()
    # tip12_filterfalse_no_intermediate_lists()
    tip9_map()
