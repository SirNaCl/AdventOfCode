from __future__ import annotations
from itertools import product
import pathlib
import pytest
import os
from matplotlib.path import Path
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
root = None  # Node
pipes = {}  # PIPES[COORD][Node]
in_map = [[]]  # MAP[ROW][COL]


class Pipe:
    def __init__(self, pos: tuple[int, int]) -> None:
        if not 0 <= pos[0] < len(in_map) or not 0 <= pos[1] < len(in_map[0]):
            return
        self.pos = pos
        self.nbs = None
        pipes[pos] = self

    # def next(self, src: tuple[int, int]) -> Pipe:
    # Get other neighbor
    #    return self.nbs[1] if src == self.nbs[0].pos else self.nbs[0]

    def init_nbs(self):
        pos = self.pos
        match in_map[pos[0]][pos[1]]:
            case "|":
                n1p = (pos[0] + 1, pos[1])
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0] - 1, pos[1])
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "L":
                n1p = (pos[0], pos[1] + 1)
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0] - 1, pos[1])
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "-":
                n1p = (pos[0], pos[1] + 1)
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0], pos[1] - 1)
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "J":
                n1p = (pos[0] - 1, pos[1])
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0], pos[1] - 1)
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "7":
                n1p = (pos[0] + 1, pos[1])
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0], pos[1] - 1)
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "F":
                n1p = (pos[0] + 1, pos[1])
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2p = (pos[0], pos[1] + 1)
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case "S":
                n = []
                try:
                    if in_map[pos[0] - 1][pos[1]] in ("|", "7", "F"):
                        n.append((pos[0] - 1, pos[1]))
                except:
                    pass
                try:
                    if in_map[pos[0]][pos[1] - 1] in ("-", "F", "L"):
                        n.append((pos[0], pos[1] - 1))
                except:
                    pass
                try:
                    if in_map[pos[0]][pos[1] + 1] in ("J", "-", "7"):
                        n.append((pos[0], pos[1] + 1))
                except:
                    pass
                try:
                    if in_map[pos[0] + 1][pos[1]] in ("|", "L", "J"):
                        n.append((pos[0] + 1, pos[1]))
                except:
                    pass
                n1p, n2p = tuple(n)
                n1 = pipes[n1p] if n1p in pipes else Pipe(n1p)
                n2 = pipes[n2p] if n2p in pipes else Pipe(n2p)
            case _:
                n1 = Pipe((-1, -1))
                n2 = Pipe((-1, -1))

        self.nbs = (n1, n2)

    def next(self, src: Pipe) -> Pipe:
        if self.nbs is None:
            self.init_nbs()
        assert self.nbs is not None
        return self.nbs[1] if src == self.nbs[0] else self.nbs[0]

    def __eq__(self, other):
        return self.pos == other.pos

    def __str__(self):
        return str(self.nbs)


def parse(puzzle_input):
    """Parse input."""
    return [[c for c in row] for row in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    global in_map
    global root
    in_map = data
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == "S":
                root = Pipe((i, j))

    assert root is not None
    root.init_nbs()
    assert root.nbs is not None

    w1pr, w2pr = root, root
    w1, w2 = root.nbs
    i = 1
    while True:
        w1, w1pr = w1.next(w1pr), w1
        w2, w2pr = w2.next(w2pr), w2
        i += 1
        if w1 == w2 or w1.next(w1pr) == w2:
            return i


def part2(data):
    """Solve part 2."""
    global in_map
    global root
    global pipes
    pipes = {}
    in_map = data
    root = None
    loop = []
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == "S":
                root = Pipe((i, j))
                break

        if root is not None:
            break

    assert root is not None
    root.init_nbs()
    assert root.nbs is not None
    w1pr = root
    w1 = root.nbs[0]

    while w1 != root:
        w1, w1pr = w1.next(w1pr), w1

    loop = Path(list(pipes.keys()), closed=True)

    # Loop created
    coords = set(pipes.keys())
    c_sorted = sorted(coords, key=lambda x: x[1])
    cmin, cmax = c_sorted[0][1], c_sorted[-1][1]
    r_sorted = sorted(coords, key=lambda x: x[0])
    rmin, rmax = r_sorted[0][0], r_sorted[-1][0]
    all_coords = set(product(range(rmin, rmax), range(cmin, cmax)))
    candidates = all_coords - coords
    return sum(loop.contains_points(list(candidates)))


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
