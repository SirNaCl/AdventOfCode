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
    return [list(r) for r in puzzle_input.split("\n")]


def part1(data: list[list[str]]):
    """Solve part 1."""
    tot = 0
    copied = [row.copy() for row in data]
    score = [[0 for _ in range(len(copied[0]))] for _ in range(len(copied))]
    w = "XMAS"
    wr = "SAMX"
    ymax = len(copied) - 1
    xmax = len(copied[0]) - 1
    for y in range(len(copied)):
        for x in range(len(copied[0])):
            if x < xmax - 2:
                if w in "".join(copied[y][x : x + 4]):
                    tot += 1
                    score[y][x] += 1
            if y < ymax - 2:
                yy = copied[y : y + 4]
                if w in "".join(arr[x] for arr in yy):
                    tot += 1
                    score[y][x] += 1
            if y < ymax - 2 and x < xmax - 2:
                if w in "".join([copied[y + i][x + i] for i in range(4)]):
                    tot += 1
                    score[y][x] += 1

            if y > 2 and x < xmax - 2:
                if w in "".join([copied[y - i][x + i] for i in range(4)]):
                    tot += 1
                    score[y][x] += 1

            # reversed
            if x < xmax - 2:
                if wr in "".join(copied[y][x : x + 4]):
                    tot += 1
                    score[y][x] += 1
            if y < ymax - 2:
                yy = copied[y : y + 4]
                if wr in "".join(arr[x] for arr in yy):
                    tot += 1
                    score[y][x] += 1
            if y < ymax - 2 and x < xmax - 2:
                if wr in "".join([copied[y + i][x + i] for i in range(4)]):
                    tot += 1
                    score[y][x] += 1

            if y > 2 and x < xmax - 2:
                if wr in "".join([copied[y - i][x + i] for i in range(4)]):
                    tot += 1
                    score[y][x] += 1

    return tot


def part2(data):
    """Solve part 2."""
    tot = 0
    copied = [row.copy() for row in data]
    for y in range(1, len(copied) - 1):
        for x in range(1, len(copied[0]) - 1):
            valid = True
            if copied[y][x] != "A":
                continue

            if copied[y - 1][x - 1] == "M" and copied[y + 1][x + 1] == "S":
                valid = True
            elif copied[y - 1][x - 1] == "S" and copied[y + 1][x + 1] == "M":
                valid = True
            else:
                valid = False
            if not valid:
                continue

            if copied[y + 1][x - 1] == "M" and copied[y - 1][x + 1] == "S":
                valid = True
            elif copied[y + 1][x - 1] == "S" and copied[y - 1][x + 1] == "M":
                valid = True
            else:
                valid = False

            if valid:
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
