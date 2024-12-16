from itertools import combinations, permutations
import pathlib
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint
import networkx as nx

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.func import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    return GridChar(puzzle_input)


def weight_func(u, v, d):
    if "w" in d:
        return d["w"]
    return 1


# ~9000ms -.- (I can't be bothered...)
@benchmark
def prep_graph(G, start, end):
    # create new edges where there are turns
    updated = True
    while updated:
        updated = False
        for n, nbhdict in G.adjacency():
            nei = [node for node in nbhdict]
            if n == start:
                for nnr, nnc in nei:
                    dr, dc = nnr - n[0], nnc - n[1]
                    if abs(dr) == 1:
                        G.edges[n, (nnr, nnc)]["w"] = 1001
                    elif dc == -1:
                        G.edges[n, (nnr, nnc)]["w"] = 2001

            if n == end:
                continue

            edges_new = set()
            skip = False
            for nn in nei:
                if "w" in G.edges[n, nn] and G.edges[n, nn]["w"] > 1000:
                    # already processed as turn so this node can't be a turn
                    skip = True
                    break

            if skip:
                continue

            for n1, n2 in combinations(nei, 2):
                dr, dc = n2[0] - n1[0], n2[1] - n1[1]
                if dr == 0 or dc == 0:
                    # straight line
                    edges_new.add((n1, n2, 2))
                else:
                    # we need to turn
                    edges_new.add((n1, n2, 1002))

            if any([e[2] > 1000 for e in edges_new]):
                # we've found a turn, update & remove existing
                for nn in nei:
                    G.remove_edge(n, nn)

                for u, v, w in edges_new:
                    G.add_edge(u, v, w=w)

                G.remove_node(n)
                updated = True
                break


# 80ms + prep_graph
@benchmark
def part1(data: GridChar):
    """Solve part 1."""
    start = data.find_all("S")[0]
    end = data.find_all("E")[0]
    G = data.to_graph(ignore=["#"])

    prep_graph(G, start, end)
    return nx.shortest_path_length(G, start, end, weight=weight_func)


# 1000ms + prep_graph
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True

    start = data.find_all("S")[0]
    end = data.find_all("E")[0]
    walls = data.find_all("#")
    G = data.to_graph(ignore=["#"])
    prep_graph(G, start, end)

    visited = set()
    for p in nx.all_shortest_paths(G, start, end, weight=weight_func):
        for n1, n2 in zip(p, p[1:]):
            visited.add(n1)
            visited.add(n2)

            n1r, n1c = n1
            n2r, n2c = n2
            dr = n2r - n1r
            dc = n2c - n1c

            if abs(dr + dc) == 1:
                # Not a corner
                continue

            if abs(dr) == 2 or abs(dc) == 2:
                # Straight through intersection
                visited.add((n1r + dr / 2, n1c + dc / 2))
                continue

            # Determine the node crossed during the turn
            candidates = [(n1r + dr, n1c), (n1r, n1c + dc)]
            for c in candidates:
                if c not in walls:
                    visited.add(c)
                    break

    return len(visited)


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
