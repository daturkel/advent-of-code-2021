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
        current_fish = [int(number) for number in file.read().split(",")]

    tic = perf_counter()
    new_fish = []
    for i in range(80):
        for fish in current_fish:
            if fish == 0:
                new_fish += [6, 8]
            else:
                new_fish.append(fish - 1)

        current_fish = new_fish
        new_fish = []

    num_fish = len(current_fish)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_fish=} ({time_us}µs)")
