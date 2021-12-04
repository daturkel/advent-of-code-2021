#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

import logging
import sys
from time import perf_counter

import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def most_common_in_column(digit_array: list[list[int]], column: int) -> int:
    """Given an array represented as a list of lists, get the most common binary digit in
    the `column`th column.
    """
    digit_array = np.array(digit_array)
    mean = np.mean(digit_array[:, column])
    if mean >= 0.5:
        most_common = 1
    else:
        most_common = 0
    return most_common


def filter_inputs(digit_array: list[list[int]], most_common: bool = True) -> list[int]:
    """Given an array represented as a list of lists, find the valid input by progressively
    filtering by bit criterion. Moving left to right, find the most common digit of the
    remaining valid inputs and filter out all that do not share that digit in that column.
    """
    valid_inputs = [row for row in digit_array]
    for i in range(len(digit_array[0])):
        bit_criterion = most_common_in_column(valid_inputs, i)
        if not most_common:
            # invert 0/1 by subtracting 1 and taking absolute value
            bit_criterion = abs(bit_criterion - 1)
        valid_inputs = [row for row in valid_inputs if row[i] == bit_criterion]
        if len(valid_inputs) == 1:
            break

    return valid_inputs[0]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        string_list = file.read().splitlines()

    tic = perf_counter()

    # Convert string inputs into array of binary digits
    digit_array = []
    for string in string_list:
        digit_array.append([int(char) for char in string])
    digit_array = np.array(digit_array)

    o2_rating_bin = filter_inputs(digit_array)
    co2_rating_bin = filter_inputs(digit_array, False)

    o2_rating = int("".join(str(digit) for digit in o2_rating_bin), 2)
    co2_rating = int("".join(str(digit) for digit in co2_rating_bin), 2)

    life_support_rating = o2_rating * co2_rating

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{life_support_rating=} ({time_us}µs)")
