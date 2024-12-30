from itertools import starmap
import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import networkx as nx
import functools as ft
from collections import deque

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.func import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


# Finished both parts in 11 minutes (yay), I wonder what placement I would have gotten
# if I could be bothered waking up at 6..
#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    G = nx.Graph()
    deque(starmap(G.add_edge, [line.split('-') for line in puzzle_input.split('\n')]))
    return G


@benchmark
def part1(data):
    """Solve part 1."""
    tot = 0
    for cl in nx.enumerate_all_cliques(data):
        if len(cl) < 3:
            continue
        if len(cl) > 3:
            break
        if any([c.startswith('t') for c in cl]):
            tot += 1
    return tot


# 527ms
# 440ms (exhaust generator using deque instead of list)
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    group = deque(nx.enumerate_all_cliques(data), maxlen=1).pop()

    return ",".join(sorted(group))



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
