from aocd import get_data
from aocd.models import Puzzle
import os
import pathlib
from itertools import combinations, chain
import sys


def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def parse(puzzle_input):
    """Parse input."""


def part1(data: str):
    """Solve part 1."""
    tot = 0
    for line in data.split('\n'):
        digits = [c for c in line if c.isdigit()]
        tot += int(digits[0] + digits[-1])
    
    return tot

def flatten(l):
    return [item for sublist in l for item in sublist]

def part2(data: str):
    """Solve part 2."""
    nums = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    tot = 0
    for line in data.split('\n'):
        buffer = []
        digits = []
        for c in line:
            if c.isdigit() and len(buffer) == 0:
                digits.append(c)
                continue

            elif c.isdigit():
                bs = ''.join(buffer)
                res = [str(bs)[x:y] for x, y in combinations( range(len(str(bs)) + 1), r = 2)]                
                sub = [s for s in res if s in list(nums.keys())]
                digits.append([str(nums[d]) for d in sub])
                digits = flatten(digits)
                buffer = []
                digits.append(c)
                continue

            if c.isalpha:
                buffer.append(c)
            
        if len(buffer) != 0:
            bs = ''.join(buffer)
            res = [str(bs)[x:y] for x, y in combinations( range(len(str(bs)) + 1), r = 2)]                
            sub = [s for s in res if s in list(nums.keys())]
            digits.append([str(nums[d]) for d in sub])
            digits = flatten(digits)
            
        print(line)
        print(digits)
        tot += int(digits[0] + digits[-1])

    return tot





def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    init()
    print(part2(get_data()))
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
