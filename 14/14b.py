#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

from collections import defaultdict
import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def add_dicts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    keys = set(a.keys()).union(b.keys())
    new_dict = {}
    for key in keys:
        new_dict[key] = a.get(key, 0) + b.get(key, 0)

    return new_dict


def count_chars(pair: str, steps_left: int, cache: dict = {}) -> list[tuple]:
    if steps_left == 0:
        return {pair[1]: 1}
    elif (pair, steps_left) in cache:
        return cache[(pair, steps_left)]

    left, right = RULES[pair]
    left_counts = count_chars(left, steps_left - 1)
    right_counts = count_chars(right, steps_left - 1)

    counts = add_dicts(left_counts, right_counts)

    cache[pair, steps_left] = counts

    return counts


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    tic = perf_counter()
    template = lines[0]
    RULES = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        RULES[pair] = (pair[0] + insert, insert + pair[1])

    counts = {template[0]: 1}
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        pair_counts = count_chars(pair, 40)
        counts = add_dicts(counts, pair_counts)

    most_minus_least = max(counts.values()) - min(counts.values())

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{most_minus_least=} ({time_us}µs)")
