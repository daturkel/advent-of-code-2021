#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        positions = [int(number) for number in file.read().split(",")]

    tic = perf_counter()
    if len(positions) % 2 == 0:
        idx_half = int(len(positions) / 2)
        middle_two = sorted(positions)[idx_half - 1 : idx_half + 1]
        median = sum(middle_two) / 2
    else:
        idx = (len(positions) - 1) / 2
        median = sorted(positions)[idx]

    median = int(median)
    fuel = sum(abs(position - median) for position in positions)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{fuel=} ({time_us}µs)")
