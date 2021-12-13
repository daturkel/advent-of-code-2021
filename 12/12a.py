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


def paths_to_here(
    here: str, edges: list[tuple[str, str]], visited: list[str] = None
) -> int:
    if visited is None:
        visited = ["end"]

    if here == "start":
        return 1

    edges_to_here = [(a, b) for (a, b) in edges if (b == here) and (a not in visited)]

    num = 0
    for location, _ in edges_to_here:
        if location == location.lower():
            num += paths_to_here(location, edges, visited + [location])
        else:
            num += paths_to_here(location, edges, visited)

    return num


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        edges = [tuple(edge.split("-")) for edge in file.read().splitlines()]

    edges += [(b, a) for (a, b) in edges]
    edges = set(edges)

    tic = perf_counter()
    num_paths = paths_to_here("end", edges)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_paths=} ({time_us}µs)")
