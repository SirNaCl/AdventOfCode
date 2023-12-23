from itertools import product
import pathlib
import re
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def create_range(a, b):
    return range(min(a, b), max(a, b) + 1)


def parse(puzzle_input):
    """Parse input."""
    coords = [
        list(map(int, re.findall(r"\d+", line))) for line in puzzle_input.split("\n")
    ]
    return {
        i: (
            product(create_range(c[0], c[3]), create_range(c[1], c[4])),
            create_range(c[2], c[5]),
        )
        for i, c in enumerate(coords)
    }


def part1(data: dict[int, tuple[product, range]]):
    """Solve part 1."""
    sorted_keys = sorted(data, key=lambda k: data[k][1].start)
    tops = {}  # (x,y): (block_key, height)
    block_coords = set()
    supported_by = [set() for _ in sorted_keys]
    supports = [set() for _ in sorted_keys]
    for k in sorted_keys:
        xy, z = data[k]
        xy = set(xy)
        zz = len(z)
        i = block_coords.intersection(xy)
        block_coords = block_coords.union(xy)
        zmax = 0
        if len(i) > 0:  # intersect
            sups = set()
            for ii in i:
                ik, iz = tops[ii]
                if iz == zmax:
                    sups.add(ik)
                elif iz > zmax:
                    zmax = iz
                    sups = {ik}

            supports[k] = sups
            for sk in sups:
                supported_by[sk].add(k)
        for xyxy in xy:
            tops[xyxy] = (k, zmax + zz)

    tot = 0
    for brick in sorted_keys:
        if len(supported_by[brick]) == 0 or all(
            [len(supports[b]) > 1 for b in supported_by[brick]]
        ):
            tot += 1

    return tot


def part2(data):
    """Solve part 2."""
    sorted_keys = sorted(data, key=lambda k: data[k][1].start)
    tops = {}  # (x,y): (block_key, height)
    block_coords = set()
    supported_by = [set() for _ in sorted_keys]
    supports = [set() for _ in sorted_keys]
    for k in sorted_keys:
        xy, z = data[k]
        xy = set(xy)
        zz = len(z)
        i = block_coords.intersection(xy)
        block_coords = block_coords.union(xy)
        zmax = 0
        if len(i) > 0:  # intersect
            sups = set()
            for ii in i:
                ik, iz = tops[ii]
                if iz == zmax:
                    sups.add(ik)
                elif iz > zmax:
                    zmax = iz
                    sups = {ik}

            supports[k] = sups
            for sk in sups:
                supported_by[sk].add(k)
        for xyxy in xy:
            tops[xyxy] = (k, zmax + zz)

    safe = []
    for brick in sorted_keys:
        if len(supported_by[brick]) == 0 or all(
            [len(supports[b]) > 1 for b in supported_by[brick]]
        ):
            safe.append(brick)
    tot = 0
    for brick in sorted_keys:
        brick = int(brick)
        falls = [brick]
        fallen = []
        while falls:
            b = falls.pop(0)
            for bb in supported_by[b]:
                if (bb not in falls and bb not in fallen) and all(
                    [sb == b or sb in falls or sb in fallen for sb in supports[bb]]
                ):
                    falls.append(bb)
                    tot += 1
            fallen.append(b)

    return tot


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
