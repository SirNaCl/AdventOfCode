import math
import pathlib
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    pin = puzzle_input.split("\n")
    times = [int(c) for c in pin[0].split("Time:")[1].split(" ") if len(c) > 0]
    dist = [int(c) for c in pin[1].split("Distance:")[1].split(" ") if len(c) > 0]
    return zip(times, dist)


def part1old(data):
    """Solve part 1.
    Go as long as possible
    Go faster the more you charge
    Only hold at start
    acceleration = 1mm/ms/ms holding
    Distance moved = 1mm/ms/ms holding *ms not holding
    determine how many ways you can win
    the solution is the product of each race's margin of error"""

    # Always maximum when holdin for half the time?
    game_margins = list()
    for gt, gd in data:
        margin = 0
        for acc in range(math.ceil(gt / 2)):  # Time held = acc
            tr = gt - acc  # time released
            d = acc**3 * tr - (acc**2) * (tr**2) + (tr**3) * (acc / 3)
            print(f"{acc}: {d}")
            if d > gd:
                margin += 2
        if gt % 2 == 0 and margin > 0:  # remove extra if even
            margin -= 1

        game_margins.append(margin)

    return math.prod(game_margins)


def part1(data):
    """Solve part 1.
    Go as long as possible
    Go faster the more you charge
    Only hold at start
    acceleration = 1mm/ms/ms holding
    Distance moved = 1mm/ms/ms holding *ms not holding
    determine how many ways you can win
    the solution is the product of each race's margin of error"""

    # Always maximum when holdin for half the time?
    game_margins = list()
    for gt, gd in data:
        margin = 0
        for vel in range(math.floor(gt / 2) + 1):  # Time held = acc
            d = vel * (gt - vel)
            if d > gd:
                margin += 2

        if gt % 2 == 0 and margin > 0:  # remove extra if even
            margin -= 1
        game_margins.append(margin)

    return math.prod(game_margins)


def part2(data):
    """Solve part 2."""
    time = ""
    dist = ""
    for gt, gd in data:
        print(gt)
        time += str(gt)
        dist += str(gd)
    time = int(time)
    dist = int(dist)
    min_vel = -1
    margin = 0
    for vel in range(math.floor(time / 2) + 1):  # Time held = acc
        d = vel * (time - vel)
        if d > dist:
            min_vel = vel
            break
    margin = (math.floor(time / 2) + 1 - min_vel) * 2
    if time % 2 == 0:
        margin -= 1

    return margin


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    solution1 = part1(data)
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
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
