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


def get_unvisited_neighbors(
    current: tuple[int], width: int, height: int, unvisited: list[tuple[int, int]]
) -> list[tuple[int]]:
    x, y = current
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (
            (0 <= x + dx < width)
            and (0 <= y + dy < height)
            and ((x + dx, y + dy) in unvisited)
        ):
            neighbors.append((x + dx, y + dy))

    return neighbors


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        array = [[int(char) for char in row] for row in file.read().splitlines()]

    verbose = True if len(sys.argv) > 2 else False

    tic = perf_counter()
    width = len(array[0])
    height = len(array)
    current = (0, 0)
    destination = (width - 1, height - 1)
    distances = defaultdict(lambda: float("inf"))
    distances[current] = 0
    unvisited = {(x, y) for x in range(width) for y in range(height)}
    pct_visited = round(1 / (width * height) * 100)

    while current != destination:
        if verbose:
            visited = width * height - len(unvisited)
            new_pct_visited = round(visited / (width * height) * 100)
            if new_pct_visited > pct_visited:
                pct_visited = new_pct_visited
                logging.info(f"{pct_visited}% visited")
        x, y = current
        neighbors = get_unvisited_neighbors(current, width, height, unvisited)
        for n_x, n_y in neighbors:
            distance_to_neighbor = array[n_y][n_x]
            this_distance = distance_to_neighbor + distances[current]
            if this_distance < distances[(n_x, n_y)]:
                distances[(n_x, n_y)] = this_distance
        unvisited.remove(current)
        current = min(unvisited, key=lambda x: distances[x])

    distance_to_destination = distances[destination]
    toc = perf_counter()
    time_us = round((toc - tic))

    logging.info(f"{distance_to_destination=} ({time_us}s)")
