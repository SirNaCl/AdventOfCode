from math import lcm
import pathlib
import time
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    p = puzzle_input.split("\n")
    d = dict()
    for pp in p[2:]:
        pd = pp.replace("(", "").replace(")", "")
        pd = pd.split(" = ")
        d[pd[0]] = tuple(pd[1].split(", "))

    return p[0], d


class Ghost:
    def __init__(self, loc, m):
        self.loc = loc
        self.m = m
        self.period = -1

    def done(self):
        return self.loc[-1] == "Z"

    def move(self, di):
        self.loc = self.m[self.loc][0] if di == "L" else self.m[self.loc][1]


def part1(data):
    """Solve part 1."""
    turns, m = data
    l = "AAA"
    i = 0
    while l != "ZZZ":
        l = m[l][0] if turns[i % len(turns)] == "L" else m[l][1]
        i += 1
    return i


def part2(data):
    """Solve part 2."""
    turns, m = data
    ghosts = []
    periods = []
    for key in m.keys():
        if key[-1] == "A":
            ghosts.append(Ghost(key, m))

    for g in ghosts:
        i = 0
        while not g.done():
            g.move(turns[i % len(turns)])
            i += 1
        periods.append(i)

    return lcm(*periods)


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
