from functools import cmp_to_key
import pathlib
from typing import Counter
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input: str):
    """Parse input."""
    p = puzzle_input.split("\n")

    return [g.split(" ") for g in p]


def handle_jokers(h: list):
    hc = Counter(h)
    mc = hc.most_common()[0][0]

    if mc == 0:
        if hc.get(0) == 5:
            return h
        mc = hc.most_common()[1][0]

    return [v if v != 0 else mc for v in h]


def comp(c1: list, c2: list, part2=False):
    t1 = handle_jokers(c1) if part2 else c1
    t2 = handle_jokers(c2) if part2 else c2
    v1 = Counter(t1).most_common()
    v2 = Counter(t2).most_common()

    # more of most common
    if v1[0][1] > v2[0][1]:
        return 1

    if v1[0][1] < v2[0][1]:
        return -1

    if v1[0][1] == v2[0][1]:
        # house for first
        if v1[0][1] == 3 and v1[1][1] == 2:
            # Both house
            if v2[0][1] == 3 and v2[1][1] == 2:
                for cc1, cc2 in zip(c1, c2):
                    if cc1 > cc2:
                        return 1
                    if cc1 < cc2:
                        return -1

            return 0

        # house second
        if v2[0][1] == 3 and v2[1][1] == 2:
            return -1

        # two pair
        if v1[0][1] == 2 and v1[1][1] == 2:
            if v2[0][1] == 2 and v2[1][1] == 2:
                for cc1, cc2 in zip(c1, c2):
                    if cc1 > cc2:
                        return 1
                    if cc1 < cc2:
                        return -1
            return 1

        if v2[0][1] == 2 and v2[1][1] == 2:
            return -1

        for cc1, cc2 in zip(c1, c2):
            if cc1 > cc2:
                return 1
            if cc1 < cc2:
                return -1

    return 0


class Hand:
    def __init__(self, c, b, part2=False):
        self.c = c
        self.b = b
        self.part2 = part2

    def __lt__(self, other):
        return comp(self.c, other.c, self.part2) == -1

    def __str__(self):
        return f"{self.c}: {self.b}"


def part1(data: list[list[str]]):
    """Solve part 1."""
    counters = []  # card counter, bet
    # cards, bet
    for hand in data:
        # todo map letters to n
        cards = [v for v in hand[0]]
        cca = []
        for cc in cards:
            if cc == "T":
                cca.append(10)
            elif cc == "J":
                cca.append(0)
            elif cc == "Q":
                cca.append(12)
            elif cc == "K":
                cca.append(13)
            elif cc == "A":
                cca.append(14)
            else:
                cca.append(int(cc))

        counters.append(Hand(cca, hand[1]))
    cs = sorted(counters, reverse=True)
    rank = len(counters)
    tot = 0
    for c in cs:
        tot += int(c.b) * rank
        rank -= 1
    return tot


def part2(data):
    """Solve part 2."""
    counters = []  # card counter, bet
    # cards, bet
    for hand in data:
        # todo map letters to n
        cards = [v for v in hand[0]]
        cca = []
        for cc in cards:
            if cc == "T":
                cca.append(10)
            elif cc == "J":
                cca.append(0)
            elif cc == "Q":
                cca.append(12)
            elif cc == "K":
                cca.append(13)
            elif cc == "A":
                cca.append(14)
            else:
                cca.append(int(cc))

        counters.append(Hand(cca, hand[1], True))
    cs = sorted(counters, reverse=True)
    rank = len(counters)
    tot = 0
    for c in cs:
        tot += int(c.b) * rank
        rank -= 1
    return tot


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
