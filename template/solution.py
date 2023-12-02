import pathlib
import pytest
import os
from aocd import get_data
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def parse(puzzle_input):
    """Parse input."""


def part1(data):
    """Solve part 1."""


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


def main():
    init()
    puzzle = Puzzle(YEAR, DAY)
    assert pytest.main(PUZZLE_DIR) != 1
    ans = solve(puzzle.input_data)
    if not puzzle.answered_a and ans[0] is not None:
        print(f"Submitting {ans[0]} as answer to part 1")
        puzzle.answer_a = ans[0]
    else:
        print(
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans[0]}"
        )

    if not puzzle.answered_b and ans[1] is not None:
        print(f"Submitting {ans[1]} as answer to part 2")
        puzzle.answer_b = ans[1]
    else:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans[1]}"
        )


if __name__ == "__main__":
    main()
