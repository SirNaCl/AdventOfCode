import os
import pathlib
import pytest
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def parse(puzzle_input):
    """Parse input."""
    lines = []
    for line in puzzle_input.split("\n"):
        lines.append(
            line.replace(",", "").replace(";", "").replace(":", "").split(" ")[2:]
        )
    return lines


def part1(data: list):
    """Solve part 1."""
    REDS = 12
    GREENS = 13
    BLUES = 14
    tot = 0
    for k, d in enumerate(data):
        canceled = False
        col = {"green": 0, "red": 0, "blue": 0}
        for i, (n, c) in enumerate(zip(d, d[1:])):
            if i % 2:
                continue
            if c == "red" and int(n) > REDS:
                canceled = True
                break
            if c == "blue" and int(n) > BLUES:
                canceled = True
                break
            if c == "green" and int(n) > GREENS:
                canceled = True
                break

            col[c] += int(n)

        if not canceled:
            tot += k + 1
    return tot


def part2(data):
    """Solve part 2."""
    maximums = []
    for d in data:
        col = {"green": -1, "red": -1, "blue": -1}
        for i, (n, c) in enumerate(zip(d, d[1:])):
            if i % 2:
                continue
            col[c] = int(n) if int(n) > col[c] else col[c]

        maximums.append(col["red"] * col["blue"] * col["green"])
    return sum(maximums)


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
    if not puzzle.answered_a:
        print(f"Submitting {ans[0]} as answer to part 1")
        puzzle.answer_a = ans[0]
    else:
        print(
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans[0]}"
        )

    if not puzzle.answered_b:
        print(f"Submitting {ans[1]} as answer to part 2")
        puzzle.answer_b = ans[1]
    else:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans[1]}"
        )


if __name__ == "__main__":
    main()
