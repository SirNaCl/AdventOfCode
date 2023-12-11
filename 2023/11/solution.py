import pathlib
import pytest
import os
import numpy as np
from aocd.models import Puzzle


PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input, exp=1):
    """Parse input."""
    p = np.array(
        [
            [int(n) for n in row]
            for row in puzzle_input.replace(".", "0").replace("#", "1").split("\n")
        ]
    )

    i = 0
    expandedr = []
    while i < p.shape[0]:
        if sum(p[i]) == 0:
            expandedr.append(i)
        i += 1
    i = 0
    pt = p.T
    expandedc = []
    while i < pt.shape[0]:
        if sum(pt[i]) == 0:
            expandedc.append(i)
        i += 1
    ic = 0
    coords = []
    for i, r in enumerate(p):
        jc = 0
        if i in expandedr:
            ic += exp
            continue

        for j, c in enumerate(r):
            if c == 1:
                coords.append((i + ic, j + jc))
            elif j in expandedc:
                jc += exp

    return coords


def manhattan(a, b):
    return sum(abs(aa - bb) for aa, bb in zip(a, b))


def part1(data):
    """Solve part 1."""
    coords = data

    d = {}
    while len(coords) > 0:
        cc = coords.pop(0)
        d[cc] = coords.copy()

    tot = 0

    for k, v in d.items():
        for p in v:
            tot += manhattan(k, p)
    return tot


def part2(data):
    """Solve part 2."""
    return part1(data)


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    parsed = parse(puzzle_input, 999999)
    data = parsed if parsed is not None else puzzle_input
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
