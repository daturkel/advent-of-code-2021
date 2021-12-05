#!/usr/bin/env python3

# Call with an input file as an argument, or else default to test.txt

from collections import namedtuple
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


class Number:
    def __init__(self, value: int, status: bool = False):
        self.value = value
        self.status = status


class Board:
    def __init__(self, board_buffer: list[str]):
        self.numbers = [
            [Number(int(num)) for num in row.split()] for row in board_buffer
        ]

    def _check_row(self, row_index: int) -> bool:
        win = True
        for number in self.numbers[row_index]:
            win = win and number.status
            if not win:
                break
        return win

    def _check_column(self, col_index: int) -> bool:
        win = True
        for row in self.numbers:
            win = win and row[col_index].status
            if not win:
                break
        return win

    def check_for_win(self) -> bool:
        win = False

        # we assume # of rows = # of columns
        for i in range(len(self.numbers[0])):
            win = win or self._check_row(i)
            if win:
                break
            win = win or self._check_column(i)
            if win:
                break

        return win

    def call_number(self, called_number: int):
        for row in self.numbers:
            for number in row:
                if number.value == called_number:
                    number.status = True

    def get_score(self) -> int:
        value = 0
        for row in self.numbers:
            for number in row:
                if not number.status:
                    value += number.value
        return value


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        raw_lines = file.read().splitlines()
        # when parsing input, we'll use an empty line to trigger adding a board, so add
        # an empty line to the end so we don't miss the last board
        raw_lines.append("")

    tic = perf_counter()
    numbers = [int(num) for num in raw_lines[0].split(",")]

    boards = []
    board_buffer = []

    for line in raw_lines[2:]:
        if line == "":
            new_board = Board(board_buffer)
            boards.append(new_board)
            board_buffer = []
        else:
            board_buffer.append(line)

    for (i, number), board in product(enumerate(numbers), boards):
        board.call_number(number)
        if i >= 5 and board.check_for_win():
            break

    board_score = board.get_score()
    score = board_score * number

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{score=} ({time_us}µs)")
