import pathlib
from numpy import sqrt
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.func import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    return GridChar(puzzle_input)


def dist(p1, p2) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


# 5900ms
@benchmark
def part1(data: GridChar, cutoff=100):
    """Solve part 1."""
    start = data.find_all("S")[0]
    end = data.find_all("E")[0]
    G = data.to_graph(ignore=["#"])
    non_cheat = nx.shortest_path(G, start, end)

    tot = 0

    for i, pt1 in enumerate(non_cheat[:-cutoff]):
        for j, pt2 in enumerate(non_cheat[i + cutoff :]):
            l1 = j + cutoff  # how long is the path without cheat

            if (cheat := dist(pt1, pt2)) <= 2 and l1 - cheat >= cutoff:
                tot += 1

    return tot


# 5900ms
@benchmark
def part2(data: GridChar, cutoff=100):
    """Solve part 2."""
    global p2
    p2 = True

    start = data.find_all("S")[0]
    end = data.find_all("E")[0]
    G = data.to_graph(ignore=["#"])
    non_cheat = nx.shortest_path(G, start, end)

    tot = 0

    for i, pt1 in enumerate(non_cheat[:-cutoff]):
        for j, pt2 in enumerate(non_cheat[i + cutoff :]):
            l1 = j + cutoff  # how long is the path without cheat

            if (cheat := dist(pt1, pt2)) <= 20 and l1 - cheat >= cutoff:
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
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans_a} "
            + f"({'correct' if str(puzzle.answer_a) == str(ans_a) else 'incorrect'})!"
        )
    else:
        print(f"Submitting {ans_a} as answer to part 1:")
        puzzle.answer_a = ans_a

    if ans_b is None:
        print("No solution for part 2, skipping submission!")
    elif puzzle.answered_b:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans_b} "
            + f"({'correct' if str(puzzle.answer_b) == str(ans_b) else 'incorrect'})!"
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
