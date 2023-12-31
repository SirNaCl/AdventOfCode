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


def compress_ranges(r: list[range]):
    r.sort(key=lambda x: x.start)
    compressed = []
    skip = False
    for f, l in zip(r, r[1:]):
        if skip:
            skip = False
            continue
        if f.stop >= l.start:
            compressed.append(range(f.start, max(l.stop, f.stop)))
            skip = True
        else:
            compressed.append(f)

    if not skip:
        compressed.append(r[-1])
    return compressed


def map_ranges(rl: list[range], m: list[tuple[int, int, int]]) -> list[range]:
    done = []
    ran = rl.copy()
    i = 0
    while i < len(ran):
        r = ran[i]
        found = False
        for dst, src, lng in m:
            if r.start <= src < r.stop:
                # head
                if src - r.start > 0:
                    ran.append(range(r.start, src))
                # mid
                new_start = src + (dst - src)
                done.append(range(new_start, new_start + min(lng, r.stop - src)))
                # tail
                tail_start = src + lng
                if tail_start < r.stop:
                    ran.append(range(tail_start, r.stop))
                found = True
                break

            if src <= r.start < src + lng:
                # head
                # done.append(range(src, r.start))
                # mid
                new_start = r.start + (dst - src)
                done.append(
                    range(new_start, new_start + min(((src + lng) - r.start), len(r)))
                )
                # tail
                tail_start = src + lng
                if tail_start < r.stop:
                    ran.append(range(tail_start, r.stop))
                found = True
                break

        if not found:
            done.append(r)
        i += 1

    return compress_ranges(done)


def part2(data):
    """Solve part 2."""
    r = [range(s, s + l) for s, l in zip(data[0][0::2], data[0][1::2])]

    # for some reason this works
    for d in data[1:]:
        r = map_ranges(r, d)

    return r[0].start


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
    # assert pytest.main(PUZZLE_DIR) == 0
    ans = solve(puzzle.input_data)
    submit(puzzle, *ans)


if __name__ == "__main__":
    main()
