from functools import lru_cache
import pathlib
import bisect
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


def manhattan(a: tuple[int, int], b: tuple[int, int]):
    ar, ac = a
    br, bc = b
    return abs(ar - br) + abs(ac - bc)


pattern = [[]]
goal = (0, 0)
lopen = []
lclosed = []
end_node = None
bound = 0


class Node:
    def __init__(self, row, col, parent, line_len):
        global end_node
        if (row, col) == goal:
            end_node = self
        self.parent = parent
        self.row = row
        self.col = col
        self.line_len = line_len
        if parent is None:
            self.next_on_line = (-1, -1)
            self.g = 0
            self.f = 0
        else:
            drow, dcol = self.row - self.parent.row, self.col - self.parent.col
            self.next_on_line = (self.row + drow, self.col + dcol)
            self.g = parent.g + int(pattern[row][col])
            self.dist_to_goal = manhattan((row, col), goal)
            self.f = self.g + self.dist_to_goal

    @property
    def pos(self):
        return (self.row, self.col)

    def gen_bound(self):
        if self.parent is None:
            exclude = set()
        else:
            exclude = set([self.parent.pos])

        if self.line_len == 3:
            exclude.add(self.next_on_line)

        cands = set(
            [
                (self.row - 1, self.col),
                (self.row, self.col - 1),
                (self.row, self.col + 1),
                (self.row + 1, self.col),
            ]
        )
        for cr, cc in cands - exclude:
            if 0 <= cr < len(pattern) and 0 <= cc < len(pattern[0]):
                n = Node(
                    cr,
                    cc,
                    self,
                    (self.line_len + 1 if (cr, cc) == self.next_on_line else 1),
                )
                skip = False
                for no in lopen:
                    if (
                        no.pos == n.pos
                        # and no.next_on_line == n.next_on_line
                        # and no.line_len == n.line_len
                        and no.f < n.f
                    ):
                        skip = True
                        break
                if skip:
                    continue
                for nc in lclosed:
                    if (
                        nc.pos == n.pos
                        # and nc.next_on_line == n.next_on_line
                        # and nc.line_len == n.line_len
                        and nc.f < n.f
                    ):
                        skip = True
                        break
                if not skip:
                    lopen.append(n)

    def gen_successors(self):
        if self.parent is None:
            exclude = set()
        else:
            exclude = set([self.parent.pos])

        if self.line_len == 3:
            exclude.add(self.next_on_line)

        cands = set(
            [
                (self.row - 1, self.col),
                (self.row, self.col - 1),
                (self.row, self.col + 1),
                (self.row + 1, self.col),
            ]
        )
        for cr, cc in cands - exclude:
            if 0 <= cr < len(pattern) and 0 <= cc < len(pattern[0]):
                n = Node(
                    cr,
                    cc,
                    self,
                    (self.line_len + 1 if (cr, cc) == self.next_on_line else 1),
                )

                if n.f > bound:
                    continue

                skip = False
                for no in lopen:
                    if (
                        no.pos == n.pos
                        and no.next_on_line == n.next_on_line
                        and no.line_len == n.line_len
                        and no.f < n.f
                    ):
                        skip = True
                        break
                if skip:
                    continue
                for nc in lclosed:
                    if (
                        nc.pos == n.pos
                        and nc.next_on_line == n.next_on_line
                        and nc.line_len == n.line_len
                        and nc.f < n.f
                    ):
                        skip = True
                        break
                if not skip:
                    lopen.append(n)


# @lru_cache
# def find_shortest(pos, prev, ll):
#     if pos == goal:


def part1(data):
    global pattern
    global goal
    global lopen
    global lclosed
    global end_node
    global bound
    pattern = data
    goal = (len(pattern) - 1, len(pattern[1]) - 1)
    """Solve part 1."""
    lopen = [Node(0, 0, None, 0)]
    lclosed = []
    while len(lopen) > 0 and end_node is None:
        lopen.sort(key=lambda n: n.f)
        q = lopen.pop(0)
        q.gen_bound()
        lclosed.append(q)

    if end_node is None:
        return -1

    bound = end_node.f
    end_node = None
    lopen = [Node(0, 0, None, 0)]
    lclosed = []
    while len(lopen) > 0 and end_node is None:
        lopen.sort(key=lambda n: n.f)
        q = lopen.pop(0)
        q.gen_successors()
        lclosed.append(q)

    if end_node is None:
        return -1

    return end_node.f


def part2(data):
    """Solve part 2."""


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
