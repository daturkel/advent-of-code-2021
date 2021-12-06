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
        raw_lines = file.read().splitlines()

    tic = perf_counter()
    lines = []
    for line in raw_lines:
        numbers = [int(number) for number in line.replace(" -> ", ",").split(",")]
        lines.append((tuple(numbers[:2]), tuple(numbers[2:])))

    coords = defaultdict(int)

    for line in lines:
        start, end = line

        # are we traveling horizontally or vertically
        if start[0] == end[0]:
            idx = 1
        elif start[1] == end[1]:
            idx = 0
        else:
            continue

        # are we moving forward or backward
        if start[idx] <= end[idx]:
            delta = 1
        else:
            delta = -1

        current = list(start)
        # count the starting point, then traverse the line and count each point
        coords[tuple(current)] += 1
        while True:
            current[idx] += delta
            coords[tuple(current)] += 1
            if tuple(current) == end:
                break

    num_points = sum(1 if count >= 2 else 0 for count in coords.values())
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_points=} ({time_us}µs)")
