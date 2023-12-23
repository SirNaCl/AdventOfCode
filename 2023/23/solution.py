import pathlib
import sys
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)

sys.setrecursionlimit(10**5)


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [list(line) for line in puzzle_input.split("\n")]


def topo_sort(coords):
    global adj, visited, stack
    visited[coords] = True

    for a in adj[coords]:
        if not visited[a]:
            topo_sort(a)

    stack.append(coords)


def part1(data):
    """Solve part 1."""
    global adj, visited, stack
    stack = []
    start = (0, data[0].index("."))
    end = (len(data) - 1, data[-1].index("."))

    adj = {}

    n = start
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == "#":
                continue

            n = (r, c)
            adj[n] = []
            r, c = n

            if col == ">":
                adj[n].append((r, c + 1))
                continue
            if col == "<":
                adj[n].append((r, c - 1))
                continue
            if col == "v":
                adj[n].append((r + 1, c))
                continue
            if col == "^":
                adj[n].append((r - 1, c))
                continue

            try:
                if data[r - 1][c] in ("^", "."):
                    adj[n].append((r - 1, c))
            except:
                pass
            try:
                if data[r + 1][c] in ("v", "."):
                    adj[n].append((r + 1, c))
            except:
                pass
            try:
                if data[r][c - 1] in ("<", "."):
                    adj[n].append((r, c - 1))
            except:
                pass
            try:
                if data[r][c + 1] in (">", "."):
                    adj[n].append((r, c + 1))
            except:
                pass

    visited = {k: False for k in adj.keys()}
    dists = {k: -(10**7) for k in adj.keys()}

    topo_sort(start)

    dists[start] = 0
    while stack:
        u = stack.pop()
        assert (d := dists[u]) != -(10**7)

        for a in adj[u]:
            if dists[a] < d + 1:
                dists[a] = d + 1

    return dists[end]


def topo_sort_splits(coords, branch=0):
    global adj, visited_s, stacks
    visited_s[branch][coords] = True
    created = []
    child_creat = []
    if len(adj[coords]) <= 1:
        for a in adj[coords]:
            if not visited_s[branch][a]:
                child_creat = topo_sort_splits(a, branch)
    else:
        for i, a in enumerate(adj[coords]):
            if not visited_s[branch][a]:
                if len(created) > 0:
                    visited_s.append(visited_s[branch].copy())
                    stacks.append(stacks[branch].copy())
                created.append(len(visited_s))
        nb = 0
        to_split = [branch] + created
        for i, a in enumerate(adj[coords]):
            if not visited_s[branch][a]:
                child_creat.append(topo_sort_splits(a, to_split[nb]))
                nb += 1

    for cc in child_creat:
        created.append(cc)

    for bn in created:
        try:
            stacks[bn].append(coords)
        except:
            pass
    stacks[branch].append(coords)
    return created


def part2(data):
    """Solve part 2."""
    global adj, visited_s, stacks
    stacks = [[]]
    start = (0, data[0].index("."))
    end = (len(data) - 1, data[-1].index("."))

    adj = {}

    n = start
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == "#":
                continue

            n = (r, c)
            adj[n] = []
            r, c = n

            try:
                if data[r - 1][c] != "#":
                    adj[n].append((r - 1, c))
            except:
                pass
            try:
                if data[r + 1][c] != "#":
                    adj[n].append((r + 1, c))
            except:
                pass
            try:
                if data[r][c - 1] != "#":
                    adj[n].append((r, c - 1))
            except:
                pass
            try:
                if data[r][c + 1] != "#":
                    adj[n].append((r, c + 1))
            except:
                pass

    visited_s = [{k: False for k in adj.keys()}]

    topo_sort_splits(start)
    dists = [{k: -(10**7) for k in adj.keys()}] * len(stacks)
    maxdist = 0
    succ = False
    for branch in range(len(stacks)):
        dists[branch][start] = 0
        s = stacks[branch].copy()
        while stacks[branch]:
            u = stacks[branch].pop()

            assert (d := dists[branch][u]) != -(10**7)

            for a in adj[u]:
                if dists[branch][a] < d + 1:
                    dists[branch][a] = d + 1
        if dists[branch][end] > maxdist:
            if succ:
                maxdist = dists[branch][end]
                print(s)
                return maxdist
            succ = True
            maxdist = dists[branch][end]

    return maxdist


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
