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
    p = []
    for l in puzzle_input.split("\n"):
        a, b = l.split(": ")
        p.append((int(a), [int(bb) for bb in b.split(" ")]))

    return p


def do_op(a, b, op):
    match op:
        case 0:
            return a + b
        case 1:
            return a * b
        case 2:
            return int(str(a) + str(b))


def has_sol(target, row, concat=False):
    operands = row.copy()
    operands[0] = [operands[0]]

    while len(operands) > 1:
        a_list = operands.pop(0)
        b = operands.pop(0)
        pair_res = [
            do_op(a, b, op) for op in range(2 if not concat else 3) for a in a_list
        ]
        operands.insert(0, pair_res)

    return target in operands[0]


def part1(data):
    """Solve part 1."""
    tot = 0

    for target, row in data:
        if has_sol(target, row):
            tot += target
    return tot


def part2(data):
    """Solve part 2."""
    tot = 0

    for target, row in data:
        if has_sol(target, row, True):
            tot += target

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
