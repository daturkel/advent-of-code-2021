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
        starting_fish = [int(number) for number in file.read().split(",")]

    tic = perf_counter()
    num_fish = len(starting_fish)

    def reproduce(days_left: int, cache: dict = {}) -> int:
        if days_left in cache.keys():
            return cache[days_left]

        days_left_now = days_left
        num_new_fish = 0
        new_fish_days_left = []
        while days_left_now > 0:
            if days_left_now - 9 > 0:
                new_fish_days_left.append(days_left_now - 9)
            num_new_fish += 1
            days_left_now -= 7

        for days_left_this_fish in new_fish_days_left:
            num_new_fish += reproduce(days_left_this_fish)

        cache[days_left] = num_new_fish

        return num_new_fish

    for fish in starting_fish:
        num_fish += reproduce(256 - fish)

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_fish=} ({time_us}µs)")
