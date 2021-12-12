#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

from itertools import product
import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    neighbors = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if (i == 0) and (j == 0):
                continue
            elif (0 <= x + i < 10) and (0 <= y + j < 10):
                neighbors.append((x + i, y + j))

    return neighbors


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        array = [[int(char) for char in line] for line in file.read().splitlines()]

    tic = perf_counter()
    num_flashes = 0
    for step in range(100):
        flashes = []
        for x, y in product(range(10), range(10)):
            array[y][x] += 1
            if array[y][x] > 9:
                flashes.append((x, y))
                num_flashes += 1
                array[y][x] = 0
        while flashes:
            x, y = flashes.pop(0)
            for n_x, n_y in get_neighbors(x, y):
                if array[n_y][n_x] != 0:
                    array[n_y][n_x] += 1
                    if array[n_y][n_x] > 9:
                        flashes.append((n_x, n_y))
                        num_flashes += 1
                        array[n_y][n_x] = 0

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_flashes=} ({time_us}µs)")
