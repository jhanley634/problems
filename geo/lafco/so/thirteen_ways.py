#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# see https://codereview.stackexchange.com/questions/291896/performance-tuning-project-euler-566-cake-icing-puzzle
# which cites https://medium.com/@nirmalya.ghosh/13-ways-to-speedup-python-loops-e3ee56cd6b73
# and https://colab.research.google.com/drive/1fPJv4zt_zQIBX1okJ0-IGW0JRxpj9yI
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

if __name__ == "__main__":
    ...
