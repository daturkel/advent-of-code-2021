#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

from collections import defaultdict
import heapq
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


class TiledArray:
    def __init__(self, array: list[list[int]], mul: int):
        self.array = array
        self.raw_height = len(array)
        self.height = len(array) * mul
        self.raw_width = len(array[0])
        self.width = len(array[0]) * mul
        self.mul = mul

    def idx(self, x: int, y: int):
        raw_x = x % self.raw_width
        raw_y = y % self.raw_height
        d_x = x // self.raw_width
        d_y = y // self.raw_height
        value = self.array[raw_y][raw_x] + d_x + d_y
        if value > 9:
            value = value % 9
        return value


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        array = [[int(char) for char in row] for row in file.read().splitlines()]

    tic = perf_counter()
    tiled_array = TiledArray(array, 5)
    current = (0, 0)
    current_distance = 0
    destination = (tiled_array.width - 1, tiled_array.height - 1)
    distances = defaultdict(lambda: float("inf"))
    distances[current] = 0
    unvisited = {
        (x, y) for x in range(tiled_array.width) for y in range(tiled_array.height)
    }
    pct_visited = round(1 / (tiled_array.width * tiled_array.height) * 100)

    queue = []

    while current != destination:
        x, y = current
        neighbors = get_unvisited_neighbors(
            current, tiled_array.width, tiled_array.height, unvisited
        )
        for n_x, n_y in neighbors:
            distance_to_neighbor = tiled_array.idx(n_x, n_y)
            this_distance = distance_to_neighbor + distances[current]
            if this_distance < distances[(n_x, n_y)]:
                distances[(n_x, n_y)] = this_distance
                heapq.heappush(queue, (this_distance, (n_x, n_y)))
        unvisited.remove(current)
        current_distance, current = heapq.heappop(queue)

    distance_to_destination = distances[destination]
    toc = perf_counter()
    time_us = round((toc - tic))

    logging.info(f"{distance_to_destination=} ({time_us}s)")
