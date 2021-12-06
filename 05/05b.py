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

        vector = [0,0]
        for i in [0,1]:
            if start[i] < end[i]:
                vector[i] = 1
            elif start[i] > end[i]:
                vector[i] = -1


        current = list(start)
        # count the starting point, then traverse the line and count each point
        coords[tuple(current)] += 1
        while True:
            current[0] += vector[0]
            current[1] += vector[1]
            coords[tuple(current)] += 1
            if tuple(current) == end:
                break

    num_points = sum(1 if count >= 2 else 0 for count in coords.values())
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_points=} ({time_us}µs)")
