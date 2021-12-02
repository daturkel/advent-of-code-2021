#!/usr/bin/env python3

# Call with an input file as an argument, or else default to input_01.txt

import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def get_sliding_windows(depths: list[int], window_width: int) -> list[int]:
    """Given a list of depths, create a new list of the sums of a sliding window_width-measurement
    window of depths.

    Args:
        depths: A list of integer depths.

    Returns:
        A list of the sums of a sliding window_width-measurement window of depths.

    """
    max_start_idx = len(depths) - window_width + 1
    windows = [sum(depths[i : i + window_width]) for i in range(max_start_idx)]

    return windows


def calc_num_increases(depths: list[int]) -> int:
    """Given a list of depths, calculate the number of times that the depth increases.

    Args:
        depths: A list of integer depths.

    Returns:
        The number of times that a depth was greater than the preceding depth

    """
    current_depth = depths.pop(0)
    num_increases = 0

    for depth in depths:
        if depth > current_depth:
            num_increases += 1
        current_depth = depth

    return num_increases


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./input_01.txt"
    with open(input_file, "r") as file:
        depths = [int(line) for line in file.readlines()]

    tic = perf_counter()
    windows = get_sliding_windows(depths, 3)
    num_increases = calc_num_increases(windows)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_increases=} ({time_us}µs)")
