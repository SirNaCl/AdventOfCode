import pathlib
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [[int(e) for e in line.split(" ")] for line in puzzle_input.split("\n")]


def validate_row(r):
    dir_up = r[1] > r[0]

    for a, b in zip(r, r[1:]):
        if abs(a - b) > 3 or a == b or (b > a) != dir_up:
            return False

    return True


def part1(data):
    """Solve part 1."""
    return sum([1 if validate_row(r) else 0 for r in data])


def part2(data):
    """Solve part 2."""
    tot = 0
    for r in data:
        found = validate_row(r)
        i = 0
        while not found and i < len(r):
            rr = r[:i]
            if i < len(r) - 1:
                rr += r[i + 1 :]
            found = validate_row(rr)
            i += 1

        if found:
            tot += 1

    return tot


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
    elif puzzle.answered_b or ans_b == 307:
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
