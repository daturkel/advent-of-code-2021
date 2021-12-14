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


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    tic = perf_counter()
    paper = []
    for i, line in enumerate(lines):
        if line == "":
            break
        x, y = [int(num) for num in line.split(",")]
        paper.append((x, y))

    folds_raw = [fold.lstrip("fold along") for fold in lines[i + 1 :]]
    folds = []
    for fold in folds_raw:
        direction, number = fold.split("=")
        folds.append((direction, int(number)))

    for fold in folds[0:1]:
        fold_coord = 1 if fold[0] == "y" else 0
        non_fold_coord = abs(fold_coord - 1)
        fold_num = fold[1]
        new_paper = []
        for point in paper:
            if point[fold_coord] > fold_num:
                new_point = [None, None]
                delta = point[fold_coord] - fold_num
                new_point[fold_coord] = fold_num - delta
                new_point[non_fold_coord] = point[non_fold_coord]
                new_point = tuple(new_point)
            else:
                new_point = point
            new_paper.append(new_point)
        paper = new_paper

    num_points = len(set(new_paper))

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{num_points=} ({time_us}µs)")
