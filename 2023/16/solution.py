import copy
import pathlib
from posixpath import split
from time import process_time_ns, sleep, time_ns
import pytest
import os
import concurrent.futures as fut
from multiprocessing import Process, Value, Lock, Queue
from aocd.models import Puzzle
import queue

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
class BeamIDGen:
    def __init__(self) -> None:
        self.lock = Lock()
        self.val = Value("i", 0)

    def gen(self):
        with self.lock:
            self.val.value += 1
            return self.val.value - 1

    def value(self):
        with self.lock:
            return self.val.value


def parse(puzzle_input):
    """Parse input."""
    return [list(col) for col in puzzle_input.split("\n")]


class Beam:
    def __init__(self, row, col, nrow, ncol, state):
        self.energized = 0  # how many have we flipped
        self.row = row
        self.col = col
        self.nrow = nrow
        self.ncol = ncol
        self.id = state.id_gen.gen()
        state.todoQueue.put(self)

    def step(self, state):
        if self.nrow >= len(state.pattern) or 0 > self.nrow:
            state.doneQueue.put(self)
            return
        if self.ncol >= len(state.pattern[0]) or 0 > self.ncol:
            state.doneQueue.put(self)
            return
        nch = state.pattern[self.nrow][self.ncol]
        dr = self.nrow - self.row
        dc = self.ncol - self.col
        self.row = self.nrow
        self.col = self.ncol
        match (nch):
            case ".":
                with state.pattern_lock:
                    # Make sure not changed
                    if state.pattern[self.nrow][self.ncol] == ".":
                        state.pattern[self.nrow][self.ncol] = "#"
                        self.energized += 1
                self.nrow = self.nrow + dr
                self.ncol = self.ncol + dc

            case "#":
                self.nrow = self.nrow + dr
                self.ncol = self.ncol + dc

            case "/":
                with state.mirror_lock:
                    if (self.row, self.col) not in state.used_mirrors:
                        state.used_mirrors.append((self.row, self.col))
                self.nrow = self.nrow - dc
                self.ncol = self.ncol - dr
            case "\\":
                with state.mirror_lock:
                    if (self.row, self.col) not in state.used_mirrors:
                        state.used_mirrors.append((self.row, self.col))
                self.nrow = self.nrow + dc
                self.ncol = self.ncol + dr
            case "|":
                with state.splitter_lock:
                    if (self.row, self.col) in state.used_splitters:
                        state.doneQueue.put(self)
                        return
                    else:
                        state.used_splitters.append((self.row, self.col))

                Beam(self.row, self.col, self.nrow + 1, self.ncol, state)
                self.nrow -= 1

            case "-":
                with state.splitter_lock:
                    if (self.row, self.col) in state.used_splitters:
                        state.doneQueue.put(self)
                        return
                    else:
                        state.used_splitters.append((self.row, self.col))
                Beam(self.row, self.col, self.nrow, self.ncol + 1, state)
                self.ncol -= 1

        state.todoQueue.put(self)


def run(state):
    with fut.ThreadPoolExecutor(max_workers=32) as executor:
        while state.doneQueue.qsize() < state.id_gen.value():
            try:
                beam = state.todoQueue.get_nowait()
            except queue.Empty:
                sleep(1 / 1000)
            else:
                executor.submit(beam.step, state)
    tot = len(state.used_mirrors) + len(state.used_splitters)
    while not state.doneQueue.empty():
        tot += state.doneQueue.get().energized
    return tot


class State:
    def __init__(self, data):
        self.todoQueue = Queue()
        self.doneQueue = Queue()
        self.pattern_lock = Lock()
        self.splitter_lock = Lock()
        self.mirror_lock = Lock()
        self.used_mirrors = []
        self.used_splitters = []  # splitters will yield same input
        self.id_gen = BeamIDGen()
        self.pattern = copy.deepcopy(data)


class Runner:
    def __init__(self, srow, scol, snrow, sncol, data):
        self.state = State(data)
        self.beam = Beam(srow, scol, snrow, sncol, self.state)

    def run(self):
        with fut.ThreadPoolExecutor() as executor:
            while self.state.doneQueue.qsize() < self.state.id_gen.value():
                try:
                    beam = self.state.todoQueue.get_nowait()
                except queue.Empty:
                    sleep(1 / 1000)
                else:
                    executor.submit(beam.step, self.state)
        tot = len(self.state.used_mirrors) + len(self.state.used_splitters)
        while not self.state.doneQueue.empty():
            tot += self.state.doneQueue.get().energized
        return tot


def part1(data):
    """Solve part 1."""
    state = State(data)
    Beam(0, -1, 0, 0, state)
    tot = run(state)

    return tot


def start_runner(args):
    return Runner(*args).run()


def part2(data):
    """Solve part 2."""
    args = []
    for i, r in enumerate(data):
        args.append((i, -1, i, 0, data))
        args.append((i, len(r), i, len(r) - 1, data))

    for i, c in enumerate(data[0]):
        args.append((-1, i, 0, i, data))
        args.append((len(data), i, len(data) - 1, i, data))

    tots = []
    with fut.ProcessPoolExecutor() as executor:
        for r, res in zip(args, executor.map(start_runner, args)):
            tots.append(res)

    return max(tots)


#### UTILITY FUNCTIONS ####
def init():
    with open("aoc-key", "r") as keyfile:
        os.environ["AOC_SESSION"] = keyfile.read()


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    parsed = parse(puzzle_input)
    data = parsed if parsed is not None else puzzle_input
    t = process_time_ns()
    solution1 = part1(data)
    print(f"Finished in {process_time_ns() - t}")
    t = process_time_ns()
    solution2 = part2(data)
    print(f"Finished in {process_time_ns() - t}")

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
    print(ans)
    submit(puzzle, *ans)


if __name__ == "__main__":
    main()
