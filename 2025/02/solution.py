import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
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
    return [s.split('-') for s in puzzle_input.split(',')]


def part1(data):
    """Solve part 1."""
    sum = 0
    for r1, r2 in data:
        start = int(r1)
        stop = int(r2)
        for i in range(start, stop + 1):
            s = str(i)
            l = len(s) // 2
            a = s[:l]
            b = s[l:]
            if a == b:
                sum += i
    return sum

def fill_str(pattern, l):
    s = ""
    while len(s) < l:
        s += pattern
    if len(s) > l:
        return None
    return s

def is_invalid(s: str):
    for p_len in range(1, len(s)//2 + 1):
        sl = fill_str(s[:p_len], len(s))
        if sl is None:
            continue
        if sl == s:
            return True

    return False


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    sum = 0
    for r1, r2 in data:
        start = int(r1)
        stop = int(r2)
        for i in range(start, stop + 1):
            if is_invalid(str(i)):
                sum += i
    return sum

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
