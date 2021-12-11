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

CLOSERS = {"{": "}", "[": "]", "<": ">", "(": ")"}
OPENERS = {"{", "[", "<", "("}
POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    tic = perf_counter()

    invalid_characters = []
    for line in lines:
        need = [None]
        for char in line:
            if char in OPENERS:
                need.append(CLOSERS[char])
            elif char == need[-1]:
                need.pop(-1)
            else:
                invalid_characters.append(char)
                break

    score = 0
    for char in invalid_characters:
        score += POINTS[char]

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{score=} ({time_us}µs)")
