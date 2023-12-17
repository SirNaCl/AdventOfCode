from functools import lru_cache
import pathlib
import bisect
from re import I
import pytest
import os
import numpy as np
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [list(row) for row in puzzle_input.split("\n")]


class Node:
    def __init__(self, row, col, parent, line_len, cost):
        self.parent = parent
        self.row = row
        self.col = col
        self.line_len = line_len
        if parent is None:
            self.next_on_line = (-1, -1)
            self.g = 0
        else:
            drow, dcol = self.row - self.parent.row, self.col - self.parent.col
            self.next_on_line = (self.row + drow, self.col + dcol)
            self.g = parent.g + cost

    @property
    def pos(self):
        return (self.row, self.col)

    def gen_successors(self, pattern, part2=False):
        if self.parent is None:
            exclude = set()
        else:
            exclude = set([self.parent.pos])

        cands = set(
            [
                (self.row - 1, self.col),
                (self.row, self.col - 1),
                (self.row, self.col + 1),
                (self.row + 1, self.col),
            ]
        )

        if not part2:
            if self.line_len == 3:
                exclude.add(self.next_on_line)
        else:
            if self.line_len < 4:
                cands = set([self.next_on_line])
            elif 10 <= self.line_len:
                exclude.add(self.next_on_line)

        res = []
        for cr, cc in cands - exclude:
            if 0 <= cr < len(pattern) and 0 <= cc < len(pattern[0]):
                res.append(
                    Node(
                        cr,
                        cc,
                        self,
                        (self.line_len + 1 if (cr, cc) == self.next_on_line else 1),
                        int(pattern[cr][cc]),
                    )
                )
        return res


def branch_bound(data, part2=False):
    goal = (len(data) - 1, len(data[1]) - 1)
    cache = set()
    n = Node(0, 0, None, 0, 0)
    nodes = [Node(1, 0, n, 1, int(data[1][0])), Node(0, 1, n, 1, int(data[0][1]))]
    while nodes:
        n = nodes.pop(0)
        if n.pos == goal and (not part2 or n.line_len > 3):
            return n.g
        if (n.pos, n.next_on_line, n.line_len) in cache:
            continue
        cache.add((n.pos, n.next_on_line, n.line_len))
        succ = n.gen_successors(data, part2)
        for s in succ:
            if not nodes:
                nodes.append(s)
            else:
                bisect.insort(nodes, s, key=lambda x: x.g)


def part1(data):
    """Solve part 1."""
    return branch_bound(data)


def part2(data):
    """Solve part 2."""
    return branch_bound(data, True)


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
