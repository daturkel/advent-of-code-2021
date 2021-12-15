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


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    tic = perf_counter()
    template = lines[0]
    rules = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert + pair[1]

    current_polymer = template
    next_polymer = []
    for _ in range(10):
        next_polymer.append(current_polymer[0])
        for i in range(len(current_polymer) - 1):
            pair = current_polymer[i : i + 2]
            next_polymer.append(rules[pair])
        current_polymer = "".join(next_polymer)
        next_polymer = []

    char_counts = defaultdict(int)
    for char in current_polymer:
        char_counts[char] += 1

    most_minus_least = max(char_counts.values()) - min(char_counts.values())

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{most_minus_least=} ({time_us}µs)")
