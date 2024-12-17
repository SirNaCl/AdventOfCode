from collections import defaultdict
import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import re
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    rules, molecule = puzzle_input.split("\n\n")
    d = defaultdict(list)

    for line in rules.split("\n"):
        src, trg = line.split(" => ")
        d[src].extend(re.findall(r"[A-Z][a-z]?", trg))

    return d, re.findall(r"[A-Z][a-z]?", molecule)


def part1(data):
    """Solve part 1."""
    rules, molecule = data
    mutations = set()
    for idx, m in enumerate(molecule):
        for replacement in rules[m]:
            tmp = molecule.copy()
            tmp[idx] = replacement
            mutations.add("".join(tmp))

    return len(mutations)


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    rules, target = data

    for r in rules:
        sp = re.findall(r"[A-Z][a-z]?", r)
        if len(sp) == 1:
            continue
        for s in sp:
            rules

    G = nx.from_dict_of_lists(rules, create_using=nx.DiGraph)
    fig = plt.figure()
    nx.draw(G, ax=fig.add_subplot())
    mpl.use("Agg")
    fig.savefig("graph.png")
    # term = set()
    # for v in rules.values():
    #     for t in v:
    #         for e in re.findall(r"[A-Z][a-z]?", t):
    #         if e not in rules:
    #             term.add(e)
    #
    # pprint(term)


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
