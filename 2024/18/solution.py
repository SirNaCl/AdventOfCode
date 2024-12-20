import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import re
import networkx as nx

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


ROWS = 0
COLS = 0
BYTE_LIMIT = 1024


def parse(puzzle_input, rows=71, cols=71, p2=p2):
    """Parse input."""
    global ROWS
    global COLS
    ROWS = rows
    COLS = cols
    rl = []
    for _ in range(rows):
        rl.append("." * (cols))

    empty = "\n".join(rl)
    G = GridChar(empty)
    if not p2:
        for i, line in enumerate(puzzle_input.split("\n")):
            if i == BYTE_LIMIT:
                break
            c, r = tuple(map(int, re.findall(r"\d+", line)))
            G[r][c] = "#"
        return G
    else:
        b = []
        for i, line in enumerate(puzzle_input.split("\n")):
            b.append(tuple(map(int, re.findall(r"\d+", line))))
        return G, b


def part1(data):
    """Solve part 1."""
    g: GridChar = data
    p = g.shortest_path((0, 0), (ROWS - 1, COLS - 1), ignore=["#"])
    return len(p) - 1


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True

    g: GridChar = data[0]
    # Tuples are in format (X, Y)
    b: list[tuple[int, int]] = data[1]

    high = len(b)
    low = 0
    largest_working = 0
    while True:
        if high < low:
            break

        gg = g.copy()
        mid = (high + low) // 2
        for x, y in b[: mid + 1]:
            gg[y][x] = "#"
        try:
            gg.shortest_path((0, 0), (ROWS - 1, COLS - 1), ignore=["#"])
            if mid > largest_working:
                largest_working = mid
            else:
                break
            low = mid + 1
        except nx.NetworkXNoPath:
            high = mid - 1
    
    return "{},{}".format(*b[largest_working+1])

#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read().strip()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    solution2 = part2(parse(puzzle_input, p2=True))

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
