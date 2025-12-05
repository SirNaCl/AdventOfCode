import pathlib
from typing import Tuple
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import git

# add common util
PATH_ROOT = git.Repo(__file__, search_parent_directories=True).git.rev_parse(
    "--show-toplevel"
)
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.func import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
ROOT_DIR = PUZZLE_DIR.parent.parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    s = puzzle_input.split("\n\n")
    r = [ri.split("-") for ri in s[0].split("\n")]
    ri = [(int(r1), int(r2)) for r1, r2 in r]
    ids = [int(si) for si in s[1].split("\n")]
    return ri, ids


def part1(data: Tuple[list, list]):
    """Solve part 1."""
    ranges, ids = data
    idc: list = ids.copy()
    idc = sorted(idc)

    for r1, r2 in ranges:
        idc.append(r1)
        idc.append(r2)
        idc.sort()
        r1i = idc.index(r1)
        r2i = idc.index(r2)
        idc = idc[:r1i] + idc[r2i + 1 :]
        try:
            # index takes first found element, remove in case of duplicates
            while r2 in idc:
                idc.remove(r2)
        except ValueError:
            pass

    return len(ids) - len(idc)


def part2(data: Tuple[list, list]):
    """Solve part 2."""
    global p2
    p2 = True
    tot = 0
    ranges, _ = data
    cranges = []

    for r1, r2 in ranges:
        rr1, rr2 = r1, r2
        for cr1, cr2 in cranges:
            if cr1 <= rr1 <= cr2:
                rr1 = cr2 + 1
            if cr1 <= rr2 <= cr2:
                rr2 = cr1 - 1

        if rr1 <= rr2:
            cranges.append((rr1, rr2))

    for cr1, cr2 in cranges:
        tot += cr2 - cr1 + 1
    return tot


#### UTILITY FUNCTIONS ####
def init():
    with open(ROOT_DIR / "aoc-key", "r") as keyfile:
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
