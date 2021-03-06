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


def execute_instructions(instructions: list[str]) -> tuple[int]:
    """Given a list of instructions, get the final horizontal distance and depth.

    Args:
        instructions: A list of integer depths.

    Returns:
        A tuple of the final horizontal distance and depth.

    """
    horizontal = 0
    depth = 0

    direction_to_vector = {"up": [0, -1], "down": [0, 1], "forward": [1, 0]}

    for instruction in instructions:
        direction, amount = instruction.split(" ")
        amount = int(amount)
        vector = direction_to_vector[direction]
        horizontal += vector[0] * amount
        depth += vector[1] * amount

    return horizontal, depth


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        instructions = file.readlines()

    tic = perf_counter()
    horizontal, depth = execute_instructions(instructions)
    product = horizontal * depth
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{horizontal=}, {depth=}, product={product} ({time_us}µs)")
