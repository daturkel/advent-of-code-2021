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


def get_neighbors(array: list[list[int]], x: int, y: int) -> list[tuple[int, int]]:
    width = len(array[0])
    height = len(array)

    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (0 <= x + dx < width) and (0 <= y + dy < height):
            neighbors.append((x + dx, y + dy))

    return neighbors


def is_low_point(array: list[list[int]], x: int, y: int) -> bool:
    value = array[y][x]

    neighbors = get_neighbors(array, x, y)
    for neighbor_x, neighbor_y in neighbors:
        neighbor_value = array[neighbor_y][neighbor_x]
        if neighbor_value <= value:
            return False

    return True


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        array = [[int(num) for num in row] for row in file.read().splitlines()]

    tic = perf_counter()
    low_points = []
    width = len(array[0])
    height = len(array)
    for y in range(height):
        for x in range(width):
            if is_low_point(array, x, y):
                low_points.append(array[y][x])

    total_risk = sum(low_points) + len(low_points)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{total_risk=} ({time_us}µs)")
