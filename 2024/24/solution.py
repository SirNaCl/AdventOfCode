from collections import defaultdict
from collections.abc import Callable
from itertools import combinations, pairwise, permutations
import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
from dataclasses import dataclass
import networkx as nx
import re

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


@dataclass
class Rule:
    op: Callable
    a: str
    b: str

    def __repr__(self) -> str:
        return f"{self.a} {self.op.__name__} {self.b}"


def OR(a, b):
    return a | b


def XOR(a, b):
    return a ^ b


def AND(a, b):
    return a & b


def get_op(s):
    match (s):
        case "XOR":
            return XOR
        case "AND":
            return AND
        case "OR":
            return OR

    raise ValueError(f"invalid op {s}")


def parse(puzzle_input):
    """Parse input."""
    state = dict()
    st, ru = puzzle_input.split("\n\n")
    for s in st.split("\n"):
        k, v = s.split(": ")
        state[k] = int(v)

    rules = dict()
    for r in ru.split("\n"):
        rr = r.split(" ")
        a, o, b, _, k = rr
        op = get_op(o)
        rules[k] = Rule(op, a, b)

    return state, rules


def resolve(state, rules):
    _state = state.copy()

    def finished():
        return all(key in _state for key in rules)

    i = 0
    while not finished():
        for k, r in rules.items():
            if r.a in _state and r.b in _state:
                _state[k] = r.op(_state[r.a], _state[r.b])
        i += 1
        if i == 1000:
            raise RuntimeError("Inf")

    return _state


def part1(data):
    """Solve part 1."""
    _, rules = data

    zs = [key for key in rules if key.startswith("z")]
    state = resolve(*data)

    tot = ""
    for z in sorted(zs):
        tot = str(state[z]) + tot

    return int(tot, 2)


def ancestors(rules, node: str):
    anc: list[str] = []
    queue: list[str] = [node]

    while len(queue) > 0:
        n = queue.pop(0)
        anc.insert(0, n)
        if n in rules:
            queue.append(rules[n].a)
            queue.append(rules[n].b)

    return anc


def to_node(prefix: str, num: int):
    return prefix + str(num).zfill(2)


def find_invalid(state):
    x = ""
    y = ""
    z = ""

    for k in sorted(state.keys()):
        if k.startswith("x"):
            x = str(state[k]) + x
        elif k.startswith("y"):
            y = str(state[k]) + y
        elif k.startswith("z"):
            z = str(state[k]) + z

    x = int(x, 2)
    y = int(y, 2)
    target = x + y
    z = int(z, 2)
    incorrect = target ^ z

    # z nodes with incorrect state
    inval_nodes: list[int] = []
    for i, b in enumerate(reversed(bin(incorrect)[2:])):
        if b == "1":
            inval_nodes.append(i)
    return inval_nodes


def print_anc(rules, k, valid):
    s = set(ancestors(rules, to_node("z", k))).difference(
        set(ancestors(rules, to_node("z", k - 1)))
    )
    print(f'====={to_node("z", k)}====({"valid" if valid else "invalid"})')
    for ss in s:
        if ss in rules:
            print(f"{ss} = {rules[ss]}")

    print("============")


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    state_start, rules = data
    # Solution was found by manually inspecting the invalid nodes and inserting swaps into list below
    swaps = []

    l = []
    for s in swaps:
        l += list(s)

    for a, b in swaps:
        rules[a], rules[b] = rules[b], rules[a]

    state = resolve(state_start, rules)
    inval_nodes = find_invalid(state)
    print(inval_nodes)

    for k in inval_nodes:
        if k - 1 not in inval_nodes:
            print_anc(rules, k - 1, True)
        print_anc(rules, k, False)


    r = ",".join(sorted(l))
    print(r)


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
