import pathlib
from typing import Iterable
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
from itertools import accumulate, product

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.func import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def indices(lst: Iterable, ele):
    return [i for i, e in enumerate(lst) if e == ele]


def parse(puzzle_input):
    """Parse input."""
    keys = []
    locks = []

    for obj in puzzle_input.split("\n\n"):
        rows = obj.split("\n")
        is_lock = "#" in rows[0]
        o = [-1] * 5

        for r in rows:
            for i in indices(r, "#"):
                o[i] += 1

        [keys, locks][is_lock].append(tuple(o))

    return keys, locks


def fits(o1, o2):
    return all(a + b < 6 for a, b in zip(o1, o2))


def part1(data):
    """Solve part 1."""
    return sum([1 for p in product(*data) if fits(*p)])


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True


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