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


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        string_list = file.read().splitlines()

    tic = perf_counter()
    digit_array = []
    for string in string_list:
        digit_array.append([int(char) for char in string])

    # Find most common digits by taking average of each column and rounding to nearest digit
    means = np.mean(digit_array, axis=0)
    digits = list((means >= 0.5).astype(int))

    # Bitwise NOT by subtracting one and taking absolute value
    complement = [abs(digit - 1) for digit in digits]

    digits_int = int("".join(str(digit) for digit in digits), 2)
    complement_int = int("".join(str(digit) for digit in complement), 2)

    product = digits_int * complement_int
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{product=} ({time_us}µs)")
