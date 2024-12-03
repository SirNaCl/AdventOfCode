import pathlib
import pytest
import os
import re
from aocd.models import Puzzle


PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
PATTERN = r"mul\(\d{1,3},\d{1,3}\)"
PATTERN2 = r"mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)"


def parse(puzzle_input, pattern):
    """Parse input."""
    return re.findall(pattern, puzzle_input)


def part1(data):
    """Solve part 1."""
    tot = 0
    for o in data:
        s = o.split("(")[1]
        s = s.split(")")[0]
        a, b = s.split(",")
        tot += int(a) * int(b)
    return tot


def part2(data: list[str]):
    """Solve part 2."""
    tot = 0
    sleeping = False
    for o in data:
        if o.count("don't()") == 1:
            sleeping = True
            continue

        if o.count("do()") == 1:
            sleeping = False
            continue

        if sleeping:
            continue

        s = o.split("(")[1]
        s = s.split(")")[0]
        a, b = s.split(",")
        tot += int(a) * int(b)

    return tot


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read().strip()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""

    parsed = parse(puzzle_input, PATTERN)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    parsed = parse(puzzle_input, PATTERN2)
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
