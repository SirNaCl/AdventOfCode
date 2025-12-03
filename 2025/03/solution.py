from functools import lru_cache
import pathlib
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
    l = puzzle_input.split('\n')
    return [[int(i) for i in li] for li in l]

def part1(data):
    """Solve part 1."""
    tot = 0
    for l in data:
        d2 = sorted(l, reverse=True)
        i = 0
        while True:
            h = d2[i]
            hi = l.index(h)
            try:
                lo = sorted(l[hi + 1:], reverse=True)[0]
                tot += 10 * h + lo
                break
            except:
                i += 1

    return tot

def recur(li, length):
    if length == 0:
        return ""

    d2 = sorted(li, reverse=True)
    i = 0
    s = []
    while True:
        h = d2[i]
        hi = li.index(h)
        if len(li[hi:]) >= length:
            s = li[hi:]
            break

        i += 1

    return str(s[0]) + recur(s[1:], length - 1)



def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    tot = 0
    for l in data:
        tot += int(recur(l, 12))

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
