from math import lcm
import pathlib
import re
import pytest
import os
from aocd.models import Puzzle

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)

# % - ignore high. Starts off.
# If given low at off, toggle and send high,
# if given low at high, toggle and send low

# & - Remember type of most recent from each
# default low
# when received, send low if all in memory is high
# else low

# broadcaster relays incomining to all connected

# "button" sends low to broadcaster. After pushing wait for all
# to process

# pulses are handled FIFO

# result is lowsent * highsent after 4000 cycles


#### SOLUTION ####
def parse(puzzle_input):
    """Parse input."""
    return [re.findall(r"[%|&]*\w+[\n|$]*", line) for line in puzzle_input.split("\n")]


class Module:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.state = False  # for flipflop
        self.incoming = {}  # for inverter
        self.targets = []
        self.outputs = 0  # targets that wont send

    def all_inc_high(self):
        return all([p == 1 for p in self.incoming.values()])

    def tupled(self):
        return tuple([self.name, self.type, self.state, self.all_inc_high()])


modules = {}


def btn_press():
    global modules
    s = [(t, int(0), "broadcaster") for t in modules["broadcaster"].targets]
    l = 1 + len(s)  # button + initial
    h = 0

    while s:
        m, pulse, sender = s.pop(0)
        match m.type:
            case "%":
                if pulse == 0:
                    if m.state:
                        # turn off and send low
                        m.state = False
                        l += m.outputs
                        for t in m.targets:
                            s.append((t, 0, m.name))
                            l += 1
                    else:
                        m.state = True
                        h += m.outputs
                        for t in m.targets:
                            s.append((t, 1, m.name))
                            h += 1

            case "&":
                m.incoming[sender] = pulse
                if m.all_inc_high():
                    pp = 0
                    l += len(m.targets) + m.outputs
                else:
                    pp = 1
                    h += len(m.targets) + m.outputs
                for t in m.targets:
                    s.append((t, pp, m.name))

    return l, h


sends2rx = ""


def solinit(data):
    global modules
    global sends2rx
    modules = {}

    for d in data:
        mtype = "broadcaster"
        key = "broadcaster"
        if d[0][0] in ("&", "%"):
            mtype = d[0][0]
            key = d[0][1:]

        modules[key] = Module(key, mtype)

    for d in data:
        mtype = "broadcaster"
        key = "broadcaster"
        if d[0][0] in ("&", "%"):
            mtype = d[0][0]
            key = d[0][1:]
        for t in d[1:]:
            if t not in modules:
                if t == "rx":
                    sends2rx = key
                modules[key].outputs += 1
                continue
            modules[key].targets.append(modules[t])
            if modules[t].type == "&":
                modules[t].incoming[key] = 0


# 0 for low, 1 for high
# button counts as low for total
def part1(data):
    """Solve part 1."""
    global modules
    solinit(data)
    tot_low = 0
    tot_high = 0
    for _ in range(1000):
        fullstate = []
        for m in modules.values():
            fullstate.append(m.tupled())

        l, h = btn_press()
        tot_low += l
        tot_high += h

    return tot_high * tot_low


def part2(data):
    """Solve part 2."""
    global modules
    global sends2rx
    sends2sender = set()

    solinit(data)

    for m in modules.values():
        if sends2rx in [t.name for t in m.targets]:
            sends2sender.add(m.name)
    cycles = {s: -1 for s in sends2sender}
    i = 0
    while any([v == -1 for v in cycles.values()]):
        i += 1
        s = [(t, int(0), "broadcaster") for t in modules["broadcaster"].targets]

        while s:
            m, pulse, sender = s.pop(0)
            match m.type:
                case "%":
                    if pulse == 0:
                        if m.state:
                            # turn off and send low
                            m.state = False
                            if m.name in sends2rx:
                                return True
                            for t in m.targets:
                                s.append((t, 0, m.name))
                        else:
                            m.state = True
                            for t in m.targets:
                                s.append((t, 1, m.name))

                case "&":
                    m.incoming[sender] = pulse
                    if m.all_inc_high():
                        pp = 0
                    else:
                        pp = 1
                        # Check if we send high to rx's sender
                        if m.name in sends2sender and cycles[m.name] == -1:
                            cycles[m.name] = i

                    for t in m.targets:
                        s.append((t, pp, m.name))

    return lcm(*list(cycles.values()))


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
