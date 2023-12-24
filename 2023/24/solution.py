import pathlib
import re
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [map(int, re.findall(r"[-]*\d+", line)) for line in puzzle_input.split("\n")]


def t_enter_leave(h, dh, lim_min, lim_max):
    t = lambda l: (l - h) / dh
    return tuple(sorted((max(0, t(lim_min)), max(0, t(lim_max)))))


def h_at(h, dh, t):
    return h + (dh * t)


def get_vertice_xy(limx, limy, x, y, _, dx, dy, __):
    tx = t_enter_leave(x, dx, *limx)
    ty = t_enter_leave(y, dy, *limy)
    t_enter, t_leave = max(tx[0], ty[0]), min(tx[1], ty[1])
    p_in = h_at(x, dx, t_enter), h_at(y, dy, t_enter)
    p_out = h_at(x, dx, t_leave), h_at(y, dy, t_leave)
    return p_in, p_out


def test_collinear(p, q, r):
    px, py = p
    qx, qy = q
    rx, ry = r
    return (
        qx <= max(px, rx)
        and qx >= min(px, rx)
        and qy <= max(py, ry)
        and qy >= min(py, ry)
    )


def or_triplet(p, q, r):
    px, py = p
    qx, qy = q
    rx, ry = r
    o = float(qy - py) * (rx - qx)
    o -= float(qx - px) * (ry - qy)

    return 0 if o == 0 else 2 if o < 0 else 1


def intersects(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    t1 = or_triplet(x1, y1, x2)
    t2 = or_triplet(x1, y1, y2)
    t3 = or_triplet(x2, y2, x1)
    t4 = or_triplet(x2, y2, y1)

    if t1 != t2 and t3 != t4:
        return True

    # collinear
    return False


def part1(data, example=False):
    """Solve part 1."""
    limx = (7, 27) if example else (200000000000000, 400000000000000)
    limy = (7, 27) if example else (200000000000000, 400000000000000)
    vertices = [get_vertice_xy(limx, limy, *d) for d in data]

    tot = 0
    for i, v1 in enumerate(vertices, 1):
        for v2 in vertices[i:]:
            tot += 1 if intersects(v1, v2) else 0

    return tot


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
