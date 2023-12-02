import pathlib
import pytest
from aocd import get_data

PUZZLE_DIR = pathlib.Path(__file__).parent


def get_session():
    with open("aoc-key", "r") as keyfile:
        return keyfile.read()


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


if __name__ == "__main__":
    assert pytest.main(PUZZLE_DIR) != 1
    puzzle_input = get_data(
        session=get_session(), year=2023, day=None  # TODO: Set today's date
    )
    print(solve(puzzle_input))
