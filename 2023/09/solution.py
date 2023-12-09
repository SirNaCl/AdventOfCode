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
    return [[int(n) for n in row.split(" ")] for row in puzzle_input.split("\n")]


def solve_seq(seq: list[int]):
    i = 0
    ss = [seq]

    while i < len(ss):
        if sum(ss[i]) == 0:
            break
        ss.append([s2 - s1 for s1, s2 in zip(ss[i], ss[i][1:])])
        i += 1
    for i, s in reversed(list(enumerate(ss))):
        ss[i - 1].append(ss[i - 1][-1] + s[-1])
    return ss[0][-1]


def part1(data):
    """Solve part 1."""
    return sum([solve_seq(d) for d in data])


def part2(data: list[list[int]]):
    """Solve part 2."""
    return sum([solve_seq(list(reversed(d))) for d in data])


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
