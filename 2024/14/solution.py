from dataclasses import dataclass
from math import prod
import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import re

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

import common

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)

ROWS = 102
COLS = 100
ITERATIONS = 100


@dataclass
class Robot:
    col: int
    row: int
    dcol: int
    drow: int

    def destination(self, iters=ITERATIONS):
        r = (self.row + self.drow * iters) % (ROWS + 1)
        c = (self.col + self.dcol * iters) % (COLS + 1)

        return r, c


#### SOLUTION ####
p2 = False

NUM_ROBOTS = 0


def parse(puzzle_input):
    """Parse input."""
    global NUM_ROBOTS
    NUM_ROBOTS = len(puzzle_input)
    return [
        Robot(*map(int, re.findall(r"(-?\d+)", line)))
        for line in puzzle_input.split("\n")
    ]


def quadrant(row, col):
    # 0 1
    # 2 3
    # invalid: -1
    if row < ROWS / 2 and col < COLS / 2:
        return 0
    if row < ROWS / 2 and col > COLS / 2:
        return 1
    if row > ROWS / 2 and col < COLS / 2:
        return 2
    if row > ROWS / 2 and col > COLS / 2:
        return 3
    return -1


def part1(data, rows=102, cols=100):
    """Solve part 1."""
    global ROWS
    global COLS
    ROWS = rows
    COLS = cols
    quads = [0, 0, 0, 0, 0]
    locations = [robot.destination() for robot in data]
    locQ = [quadrant(r, c) for r, c in locations]

    for q in locQ:
        quads[q] += 1

    return prod(quads[:-1])


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    grid_empty = [["."] * (COLS + 1) for _ in range(ROWS + 1)]
    for iter in range(20000):
        g = [r.copy() for r in grid_empty]

        for r, c in [robot.destination(iter) for robot in data]:
            g[r][c] = "#"

        for row in g:
            s = "".join(row)
            if s.count("#######################") > 0:
                return iter


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read().strip()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


def submit(puzzle, ans_a, ans_b):
    if ans_a is None:
        print("No solution for part 1, skipping submission!")
    elif puzzle.answered_a:
        print(
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans_a} "
            + f"({'correct' if str(puzzle.answer_a) == str(ans_a) else 'incorrect'})!"
        )
    else:
        print(f"Submitting {ans_a} as answer to part 1:")
        puzzle.answer_a = ans_a

    if ans_b is None:
        print("No solution for part 2, skipping submission!")
    elif puzzle.answered_b:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans_b} "
            + f"({'correct' if str(puzzle.answer_b) == str(ans_b) else 'incorrect'})!"
        )
    else:
        print(f"Submitting {ans_b} as answer to part 2:")
        puzzle.answer_b = ans_b


def main():
    init()
    puzzle = Puzzle(YEAR, DAY)
    assert pytest.main(PUZZLE_DIR) == 0
    ans = solve(puzzle.input_data)
    submit(puzzle, *ans)


if __name__ == "__main__":
    main()
