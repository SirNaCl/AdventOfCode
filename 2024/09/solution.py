import pathlib
from time import perf_counter_ns
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def benchmark(func):
    def timed(*args, **kwargs):
        t1 = perf_counter_ns()
        res = func(*args, **kwargs)
        t2 = perf_counter_ns()
        print(f"{func.__name__} took {(t2-t1)/1000000}ms")
        return res

    return timed


class Block:
    def __init__(self, id: int, size: int, free: bool):
        self.id = id if not free else -1
        self.free = free
        self.size = size

    def __gt__(self, rhs):
        return self.size > rhs.size

    def __str__(self):
        ch = f"{self.id}" if not self.free else "."
        return f"{ch * self.size}"

    def __repr__(self):
        ch = f"{self.id}" if not self.free else "."
        return f"{ch * self.size}"


def parse(puzzle_input):
    """Parse input."""
    blocks = []
    for i, size in enumerate(puzzle_input):
        if int(size) == 0:
            continue
        id = int(i) // 2
        s = int(size)
        free = i % 2 == 1
        blocks.append(Block(id, s, free))
    return blocks


@benchmark
def part1(data):
    """Solve part 1."""
    blocks = data.copy()
    b = []
    for bl in blocks:
        b.extend([bl.id if not bl.free else -1] * bl.size)

    i = len(b)
    dot_idx = 0

    while i >= 0:
        i -= 1
        if b[i] == -1:
            continue

        dot_idx = b.index(-1)
        if dot_idx < i:
            b[dot_idx] = b[i]
            b[i] = -1

    tot = 0
    for idx, bb in enumerate(b):
        if bb == -1:
            break
        tot += bb * idx

    return tot


def first_free_idx(blocks):
    for i, b in enumerate(blocks):
        if b.free:
            return i

    return -1


def first_fits(blocks, size):
    for i, b in enumerate(blocks):
        if b.free and b.size >= size:
            return i, b

    return -1, Block(-1, 0, True)


@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True

    blocks: list[Block] = data.copy()
    i = len(blocks) - 1
    frst_fr = first_free_idx(blocks)

    while i > frst_fr:
        if blocks[i].free:
            i -= 1
            continue

        b = blocks[i]
        targ_i, targ = first_fits(blocks, b.size)

        if targ_i == -1 or targ_i > i:
            i -= 1
            continue

        blocks[targ_i] = b
        blocks[i] = Block(-1, b.size, True)
        if targ.size > b.size:
            blocks.insert(targ_i + 1, Block(-1, targ.size - b.size, True))
        frst_fr = first_free_idx(blocks)

    b = []
    for bl in blocks:
        b.extend([bl.id if not bl.free else -1] * bl.size)

    tot = 0
    for idx, bb in enumerate(b):
        if bb == -1:
            continue
        tot += bb * idx
    return tot


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
            f"Already submitted correct answer a: {puzzle.answer_a}, you tried to submit {ans_a} "
            + f"({'correct' if str(puzzle.answer_a) == str(ans_a) else 'incorrect'})!"
        )
    else:
        print(f"Submitting {ans_a} as answer to part 1:")
        puzzle.answer_a = ans_a

    if ans_b is None:
        print("No solution for part 2, skipping submission!")
    elif puzzle.answered_b:
        print(
            f"Already submitted correct answer b: {puzzle.answer_b}, you tried to submit {ans_b} "
            + f"({'correct' if str(puzzle.answer_b) == str(ans_b) else 'incorrect'})!"
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
