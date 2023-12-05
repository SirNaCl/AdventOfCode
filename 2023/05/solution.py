from functools import lru_cache
from operator import is_
import pathlib
from webbrowser import get
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    i = [l for l in puzzle_input.split("\n") if len(l) > 0]
    seeds = [int(s) for s in i[0].split("seeds: ")[1].split(" ")]
    parsed = [seeds]
    section = list()
    for row in i[1:]:
        if row[0].isdigit():
            section.append([int(n) for n in row.split(" ")])
        elif len(section) > 0:
            parsed.append(section)
            section = []

    parsed.append(section)
    return parsed


def pick_from_map(seed, data):
    picked = seed
    for soil in data:
        if soil[1] <= seed <= soil[1] + soil[2]:
            return soil[0] + (seed - soil[1])
    return picked


def part1(data):
    """Solve part 1."""
    locations = []
    for seed in data[0]:
        picked = pick_from_map(seed, data[1])
        picked = pick_from_map(picked, data[2])
        picked = pick_from_map(picked, data[3])
        picked = pick_from_map(picked, data[4])
        picked = pick_from_map(picked, data[5])
        picked = pick_from_map(picked, data[6])
        picked = pick_from_map(picked, data[7])
        locations.append(picked)

    return min(locations)


def translate_range(ran: list[int], map):
    out = ran.copy()
    for m in map:
        for i, mv in enumerate(range(m[1], m[1] + m[2])):
            try:
                idx = ran.index(mv)
                out[idx] = m[0] + i
                print(f"{idx} => {m[0]+i}")
            except:
                pass
    return out


def part2(data):
    """Solve part 2."""
    rangeloc = []
    locations = []
    seedr = list()
    for i, (s, l) in enumerate(zip(data[0], data[0][1:])):
        if i % 2 == 0:
            seedr.append((s, l))

    for rs, rl in seedr:
        r = list(range(rs, rs + rl))
        print(r)
        r = translate_range(r, data[1])
        print(r)
        r = translate_range(r, data[2])
        print(r)
        r = translate_range(r, data[3])
        print(r)
        r = translate_range(r, data[4])
        r = translate_range(r, data[4])
        r = translate_range(r, data[5])
        r = translate_range(r, data[6])
        r = translate_range(r, data[7])

        locations.append(min(r))
    return min(locations)


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
