from aocd.models import Puzzle
import os

def init():
    with open('aoc-key', 'r') as keyfile:
        os.environ['AOC_SESSION'] = keyfile.read()


if __name__ == '__main__':
    init()
    puzzle = Puzzle(year=2020, day=1)
    # Personal input data. Your data will be different.
    print(puzzle.input_data[:20])
