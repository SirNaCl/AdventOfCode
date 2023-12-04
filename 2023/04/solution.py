import pathlib
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
def parse(puzzle_input: str):
    """Parse input."""
    games = list()
    for line in puzzle_input.split("\n"):
        have, won = tuple(line.split(":")[1].split("|"))
        games.append((set(have.split()), set(won.split())))

    return games


def part1(data: list[tuple[set[str], set[str]]]):
    """Solve part 1."""
    tot = 0
    for have, won in data:
        game_score = 0
        for n in have:
            if n == "":
                continue
            if n in won:
                game_score = 1 if game_score == 0 else game_score * 2

        tot += game_score
    return tot


def part2(data: list[tuple[set[str], set[str]]]):
    """Solve part 2."""
    card_counts = [1] * len(data)
    game_scores = [0] * len(data)
    for i, (have, won) in enumerate(data):
        game_score = 0
        for n in have:
            if n == "":
                continue
            if n in won:
                game_score += 1

        game_scores[i] = game_score

    for i, score in enumerate(game_scores):
        if score == 0:
            continue
        for j in range(i + 1, i + score + 1):
            try:
                card_counts[j] += card_counts[i]
            except IndexError:
                break
    return sum(card_counts)


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
