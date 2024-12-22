import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import functools
from collections import defaultdict

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
    return map(int, puzzle_input.split("\n"))


def prune(secret):
    return secret % 16777216


def mix(secret, factor):
    return prune(secret ^ factor)


@functools.cache
def evolve(secret):
    secret = mix(secret, secret * 64)
    secret = mix(secret, secret // 32)
    secret = mix(secret, secret * 2048)
    return secret


def evolvefull(secret):
    return functools.reduce(lambda s, _: evolve(s), range(2000), secret)


# 2351ms
@benchmark
def part1(data):
    """Solve part 1."""
    return sum(map(evolvefull, data))


BANANAS = defaultdict(int)


def digit(v):
    return v % 10


def gen_prices(secret):
    fifo = [None] * 4
    prev = digit(secret)

    # Dict with the signal sequence as key and the resulting amount of bananas as value
    earned = set()

    def insert(e):
        fifo.pop()
        fifo.insert(0, e)

    for _ in range(2000):
        secret = evolve(secret)
        dig = digit(secret)
        delta = dig - prev
        insert(delta)
        if None not in fifo and (k := tuple(fifo)) not in earned:
            earned.add(k)
            BANANAS[k] += dig

        prev = dig


# 3634ms
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    for secret in data:
        gen_prices(secret)

    return max(BANANAS.values())


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read().strip()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(parse(puzzle_input))
    solution2 = part2(parse(puzzle_input))

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
