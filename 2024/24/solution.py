from collections import defaultdict
from collections.abc import Callable
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
class Rule():
    op: Callable
    a: str
    b: str
    


def OR(a, b):
    return a | b


def XOR(a, b):
    return a ^ b


def AND(a, b):
    return a & b

def get_op(s):
    match(s):
        case 'XOR':
            return XOR
        case 'AND':
            return AND
        case 'OR':
            return OR

    raise ValueError(f"invalid op {s}")

def parse(puzzle_input):
    """Parse input."""
    state = dict()
    st, ru = puzzle_input.split("\n\n")
    for s in st.split('\n'):
        k, v = s.split(": ")
        state[k] = int(v)


    rules = dict()
    for r in ru.split("\n"):
        rr = r.split(' ')
        a, o, b, _, k = rr
        op = get_op(o)
        rules[k] = Rule(op, a, b)

    return state, rules

def part1(data):
    """Solve part 1."""
    state, rules = data
    state = state.copy()
    zs = [key for key in rules if key.startswith('z')]

    def finished():
        return all(key in state for key in zs)

    while not finished():
        for k, r in rules.items():
            if r.a in state and r.b in state:
                state[k] = r.op(state[r.a], state[r.b])

    tot = ''
    for z in sorted(zs):
        tot = str(state[z]) + tot

    return int(tot, 2)
    


def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    state, rules = data
    state = state.copy()
    x = ''
    y = ''
    zs = [key for key in rules if key.startswith('z')]

    state_keys = state.keys()
    print(len(rules))

    for k in sorted(state_keys):
        if k.startswith('x'):
            x = str(state[k]) + x
        elif k.startswith('y'):
            y = str(state[k]) + y

    x = int(x, 2)
    y = int(y, 2)
    target = x + y

    def finished():
        return all(key in state for key in zs)

    while not finished():
        for k, r in rules.items():
            if r.a in state and r.b in state:
                state[k] = r.op(state[r.a], state[r.b])

    actual = ''
    for z in sorted(zs):
        actual = str(state[z]) + actual

    actual = int(actual, 2)
    incorrect = target ^ actual
    inval_nodes = []
    val_nodes = []
    for i, b in enumerate(reversed(bin(incorrect)[2:])):
        if b == '1':
            inval_nodes.append('z' + str(i).zfill(2))
        else:
            val_nodes.append('z' + str(i).zfill(2))


    G = nx.DiGraph()
    for k,v in rules.items():
        G.add_edge(v.a, k)
        G.add_edge(v.b, k)

    sanc = set()
    anc = defaultdict(list)
    for n in inval_nodes:
        for a in nx.ancestors(G, n):
            if re.match(r"[y|x]\d+", a) is None:
                anc[n].append(a)
                sanc.add(a)

    sancval = set()
    for n in val_nodes:
        for a in nx.ancestors(G, n):
            if re.match(r"[y|x]\d+", a) is None:
                sancval.add(a)

    # pprint(anc)
    # pprint(anc_val)
    only_inv = sanc.difference(sancval)    
    only_val = sancval.difference(sanc)    
    print(inval_nodes)
    print(f"{len(only_inv)=} {len(only_val)=}")
    print(bin(actual))
    print(bin(target))
    print('0b' + bin(incorrect)[2:].zfill(46))
    for v in anc.values():
        for s in sancval:
            if s in v:
                v.remove(s)





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
