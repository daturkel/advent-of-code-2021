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
SEGMENTS_TO_DIGIT = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def as_element(singleton: set) -> str:
    return list(singleton)[0]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [
            line.replace(" | ", " ").split(" ") for line in file.read().splitlines()
        ]
        entries = [
            (
                [set(signal) for signal in line[:-4]],
                [set(signal) for signal in line[-4:]],
            )
            for line in lines
        ]

    tic = perf_counter()

    total = 0
    for inputs, outputs in entries:
        mapping = {}

        # a is the difference of 1 and 7
        one = [signal for signal in inputs if len(signal) == 2][0]
        seven = [signal for signal in inputs if len(signal) == 3][0]
        mapping["a"] = list(seven - one)[0]

        # the intersection between 1 and 6 shows us c versus f
        six_segment_digits = [signal for signal in inputs if len(signal) == 6]
        six = [
            signal
            for signal in six_segment_digits
            if len(set(signal).intersection(one)) == 1
        ][0]
        mapping["f"] = as_element(six.intersection(one))
        mapping["c"] = as_element(one - six)

        # b and d are 4 - 1
        # of b and d, the one which appears in the six-segment digits twice is d
        # and the other is d
        four = [signal for signal in inputs if len(signal) == 4][0]
        bd = four - one
        for segment in bd:
            num_appearances = len(
                [signal for signal in six_segment_digits if segment in signal]
            )
            if num_appearances == 2:
                mapping["d"] = segment
                mapping["b"] = as_element(bd - set(segment))

        # the segment not in 9 must be e, then the last segment is g
        nine = [
            signal
            for signal in six_segment_digits
            if (mapping["d"] in signal) and (mapping["c"] in signal)
        ][0]
        mapping["e"] = as_element(set("abcdefg") - nine)
        mapping["g"] = as_element(set("abcdefg") - set(mapping.values()))

        reverse_mapping = {value: key for key, value in mapping.items()}

        output_digits = []
        for output in outputs:
            output_str = "".join(sorted([reverse_mapping[char] for char in output]))
            output_digits.append(SEGMENTS_TO_DIGIT[output_str])

        total += int("".join(output_digits))

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{total=} ({time_us}µs)")
