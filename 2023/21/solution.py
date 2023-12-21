from functools import lru_cache
import pathlib
import sys
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [list(line) for line in puzzle_input.split("\n")]


def part1(data, example=False):
    """Solve part 1."""
    steps = 6 if example else 64
    s = None
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == "S":
                s = (i, j)
                break
        if s is not None:
            break

    assert s is not None

    cache = {}  # (coord): [(coords)]
    queue = set([s])
    queuenext = set()
    for i in range(steps):
        while queue:
            p = queue.pop()
            if p not in cache:
                cache[p] = []
                pr, pc = p
                try:
                    if data[pr - 1][pc] != "#":
                        cache[p].append((pr - 1, pc))
                except:
                    pass
                try:
                    if data[pr][pc - 1] != "#":
                        cache[p].append((pr, pc - 1))
                except:
                    pass
                try:
                    if data[pr][pc + 1] != "#":
                        cache[p].append((pr, pc + 1))
                except:
                    pass
                try:
                    if data[pr + 1][pc] != "#":
                        cache[p].append((pr + 1, pc))
                except:
                    pass

            queuenext = queuenext.union(set(cache[p]))
        queue = queuenext.copy()
        queuenext = set()

    return len(queue)


def part2(data, example=False):
    """Solve part 2."""
    steps = 1000 if example else 26501365
    s = None
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == "S":
                s = (i, j)
                break
        if s is not None:
            break

    assert s is not None

    queue = set([s])
    queuenext = set()
    odd = set()
    even = set()
    for i in range(steps):
        modalitynext = odd if i % 2 == 0 else even
        while queue:
            p = queue.pop()
            pr, pc = p
            nr, nc = (pr - 1) % len(data), pc % len(data[1])
            if data[nr][nc] != "#" and (pr - 1, pc) not in modalitynext:
                modalitynext.add((pr - 1, pc))
                queuenext.add((pr - 1, pc))
            nr = (pr + 1) % len(data)
            if data[nr][nc] != "#" and (pr + 1, pc) not in modalitynext:
                modalitynext.add((pr + 1, pc))
                queuenext.add((pr + 1, pc))
            nr, nc = pr % len(data), (pc - 1) % len(data[0])
            if data[nr][nc] != "#" and (pr, pc - 1) not in modalitynext:
                modalitynext.add((pr, pc - 1))
                queuenext.add((pr, pc - 1))
            nc = (pc + 1) % len(data[0])
            if data[nr][nc] != "#" and (pr, pc + 1) not in modalitynext:
                modalitynext.add((pr, pc + 1))
                queuenext.add((pr, pc + 1))

        queue = queuenext.copy()
        queuenext = set()

    return len(even if steps % 2 == 0 else odd)


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
