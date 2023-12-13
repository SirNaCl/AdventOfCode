from functools import lru_cache
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
    l = puzzle_input.split("\n")
    return [(s.split()[0], [int(n) for n in s.split()[1].split(",")]) for s in l]


@lru_cache
def solve_recur(springs: str, nums):
    if springs == "":
        return 1 if len(nums) == 0 else 0

    if len(nums) == 0:
        return 0 if "#" in springs else 1

    result = 0
    # if . or treat ? as .
    if springs[0] != "#":
        result += solve_recur(springs[1:], nums)

    # if # or treat ? as #
    if springs[0] != ".":
        blocklen = nums[0]
        springs += "."  # to avoid out of bounds
        if (
            blocklen <= len(springs)  # check if fits
            and "." not in springs[:blocklen]  # check that we only have # or ?
            and (springs[blocklen] != "#")  # check that it's long enough
        ):
            result += solve_recur(springs[blocklen + 1 :], nums[1:])

    return result


def part1(data):
    """Solve part1."""
    tot = 0
    for d in data:
        tot += solve_recur(d[0], tuple(d[1]))
    return tot


def part2(data):
    """Solve part 2."""
    tot = 0
    for d in data:
        dd = "?".join([d[0]] * 5)
        tot += solve_recur(dd, tuple(d[1] * 5))
    return tot


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
