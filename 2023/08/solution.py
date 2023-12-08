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


class Node:
    def __init__(self, name, L=None, R=None, cost=[-1, -1]):
        self.name = name
        self.L = L
        self.R = R
        self.cost = cost

    def __str__(self):
        if self.L is not None and self.R is not None:
            return f"{self.name} => {self.L.name}: {self.R.name}"
        return self.name

    def calc_cost(self, go2L, at_start=False, d=1, ma=100):
        if not at_start and self.name[-1] == "Z":
            return 0

        if d >= ma:
            return ma

        if go2L:
            if self.cost[0] == -1:
                if self.L is None:
                    return ma
                if self.L.name == self.name:
                    c = self.cost[1]
                else:
                    c = self.L.calc_cost(False, False, d + 1) + 1
                self.cost[0] = c

            if not at_start and self.name[-1] == "Z":
                return 0

            return self.cost[0]

        if self.cost[1] == -1:
            if self.R is None:
                return ma

            if self.R.name == self.name:
                c = self.cost[0]
            else:
                c = self.R.calc_cost(True, False, d + 1) + 1

            self.cost[1] = c

        if not at_start and self.name[-1] == "Z":
            return 0

        return self.cost[1]


def part2(data):
    """Solve part 2."""
    turns, m = data
    i = 0
    ghosts = []
    network = {}
    for key, item in m.items():
        network[key] = Node(key)
        if key[-1] == "A":
            ghosts.append(Ghost(key, m))

    for key, item in m.items():
        network[key].L = network[item[0]]
        network[key].R = network[item[1]]

    for key, item in network.items():
        # if key[-1] == "A":
        item.calc_cost(turns[0] == "R", True, ma=len(network.keys()))

    done = 0
    t = time.time()
    while done != len(ghosts):
        done = 0
        for g in ghosts:
            g.move(turns[i % len(turns)])
            if g.done():
                done += 1
        i += 1
    return i


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
