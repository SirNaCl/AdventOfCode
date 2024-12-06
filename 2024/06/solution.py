import pathlib
import pytest
import os
from aocd.models import Puzzle
from pprint import pprint

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [[c for c in s] for s in puzzle_input.split("\n")]


START_CHAR = "^"
OBSTRUCTION = "#"


def path(data, xst, yst):
    p = {
        "up": set(),
        "down": set(),
        "right": set(),
        "left": set(),
    }
    direction = "up"
    x = xst
    y = yst
    escaped = False
    while not escaped:
        if direction in "up":
            while y > 0 and direction in "up":
                y -= 1
                if data[y][x] in OBSTRUCTION:
                    y += 1
                    direction = "right"
                else:
                    if y == 0:
                        escaped = True
                    p["up"].add((x, y))

        if direction in "right":
            while x < len(data[0]) - 1 and direction in "right":
                x += 1
                if data[y][x] in OBSTRUCTION:
                    x -= 1
                    direction = "down"
                else:
                    if x == len(data[0]) - 1:
                        escaped = True
                    p["right"].add((x, y))

        if direction in "down":
            while y < len(data) - 1 and direction in "down":
                y += 1
                if data[y][x] in OBSTRUCTION:
                    y -= 1
                    direction = "left"
                else:
                    if y == len(data) - 1:
                        escaped = True
                    p["down"].add((x, y))

        if direction in "left":
            while x > 0 and direction in "left":
                x -= 1
                if data[y][x] in OBSTRUCTION:
                    x += 1
                    direction = "up"
                else:
                    if x == 0:
                        escaped = True
                    p["left"].add((x, y))

    return p


def part1(data):
    """Solve part 1."""
    xst, yst = 0, 0

    for i, line in enumerate(data):
        if START_CHAR not in line:
            continue
        yst = i
        xst = line.index(START_CHAR)

    v = path(data, xst, yst)
    coords = set()
    for key in v:
        coords = coords.union(v[key])

    return len(coords)


def is_inf(data, xst, yst, xobj, yobj, direction):
    _dir = "up"
    cache = set((xst, yst, direction))
    x = xst
    y = yst
    while True:
        while y > 0 and _dir in "up":
            y -= 1
            if (x, y, _dir) in cache:
                return True

            cache.add((x, y, _dir))

            if data[y][x] in OBSTRUCTION or (x == xobj and y == yobj):
                y += 1
                _dir = "right"
            else:
                if y == 0:
                    return False

        while x < len(data[0]) - 1 and _dir in "right":
            x += 1
            if (x, y, _dir) in cache:
                return True

            cache.add((x, y, _dir))

            if data[y][x] in OBSTRUCTION or (x == xobj and y == yobj):
                x -= 1
                _dir = "down"
            else:
                if x == len(data[0]) - 1:
                    return False

        while y < len(data) - 1 and _dir in "down":
            y += 1
            if (x, y, _dir) in cache:
                return True

            cache.add((x, y, _dir))

            if data[y][x] in OBSTRUCTION or (x == xobj and y == yobj):
                y -= 1
                _dir = "left"
            else:
                if y == len(data) - 1:
                    return False

        while x > 0 and _dir in "left":
            x -= 1
            if (x, y, _dir) in cache:
                return True

            cache.add((x, y, _dir))

            if data[y][x] in OBSTRUCTION or (x == xobj and y == yobj):
                x += 1
                _dir = "up"
            else:
                if x == 0:
                    return False


def part2(data):
    """Solve part 2."""
    yst, xst = 0, 0

    obstructions = set()
    for yi, row in enumerate(data):
        for xi, c in enumerate(row):
            if OBSTRUCTION in c:
                obstructions.add((xi, yi))
            elif START_CHAR in c:
                yst = yi
                xst = xi

    visited = path(data, xst, yst)
    new_obs = set()

    for direction in visited:
        for x, y in visited[direction]:
            if (x, y) in new_obs:
                continue
            if is_inf(data, xst, yst, x, y, direction):
                new_obs.add((x, y))

    return len(new_obs)


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
