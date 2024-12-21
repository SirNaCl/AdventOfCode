import pathlib
from typing import Callable
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
from itertools import permutations, product
from functools import cache

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
    return puzzle_input.split("\n")


def pos(btn):
    match (btn):
        case "7":
            return 0, 0
        case "8":
            return 0, 1
        case "9":
            return 0, 2
        case "4":
            return 1, 0
        case "5":
            return 1, 1
        case "6":
            return 1, 2
        case "1":
            return 2, 0
        case "2":
            return 2, 1
        case "3":
            return 2, 2
        case "0":
            return 3, 1
        case "A":
            return 3, 2
        case None:
            return 3, 0

    raise ValueError()


def rob_pos(btn):
    match (btn):
        case "A":
            return 0, 2
        case "^":
            return 0, 1
        case "<":
            return 1, 0
        case "v":
            return 1, 1
        case ">":
            return 1, 2
        case None:
            return 0, 0

    raise ValueError()


def crosses_empty(path: str, start: str, pos_func: Callable):
    AVOID = pos_func(None)
    r, c = pos_func(start)
    path = path.replace("A", "")
    move = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0),
    }

    for p in path:
        dr, dc = move[p]
        r += dr
        c += dc
        if (r, c) == AVOID:
            return True

    return False


def find_paths(seq: str, start: str, pos_func: Callable):
    pr, pc = pos_func(start)
    moves = []
    for char in seq:
        m = []
        cr, cc = pos_func(char)
        dr = cr - pr
        dc = cc - pc
        if dr < 0:
            m.extend(["^"] * -dr)
        elif dr > 0:
            m.extend(["v"] * dr)

        if dc < 0:
            m.extend(["<"] * -dc)
        elif dc > 0:
            m.extend([">"] * dc)

        mm = []
        for perm in set(["".join(p) for p in permutations(m)]):
            mm.append(perm + "A")

        moves.append(mm)
        pr, pc = cr, cc

    paths = ("".join(p) for p in product(*moves))
    return [path for path in paths if not crosses_empty(path, start, pos_func)]


walks = dict()


# 95000ms xD
@benchmark
def part1_slow(data):
    """Solve part 1."""
    tot = 0

    for line in data:
        seq_list = find_paths(line, "A", pos)

        for _ in range(2):
            possible = []
            for s in seq_list:
                possible.extend(find_paths(s, "A", rob_pos))

            minl = min(map(len, possible))
            seq_list = [s for s in possible if len(s) == minl]

        tot += int(line[:-1]) * len(seq_list[0])

    return tot

walks = {
    (start, end): find_paths(end, start, rob_pos)
    for start in "<>v^A"
    for end in "<>v^A"
}

@cache
def calc_cost_old(path, iters) -> int:
    if iters == 0:
        return len(path)

    cost = 0
    for p1, p2 in zip("A" + path, path):
        cost += min(calc_cost(p, iters - 1) for p in walks[p1, p2])

    return int(cost)


@cache
def calc_cost(c1, c2, iters) -> int:
    if iters == 1:
        return min(map(len, walks[c1, c2]))

    cost = min(
        [
            sum([calc_cost(cc1, cc2, iters - 1) for cc1, cc2 in zip("A" + path, path)])
            for path in walks[c1, c2]
        ]
    )

    return cost


# 2ms xD
# 0.35ms (pre-compute walks)
# 0.2ms (chars instead of full strings to calc_cost)
@benchmark
def part1(data):
    """Solve part 1."""
    tot = 0

    # Old calc_cost:
    # for line in data:
    #     cost = min(calc_cost(path, 2) for path in find_paths(line, pos))
    #     tot += int(line[:-1]) * cost

    for line in data:
        cost = min(
            [
                sum([calc_cost(c1, c2, 2) for c1, c2 in zip("A" + path, path)])
                for path in find_paths(line, "A", pos)
            ]
        )

        tot += int(line[:-1]) * cost

    return tot


# 4.5ms
# 0.85ms (pre-compute walks)
# 0.7ms (chars instead of full strings to calc_cost)
@benchmark
def part2(data):
    """Solve part 2."""
    tot = 0

    # Old calc_cost:
    # for line in data:
    #     cost = min(calc_cost(path, 25) for path in find_paths(line, pos))
    #     tot += int(line[:-1]) * cost

    for line in data:
        cost = min(
            [
                sum([calc_cost(c1, c2, 25) for c1, c2 in zip("A" + path, path)])
                for path in find_paths(line, "A", pos)
            ]
        )

        tot += int(line[:-1]) * cost
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
