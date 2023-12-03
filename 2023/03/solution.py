import pathlib
import pytest
import os
from aocd.models import Puzzle
from numpy import prod

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def flatten(l):
    return [item for sublist in l for item in sublist]


def adjac(x, y):
    nb = lambda c: [c - 1, c, c + 1]
    return flatten([[(xx, yy) for xx in nb(x)] for yy in nb(y)])


def is_symbol(s: str):
    return s in "!@#$%^&*()-_=+<>/"


def is_gear(s):
    return s == "*"


def parse(puzzle_input):
    """Parse input."""
    lines = puzzle_input.split("\n")
    puz = list()
    for line in lines:
        puz.append([c for c in line])
    return puz


def coords_with_symb_nb(data):
    with_sym = list()
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if not c.isdigit():
                continue

            adjacent = adjac(x, y)
            for ax, ay in adjacent:
                if 0 < ay < len(data) and 0 < ax < len(row) and is_symbol(data[ay][ax]):
                    with_sym.append((y, x))

    return with_sym


def coords_with_gear_nb(data: list[list[str]]):
    with_sym = list()
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if not c.isdigit():
                continue

            adjacent = adjac(x, y)
            for ax, ay in adjacent:
                if 0 < ay < len(data) and 0 < ax < len(row) and is_gear(data[ay][ax]):
                    with_sym.append(((y, x), (ay, ax)))

    return with_sym


def digits_before(data, checked, row, col):
    if col < 0 or row < 0 or not data[row][col].isdigit():
        checked.append((row, col))
        return ""

    checked.append((row, col))
    b4 = digits_before(data, checked, row, col - 1)
    return b4 + data[row][col] if len(b4) > 0 else data[row][col]


def digits_after(data, checked, row, col):
    if col >= len(data[0]) or row > len(data) or (row, col) in checked:
        checked.append((row, col))
        return ""
    if not data[row][col].isdigit():
        checked.append((row, col))
        return ""

    af = digits_after(data, checked, row, col + 1)
    checked.append((row, col))
    return data[row][col] + af if len(af) > 0 else data[row][col]


def part1(data):
    """Solve part 1."""
    tot = 0
    checked = list()
    for coords in coords_with_symb_nb(data):
        if coords in checked:
            continue
        dy, dx = coords
        s = (
            digits_before(data, checked, dy, dx - 1)
            + data[dy][dx]
            + digits_after(data, checked, dy, dx + 1)
        )
        tot += int(s)
        checked.append(coords)

    return tot


def part2(data):
    """Solve part 2."""
    gears = dict()
    checked = list()
    for coords, gear in coords_with_gear_nb(data):
        if coords in checked:
            continue
        dy, dx = coords
        c = data[dy][dx]
        s = (
            digits_before(data, checked, dy, dx - 1)
            + c
            + digits_after(data, checked, dy, dx + 1)
        )
        checked.append(coords)

        if gear in gears:
            gears[gear].append(int(s))
        else:
            gears[gear] = [int(s)]

    return sum([prod(nums) for nums in gears.values() if len(nums) == 2])


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
