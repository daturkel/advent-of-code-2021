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

NUM_SEGMENTS = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        signals = [
            line.replace(" | ", " ").split(" ") for line in file.read().splitlines()
        ]
        entries = [(signal[:-4], signal[-4:]) for signal in signals]

    tic = perf_counter()
    unique_segment_counts = set([NUM_SEGMENTS[digit] for digit in [1, 4, 7, 8]])
    num_ocurrences = 0
    for inputs, outputs in entries:
        segment_counts = [len(segments) for segments in outputs]
        num_ocurrences += len([x for x in segment_counts if x in unique_segment_counts])

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_ocurrences=} ({time_us}µs)")
