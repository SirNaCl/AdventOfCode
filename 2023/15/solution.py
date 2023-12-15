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
    return puzzle_input.split(",")


def hash_word(w):
    val = 0
    for c in w:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def part1(data):
    """Solve part 1."""
    tot = 0
    for word in data:
        if word == "":
            continue
        h = hash_word(word)
        tot += h

    return tot


def part2(data):
    """Solve part 2."""
    boxes = {i: [] for i in range(256)}
    lengths = {}
    for word in data:
        if word == "":
            continue

        if "=" in word:
            ww = word.split("=")
            label = ww[0]
            f = ww[1]
            h = hash_word(label)
            if label not in boxes[h]:
                boxes[h].append(label)
            lengths[label] = int(f)

        else:
            ww = word.split("-")
            label = ww[0]
            h = hash_word(label)
            if label in boxes[h]:
                boxes[h].remove(label)

    tot = 0
    for h, box in boxes.items():
        for i, label in enumerate(box, 1):
            tot += (1 + h) * lengths[label] * i

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
