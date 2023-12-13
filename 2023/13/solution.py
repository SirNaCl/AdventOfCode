from functools import lru_cache
from gettext import find
from itertools import combinations
import pathlib
import pytest
import os
from aocd.models import Puzzle
import numpy as np

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    p = puzzle_input.split("\n\n")
    return [[l for l in pp.split("\n")] for pp in p]


def is_sym(s):
    for st, en in zip(s, s[-1::-1]):
        if st != en:
            return False
    return True


def substr(s, l):
    r = []
    for i in range(len(s) - l + 1):
        r.append((i, s[i : i + l]))
    return [r[0], r[-1]]


@lru_cache
def find_largest(string, ln=-1):
    # Returns start, substr
    if ln == -1:
        ln = len(string)
    if ln == 1:
        return 0, string[0]

    for i, sub in substr(string, ln):
        if is_sym(sub):
            return i, sub

    return find_largest(string, ln - 1)


def largest_many(pattern):
    l = len(pattern[0])
    found = False
    while l > 1 and not found:
        found = True
        for f, s in zip(pattern, pattern[1:]):
            fl = find_largest(f, l)
            sl = find_largest(s, l)
            if len(fl[1]) != len(sl[1]):
                l -= 1
                found = False
                break

    return find_largest(pattern[0], l)


def part1(data):
    """Solve part 1."""
    tot = 0
    for p in data:
        col = largest_many(p)
        rows = [
            "".join(r) for r in np.array([[c for c in col] for col in p]).T.tolist()
        ]
        row = largest_many(rows)
        cl = col[0] + (len(col[1]) // 2)
        rl = row[0] + (len(row[1]) // 2)
        if len(col[1]) > len(row[1]):
            tot += cl
        else:
            tot += rl * 100
    return tot


def part2(data):
    """Solve part 2."""


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


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
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans_a}!"
        )
    else:
        print(f"Submitting {ans_a} as answer to part 1:")
        puzzle.answer_a = ans_a

    if ans_b is None:
        print("No solution for part 2, skipping submission!")
    elif puzzle.answered_b:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans_b}!"
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
