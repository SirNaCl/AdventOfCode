from aocd.models import Puzzle
import os
import pathlib
import sys
import functools

class Node:
    def __init__(self, flowrate: int):
        self.open = False
        self.flowrate = flowrate
        self.tunnels = []
    
    def add_tunnel(self, Node):
        self.tunnels.append(Node)
    
    def calc_path(self, time: int):
        if time < 1:
            return 0
        
        skip = max([t.calc_path(time-1) for t in self.tunnels])

        if self.open:
            return skip

        stay = self.flowrate * (time-1) + max([t.calc_path(time-2) for t in self.tunnels])
        print(stay)

        if skip < stay:
            self.open = True
            return stay

        return skip


def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def parse(puzzle_input: str):
    """Parse input."""
    data = {}
    start = None

    for line in puzzle_input.split('\n'):
        words = line.replace(',', '').split(" ")
        name = words[1]
        if start is None:
            start = name
        rate = words[4][5:-1]
        tunnels = words[9:] 
        data[name] = (Node(int(rate)), tunnels)

    for name, (node, nbs) in data.items():
        for nb in nbs:
            node.add_tunnel(data[nb][0])
    
    return data[start][0]

def part1(data: Node):
    """Solve part 1."""
    return data.calc_path(30)


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    init()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
