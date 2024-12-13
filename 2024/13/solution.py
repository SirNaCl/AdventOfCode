import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import re
import sympy as sp
from sympy.solvers import solve as spsolve

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import benchmark

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False

PATTERN = r"[.]*([-]?[\d]+)[^\d]+([-]?[\d]+)"


class Game:
    def __init__(self, a: tuple[int, int], b: tuple[int, int], target: tuple[int, int]):
        self.a = a
        self.b = b
        self.target = target

    def __repr__(self):
        return f"{self.a=} {self.b=} {self.target=}"


def parse(puzzle_input):
    """Parse input."""
    games = []
    for g in puzzle_input.split("\n\n"):
        nums = []
        for line in g.split("\n"):
            n = [int(i) for i in re.findall(PATTERN, line)[0]]
            nums.append(n)
        games.append(Game(*nums))
    return games


A_COST = 3
B_COST = 1


def solve_game(game: Game) -> int:
    MAX_PRESSES = 100 if not p2 else 1000000000000000000000000000000
    if p2:
        game.target = (
            game.target[0] + 10000000000000,
            game.target[1] + 10000000000000,
        )
    sp.var("b_press a_press")
    eqX = sp.Eq(b_press * game.b[0] + a_press * game.a[0], game.target[0])
    eqY = sp.Eq(b_press * game.b[1] + a_press * game.a[1], game.target[1])
    output = spsolve([eqX, eqY], b_press, a_press, dict=True)

    solutions = []
    for o in output:
        a = o[a_press]
        b = o[b_press]
        if int(a) != a or a < 0 or a > MAX_PRESSES:
            continue
        if int(b) != b or b < 0 or b > MAX_PRESSES:
            continue

        solutions.append(int(a) * A_COST + int(b) * B_COST)
    if len(solutions) == 0:
        return 0
    return min(solutions)


# 1550ms
@benchmark
def part1(data):
    """Solve part 1."""
    return sum([solve_game(game) for game in data])


# 1570ms
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    return sum([solve_game(game) for game in data])


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
