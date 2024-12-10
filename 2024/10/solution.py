from math import sqrt
import pathlib
from networkx import all_simple_paths, neighbors, shortest_path
import pytest
import os
from aocd.models import Puzzle
import sys
from os import path

PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import benchmark
from common.grid import GridInt, GRID_VALUE


PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    return GridInt(puzzle_input)


def remove_invalid_edges(G, data):
    invalid = set()
    for node, val in G.nodes(data=GRID_VALUE):
        for nrow, ncol in neighbors(G, node):
            if data[nrow][ncol] - val != 1:
                invalid.add((node, (nrow, ncol)))

    for edge in invalid:
        if G.has_edge(*edge):
            G.remove_edge(*edge)


# 94ms
@benchmark
def part1(data: GridInt):
    """Solve part 1."""
    tot = 0
    starts = data.find_all(0)
    ends = data.find_all(9)
    G = data.to_graph().to_directed()
    remove_invalid_edges(G, data)

    for s in starts:
        for e in ends:
            if sqrt((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2) > 10:
                # ignore impossible
                continue
            try:
                p = shortest_path(G, s, e)
            except:
                continue
            vals = [data[row][col] for row, col in p]
            if len(vals) == 10 and vals == sorted(vals):
                tot += 1

    return tot


# 445ms
@benchmark
def part2(data: GridInt):
    """Solve part 2."""
    global p2
    p2 = True

    tot = 0
    starts = data.find_all(0)
    ends = data.find_all(9)
    G = data.to_graph().to_directed()
    remove_invalid_edges(G, data)

    for s in starts:
        for e in ends:
            if sqrt((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2) > 10:
                # ignore impossible
                continue
            try:
                paths = all_simple_paths(G, s, e, 10)
            except:
                continue

            for p in paths:
                if len(p) != 10:
                    continue
                vals = [data[row][col] for row, col in p]

                if vals == sorted(vals):
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
