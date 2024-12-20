import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
from collections import Counter

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
    regs, prog = puzzle_input.split("\n\n")
    dregs = dict()
    for line in regs.split("\n"):
        i = line.find(" ")
        l = line[i:]
        key, value = l.split(": ")
        dregs[key.strip()] = int(value)

    return dregs, list(map(int, [j for j in prog.split(": ")[1].split(",")]))


REGS = {}
PROG = []
I_PTR = 0
STDOUT = []


def get_comb() -> int:
    if I_PTR + 1 == len(PROG):
        raise StopIteration("SIGTERM")
    combo = PROG[I_PTR + 1]
    match (combo):
        case 0:
            return 0
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return REGS["A"]
        case 5:
            return REGS["B"]
        case 6:
            return REGS["C"]
        case 7:
            raise RuntimeError("INVALID COMBO OPERATOR 7!")
    return -1


def adv():
    global I_PTR
    num = REGS["A"]
    den = 2 ** get_comb()
    REGS["A"] = num // den
    I_PTR += 2


def bxl():
    global I_PTR
    REGS["B"] = REGS["B"] ^ PROG[I_PTR + 1]
    I_PTR += 2


def bst():
    global I_PTR
    REGS["B"] = get_comb() % 8
    I_PTR += 2


def jnz():
    global I_PTR
    if REGS["A"] == 0:
        I_PTR += 2
        return

    I_PTR = PROG[I_PTR + 1]


def bxc():
    global I_PTR
    REGS["B"] = REGS["B"] ^ REGS["C"]
    I_PTR += 2


def out():
    global I_PTR
    c = get_comb() % 8
    STDOUT.append(c)
    I_PTR += 2


def bdv():
    global I_PTR
    num = REGS["A"]
    den = 2 ** get_comb()
    REGS["B"] = int(num / den)
    I_PTR += 2


def cdv():
    global I_PTR
    num = REGS["A"]
    den = 2 ** get_comb()
    REGS["C"] = int(num / den)
    I_PTR += 2


OPS = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def step():
    OPS[PROG[I_PTR]]()


# 0.15ms
@benchmark
def part1(data):
    """Solve part 1."""
    global REGS
    global PROG
    regs, prog = data
    REGS = regs
    PROG = prog

    while I_PTR < len(prog):
        try:
            step()
        except:
            return ",".join(map(str, STDOUT))

    return ",".join(map(str, STDOUT))


def do_iter(A: int):
    global REGS
    global I_PTR

    I_PTR = 0
    REGS["A"] = A
    REGS["B"] = 0
    REGS["C"] = 0

    while I_PTR <= 12:
        step()


# iter: bst, bxl, cdv, bxl, adv, bxc -> print B
def get_canditates(a_targs: list[int], out: int):
    # a_targs: Possible finishes for A, out: the value we want printed out (reg b)
    cands = []
    for a in a_targs:
        a_max = (a + 1) * 8
        c = range(a_max - 8, a_max + 1)
        for A in c:
            do_iter(A)
            if REGS["B"] % 8 == out:
                cands.append(A)
    return cands


# 2.7ms
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    global REGS
    global PROG

    p2 = True
    regs, prog = data
    REGS = regs
    PROG = prog
    targ_prev = [0]
    for op in reversed(prog):
        targ = get_canditates(targ_prev, op)
        targ_prev = targ

    return targ_prev[0]


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
