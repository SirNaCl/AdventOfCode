from collections import defaultdict
from math import sqrt
import pathlib
from time import perf_counter_ns
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####

rmax = 0
cmax = 0
p2 = False


def parse(puzzle_input):
    """Parse input."""
    global rmax
    global cmax

    lines = puzzle_input.split("\n")
    rmax = len(lines) - 1
    cmax = len(lines[0]) - 1
    p = defaultdict(set)

    for ri, row in enumerate(lines):
        for ci, col in enumerate(row):
            if col in ".":
                continue
            p[col].add((ri, ci))
    return p


def dist(p1, p2):
    return sqrt(sum([abs(n1 - n2) ** 2 for n1, n2 in zip(p1, p2)]))


def find_antinodes(nodes: set[tuple[int, int]]):
    if len(nodes) == 1:
        return set()

    antinodes = set() if not p2 else nodes.copy()

    for r1, c1 in nodes:
        for r2, c2 in nodes:
            if (r1, c1) == (r2, c2):
                continue

            dr = r2 - r1
            dc = c2 - c1
            rn, cn = r1 - dr, c1 - dc

            while 0 <= rn <= rmax and 0 <= cn <= cmax:
                antinodes.add((rn, cn))
                if not p2:
                    break

                rn -= dr
                cn -= dc

    return antinodes


def part1(data: dict[str, set[tuple[int, int]]]):
    """Solve part 1."""
    antinodes = set()
    for coords in data.values():
        antinodes = antinodes.union(find_antinodes(coords))

    return len(antinodes)


def part2(data):
    """Solve part 2."""
    global p2

    p2 = True
    antinodes = set()

    for a in (find_antinodes(d) for d in data.values()):
        antinodes = antinodes.union(a)

    return len(antinodes)


#### UTILITY FUNCTIONS ####
def timed(f, *args):
    t1 = perf_counter_ns()
    res = f(*args)
    t2 = perf_counter_ns()
    print(f"{f.__name__} took {(t2-t1)/1000000}ms")
    return res


def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read().strip()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = timed(part1, data)
    solution2 = timed(part2, data)

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
