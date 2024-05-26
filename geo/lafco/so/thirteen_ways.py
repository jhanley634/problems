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


if __name__ == "__main__":
    tip03_use_sets()
