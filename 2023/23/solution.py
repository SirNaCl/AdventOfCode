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


def gen_graph(nodes, adj):
    graph = {n: {} for n in nodes}
    for node in nodes:
        visited = {node}
        walkers = [(node, int(0))]  # pos, steps
        while walkers:
            wpos, steps = walkers.pop()
            if wpos in nodes and steps > 0:
                graph[node][wpos] = steps
                continue

            for a in adj[wpos]:
                if a not in visited:
                    walkers.append((a, steps + 1))
                    visited.add(a)

    return graph


def search(node, end, graph, visited):
    if node == end:
        return 0

    d = -float("inf")
    visited.add(node)
    for edge in graph[node]:
        if edge not in visited:
            d = max(d, search(edge, end, graph, visited) + graph[node][edge])
    visited.remove(node)

    return d


def part2(data):
    """Solve part 2."""
    start = (0, data[0].index("."))
    end = (len(data) - 1, data[-1].index("."))

    adj = {}
    n = start
    nodes = [start, end]
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

            if len(adj[n]) > 2:
                nodes.append(n)

    graph = gen_graph(nodes, adj)
    visited = set()
    return search(start, end, graph, visited)


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
