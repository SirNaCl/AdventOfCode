import pathlib
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    s = puzzle_input.split("\n\n")
    s = [ss.split("\n") for ss in s]
    o = [[int(i) for i in e.split("|")] for e in s[0]]
    od = {}
    for a, b in o:
        if a not in od:
            od[a] = []
        od[a].append(b)

    return od, [[int(i) for i in e.split(",")] for e in s[1]]


def part1(data):
    """Solve part 1."""
    tot = 0
    order, updates = data
    for u in updates:
        invalid = False
        for i, uu in enumerate(u):
            if uu not in order:
                continue

            if any([o in u and u.index(o) < i for o in order[uu]]):
                invalid = True
                break

        if not invalid:
            tot += u[int(len(u) / 2)]

    return tot


def part2(data):
    """Solve part 2."""
    tot = 0
    order, updates = data

    for u in updates:
        invalid = True
        sor: list[int] = u.copy()
        tmp = sor.copy()
        while invalid:
            updated = False
            for s in sor[::-1]:
                if s not in order:
                    continue

                for oo in order[s]:
                    if oo not in sor:
                        continue

                    si = tmp.index(s)
                    oi = tmp.index(oo)
                    if si < oi:
                        continue

                    tmp.pop(si)
                    tmp.insert(oi, s)
                    updated = True

            invalid = updated
            sor = tmp.copy()

        if u != sor:
            tot += sor[int(len(sor) / 2)]

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
