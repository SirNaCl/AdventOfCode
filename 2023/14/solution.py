from functools import lru_cache
import math
import pathlib
import pytest
import os
import numpy as np
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [list(row) for row in puzzle_input.split("\n")]


def transpose_counter_clock(l):
    return tuple([tuple(l) for l in np.rot90(np.array(l)).tolist()])


def transpose_clock(l):
    return tuple([tuple(l) for l in np.rot90(np.array(l), -1).tolist()])


def calc_load_n(d):
    tot = 0
    for row in d:
        rocks = []
        stop = 0
        for i, c in enumerate(row):
            if c == 'O':
                rocks.append(stop)
                stop += 1
            elif c == '#':
                stop = i+1
        for r in rocks:
            tot += len(row)-r
    return tot


@ lru_cache
def slide_row(r):
    tmp = ['.'] * len(r)
    stop = 0
    for i, c in enumerate(r):
        if c == 'O':
            tmp[stop] = 'O'
            stop += 1
        elif c == '#':
            tmp[i] = '#'
            stop = i+1
    return tuple(tmp)


@lru_cache
def slide(d):
    return tuple([slide_row(r) for r in d])


@lru_cache
def cycle(d, n=1):
    r = d
    for i in range(4*n):
        r = slide(r)
        r = transpose_clock(r)
    return r


@lru_cache
def cycle100(din):
    d = din
    d = cycle(d, 100)
    return d


@lru_cache
def cycleMIL(din):
    d = din
    for i in range(10000):
        d = cycle100(d)
    return d


def part1(data):
    """Solve part 1."""
    d = transpose_counter_clock(data)
    return calc_load_n(d)


def part2(data):
    """Solve part 2."""
    d = tuple([tuple(d) for d in data])

    for i in range(1000):
        d = cycleMIL(d)
    for i in range(4):
        d = transpose_counter_clock(d)
        print(calc_load_n(d))
    return calc_load_n(d)

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
