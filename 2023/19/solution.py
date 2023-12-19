import pathlib
import re
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
class Part:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    @property
    def tot(self):
        return self.x + self.m + self.a + self.s


def parse(puzzle_input):
    """Parse input."""
    rules, parts = puzzle_input.split("\n\n")
    rmap = {}
    for line in rules.split():
        key, opts = line[:-1].split("{")
        opts = opts.split(",")
        rulelist = []
        for o in opts[:-1]:
            r, dst = o.split(":")
            rulelist.append((r[0], r[1], int(r[2:]), dst))
        rulelist.append(("default", "", 0, opts[-1]))
        rmap[key] = rulelist

    partlist = []
    for p in parts.split("\n"):
        nums = re.findall(r"\d+", p)
        partlist.append(Part(*nums))

    return rmap, partlist


def comp(a, op, b):
    if op == "<":
        return a < b
    else:
        return a > b


def process_rule(part: Part, rule: list[tuple[str, str, int, str]]):
    for r in rule[:-1]:
        pval = 0
        match r[0]:
            case "x":
                pval = part.x
            case "m":
                pval = part.m
            case "a":
                pval = part.a
            case "s":
                pval = part.s

        if comp(pval, r[1], r[2]):
            return r[3]

    return rule[-1][3]


def part1(data):
    """Solve part 1."""
    rules, parts = data
    tot = 0
    for part in parts:
        target = process_rule(part, rules["in"])
        while target not in ("A", "R"):
            target = process_rule(part, rules[target])

        if target == "A":
            tot += part.tot
    return tot


class RangedPart:
    def __init__(
        self, x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)
    ):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @property
    def tot(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


def process_range(part: RangedPart, rule: list[tuple[str, str, int, str]]):
    ret = []  # [(target, rangedpard)]
    for r in rule[:-1]:
        match r[0]:
            case "x":
                if r[2] in part.x:
                    if r[1] == "<":
                        new = RangedPart(
                            range(part.x.start, r[2]), part.m, part.a, part.s
                        )
                        ret.append((r[3], new))
                        part.x = range(r[2], part.x.stop)
                    else:
                        new = RangedPart(
                            range(r[2], part.x.stop), part.m, part.a, part.s
                        )
                        ret.append((r[3], new))
                        part.x = range(part.x.start, r[2])

            case "m":
                if r[2] in part.m:
                    if r[1] == "<":
                        new = RangedPart(
                            part.x, range(part.m.start, r[2]), part.a, part.s
                        )
                        ret.append((r[3], new))
                        part.m = range(r[2], part.m.stop)
                    else:
                        new = RangedPart(
                            part.x, range(r[2], part.m.stop), part.a, part.s
                        )
                        ret.append((r[3], new))
                        part.m = range(part.m.start, r[2])
            case "a":
                if r[2] in part.a:
                    if r[1] == "<":
                        new = RangedPart(
                            part.x, part.m, range(part.a.start, r[2]), part.s
                        )
                        ret.append((r[3], new))
                        part.a = range(r[2], part.a.stop)
                    else:
                        new = RangedPart(
                            part.x, part.m, range(r[2], part.a.stop), part.s
                        )
                        ret.append((r[3], new))
                        part.a = range(part.a.start, r[2])
            case "s":
                if r[2] in part.s:
                    if r[1] == "<":
                        new = RangedPart(
                            part.x, part.m, part.a, range(part.s.start, r[2])
                        )
                        ret.append((r[3], new))
                        part.s = range(r[2], part.s.stop)
                    else:
                        new = RangedPart(
                            part.x, part.m, part.a, range(r[2], part.s.stop)
                        )
                        ret.append((r[3], new))
                        part.s = range(part.s.start, r[2])

    if part.tot > 0:
        ret.append((rule[-1][3], part))

    return ret


def part2(data):
    """Solve part 2."""
    rules, _ = data

    tot = 0
    open_parts = [("in", RangedPart())]
    while open_parts:
        target, p = open_parts.pop()
        if target == "A":
            tot += p.tot
            continue
        if target == "R":
            continue

        open_parts += process_range(p, rules[target])

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
