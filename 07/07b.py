#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

import logging
from math import ceil, floor
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def calc_fuel(distance: int, cache: dict = {}):
    fuel = (distance ** 2 + distance) / 2
    return int(fuel)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        positions = [int(number) for number in file.read().split(",")]

    tic = perf_counter()
    avg = sum(positions) / len(positions)

    fuel_a = sum(calc_fuel(abs(position - floor(avg))) for position in positions)
    fuel_b = sum(calc_fuel(abs(position - ceil(avg))) for position in positions)
    fuel = int(min(fuel_a, fuel_b))
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{fuel=} ({time_us}µs)")
