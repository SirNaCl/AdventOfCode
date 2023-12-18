from itertools import product
import pathlib
import numpy as np
import pytest
import os
from aocd.models import Puzzle
from matplotlib.path import Path

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [
        (row.split()[0], int(row.split()[1]), row.split()[2])
        for row in puzzle_input.split("\n")
    ]


def part1(data):
    """Solve part 1."""
    pos = [0, 0]
    points = [tuple(pos)]
    path_len = 0
    max_col, max_row, min_col, min_row = 0, 0, 0, 0

    for d in data:
        dd = (0, 0)
        match d[0]:
            case "R":
                dd = (0, 1)
            case "D":
                dd = (1, 0)
            case "L":
                dd = (0, -1)
            case "U":
                dd = (-1, 0)
        for _ in range(d[1]):
            path_len += 1
            pos[0] += dd[0]
            pos[1] += dd[1]
            if pos[0] > max_row:
                max_row = pos[0]
            elif pos[0] < min_row:
                min_row = pos[0]
            if pos[1] > max_col:
                max_col = pos[1]
            elif pos[1] < min_col:
                min_col = pos[1]

            points.append(tuple(pos))

    path = Path(points, closed=True)
    all_coords = set(product(range(min_row, max_row + 1), range(min_row, max_col + 1)))
    candidates = all_coords - set(points)

    return path_len + sum(path.contains_points(list(candidates)))


def range_intersects(a: range, b: range):
    return len(range(max(a.start, b.start), min(a.stop, b.stop))) > 0


def part2(data):
    """Solve part 2."""
    pos = [0, 0]
    points = [tuple(pos)]
    path_len = 0
    h = [d[2][2:-1] for d in data]
    dehexed = [(int(hh[-1]), int(f"0x{hh[:-1]}", 16)) for hh in h]
    horizontal = {}
    vertical = {}

    for d in dehexed:
        dd = (0, 0)
        match d[0]:
            case 0:
                dd = (0, d[1])
                if pos[0] in horizontal:
                    horizontal[pos[0]].append(range(pos[1], pos[1] + d[1]))
                else:
                    horizontal[pos[0]] = [range(pos[1], pos[1] + d[1])]
            case 1:
                dd = (d[1], 0)
                if pos[1] in vertical:
                    vertical[pos[1]].append(range(pos[0], pos[0] + d[1]))
                else:
                    vertical[pos[1]] = [range(pos[0], pos[0] + d[1])]
            case 2:
                dd = (0, -d[1])
                if pos[0] in horizontal:
                    horizontal[pos[0]].append(range(pos[1] - d[1], pos[1]))
                else:
                    horizontal[pos[0]] = [range(pos[1] - d[1], pos[1])]
            case 3:
                dd = (-d[1], 0)
                if pos[1] in vertical:
                    vertical[pos[1]].append(range(pos[0] - d[1], pos[0]))
                else:
                    vertical[pos[1]] = [range(pos[0] - d[1], pos[0])]

        path_len += d[1]
        pos[0] += dd[0]
        pos[1] += dd[1]

        points.append(tuple(pos))

    path = Path(points, closed=True)
    rows = []
    cols = []
    for r, c in points:
        rows.append(r)
        cols.append(c)
    rows = sorted(set(rows))
    cols = sorted(set(cols))

    tot = 0
    for i, rr in enumerate(rows[:-1]):
        dr = rows[i + 1] - rr
        for j, cc in enumerate(cols[:-1]):
            # might need to add case for snuggling lines if main fails
            dc = cols[j + 1] - cc
            removed_top = False
            removed_btm = False
            removed_left = False

            if path.contains_point((rr + 1, cc + 1)):
                tot += (dr + 1) * (dc + 1)
                # remove double counted side(s)
                # top
                if rr in horizontal:
                    top = range(cc + 1, cc + dc - 1)
                    if any([range_intersects(top, hor) for hor in horizontal[rr]]):
                        tot -= dc
                        removed_top = True
                # left
                if cc in vertical:
                    left = range(rr + 1, rr + dr - 1)
                    if any([range_intersects(left, vert) for vert in vertical[cc]]):
                        tot -= dr
                        removed_left = True
                        # fix double remove
                        if removed_top:
                            tot += 1
                # bottom if last row
                if i == len(rows) - 2 and rows[-1] in horizontal:
                    btm = range(cc, cc + dc)
                    if any(
                        [range_intersects(btm, hor) for hor in horizontal[rows[-1]]]
                    ):
                        removed_btm = True
                        tot -= dc
                        if removed_left:
                            tot += 1
                # right if last col
                if j == len(cols) - 2 and cols[-1] in vertical:
                    right = range(rr, rr + dr)
                    if any(
                        [range_intersects(right, vert) for vert in vertical[cols[-1]]]
                    ):
                        tot -= dr
                        # fix double remove of corner
                        if removed_btm:
                            tot += 1
                        if removed_top:
                            tot += 1
    return tot


#### UTILITY FUNCTIONS #### + 1)
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
