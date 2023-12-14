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
    return [list(pp.split("\n")) for pp in p]


def boring(slist: list[str], part2=False):
    ptr = 1
    while ptr < len(slist):
        b4 = slist[: ptr]
        diff = 0
        for f, l in zip(b4[:: -1], slist[ptr:]):
            if f != l:
                for ff, ll in zip(f, l):
                    if ff != ll:
                        diff += 1

        if (not part2 and diff == 0) or (part2 and diff == 1):
            return ptr

        ptr += 1
    return 0


def part1(data):
    """Solve part 1."""
    tot = 0
    for p in data:
        rows = ["".join(r) for r in np.array([list(col)
                                             for col in p]).T.tolist()]
        hor = boring(p)
        vert = boring(rows)

        if hor > vert:
            tot += hor * 100
        else:
            tot += vert
    return tot


def part2(data):
    """Solve part 2."""
    tot = 0
    for p in data:
        rows = ["".join(r) for r in np.array([list(col)
                                             for col in p]).T.tolist()]
        hor = boring(p, True)
        vert = boring(rows, True)

        if hor > vert:
            tot += hor * 100
        else:
            tot += vert
    return tot


#### UTILITY FUNCTIONS ####
def init():
    with open(PUZZLE_DIR / ".." / ".." / "aoc-key", "r") as keyfile:
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
