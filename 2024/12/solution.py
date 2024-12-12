from collections import defaultdict
import pathlib
from networkx import connected_components
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import benchmark
import common.grid

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    return common.grid.GridChar(puzzle_input)


def remove_invalid_edges_ret_graph(grid: common.grid.GridChar):
    G = grid.to_graph()
    to_remove = set()
    for e in G.edges():
        if (
            G.nodes[e[0]][common.grid.GRID_VALUE]
            != G.nodes[e[1]][common.grid.GRID_VALUE]
        ):
            to_remove.add(e)

    G.remove_edges_from(to_remove)
    return G


def circumference(nodes):
    circ = list()
    for n in nodes:
        circ.append((n[0] - 1, n[1]))
        circ.append((n[0] + 1, n[1]))
        circ.append((n[0], n[1] - 1))
        circ.append((n[0], n[1] + 1))

    return [c for c in circ if c not in nodes]


# 100ms
@benchmark
def part1(data):
    """Solve part 1."""
    grid = data.copy()
    tot = 0
    G = remove_invalid_edges_ret_graph(grid)
    for garden in connected_components(G):
        tot += len(garden) * len(circumference(garden))

    return tot


def sides(nodes):
    s = defaultdict(list)
    for n in nodes:
        # Left, Top, Right, Bottom
        if (n[0] - 1, n[1]) not in nodes:
            # s[(n[0] - 1, n[1])].append("B")
            s["B"].append((n[0] - 1, n[1]))
        if (n[0] + 1, n[1]) not in nodes:
            # s[(n[0] + 1, n[1])].append("T")
            s["T"].append((n[0] + 1, n[1]))
        if (n[0], n[1] - 1) not in nodes:
            # s[(n[0], n[1] - 1)].append("R")
            s["R"].append((n[0], n[1] - 1))
        if (n[0], n[1] + 1) not in nodes:
            # s[(n[0], n[1] + 1)].append("L")
            s["L"].append((n[0], n[1] + 1))

    num_sides = 0

    for i, dir in enumerate("BRTL"):
        # check either row or col idx (B,T) => row <idx 0>
        if len(s[dir]) == 1:
            num_sides += 1
            continue

        idx2check = i % 2
        # when top: key = row, val = columns on that row
        counted = defaultdict(list)
        for n in s[dir]:
            counted[n[idx2check]].append(n[idx2check - 1])

        for key in counted:
            arr = counted[key]
            num_sides += 1
            if len(arr) == 1:
                continue
            arr.sort()
            for c1, c2 in zip(arr, arr[1:]):
                if abs(c1 - c2) > 1:
                    num_sides += 1

    return num_sides


# 103ms
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True

    grid = data.copy()
    tot = 0
    G = remove_invalid_edges_ret_graph(grid)
    for garden in connected_components(G):
        tot += len(garden) * sides(garden)

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
