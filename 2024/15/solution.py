from collections import defaultdict
import pathlib
from time import sleep, time
import pytest
import os
from aocd.models import Puzzle
from os import path
import sys
from pprint import pprint

# add common util
PATH_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(PATH_ROOT)

from common.decorators import *
from common.grid import *

PUZZLE_DIR = pathlib.Path(__file__).parent
YEAR = int(PUZZLE_DIR.parent.name)
DAY = int(PUZZLE_DIR.name)


#### SOLUTION ####
p2 = False


def parse(puzzle_input):
    """Parse input."""
    g, moves = puzzle_input.split("\n\n")
    g = GridChar(g)
    return g, moves


# First: 63ms
@benchmark
def part1(data):
    """Solve part 1."""
    G: GridChar = data[0].copy()
    moves: str = data[1]
    walls = G.find_all("#")
    boxes = G.find_all("O")
    empty = G.find_all(".")
    robot = G.find_all("@")[0]

    # dicts of walls indexed with row or col
    wdrow = defaultdict(set)
    wdcol = defaultdict(set)
    bdrow = defaultdict(set)
    bdcol = defaultdict(set)
    edrow = defaultdict(set)
    edcol = defaultdict(set)
    for row, col in walls:
        wdrow[row].add(col)
        wdcol[col].add(row)
    for row, col in boxes:
        bdrow[row].add(col)
        bdcol[col].add(row)
    for row, col in empty:
        edrow[row].add(col)
        edcol[col].add(row)

    for move in moves:
        will_move = False

        if move in "<":
            collisionw = 0
            closest_free = 0
            # find closes wall in given direction
            w = wdrow[robot[0]]
            for ww in sorted(list(w)):
                if ww < robot[1] and ww > collisionw:
                    collisionw = ww

            for erow in edrow[robot[0]]:
                if erow < robot[1] and collisionw < erow:
                    will_move = True
                    if erow > closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdrow[robot[0]]):
                if (
                    box < collisionw
                    or robot[1] < box
                    or box - 1 not in edrow[robot[0]]
                    or box < closest_free
                ):
                    continue

                edrow[robot[0]].remove(box - 1)
                edrow[robot[0]].add(box)
                bdrow[robot[0]].remove(box)
                bdrow[robot[0]].add(box - 1)

                edcol[box - 1].remove(robot[0])
                edcol[box].add(robot[0])
                bdcol[box].remove(robot[0])
                bdcol[box - 1].add(robot[0])
                # If a box has moved, we can move as well

            edrow[robot[0]].add(robot[1])
            edrow[robot[0]].remove(robot[1] - 1)
            edcol[robot[1]].add(robot[0])
            edcol[robot[1] - 1].remove(robot[0])
            robot = (robot[0], robot[1] - 1)

        elif move in ">":
            collisionw = float("inf")
            closest_free = float("inf")
            # find closes wall in given direction
            w = wdrow[robot[0]]
            for ww in sorted(list(w)):
                if ww > robot[1] and ww < collisionw:
                    collisionw = ww

            for erow in edrow[robot[0]]:
                if erow > robot[1] and collisionw > erow:
                    will_move = True
                    if erow < closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdrow[robot[0]], reverse=True):
                if (
                    box > collisionw
                    or robot[1] > box
                    or box + 1 not in edrow[robot[0]]
                    or box > closest_free
                ):
                    continue

                edrow[robot[0]].remove(box + 1)
                edrow[robot[0]].add(box)
                bdrow[robot[0]].remove(box)
                bdrow[robot[0]].add(box + 1)

                edcol[box + 1].remove(robot[0])
                edcol[box].add(robot[0])
                bdcol[box].remove(robot[0])
                bdcol[box + 1].add(robot[0])
                # If a box has moved, we can move as well

            edrow[robot[0]].add(robot[1])
            edrow[robot[0]].remove(robot[1] + 1)
            edcol[robot[1]].add(robot[0])
            edcol[robot[1] + 1].remove(robot[0])
            robot = (robot[0], robot[1] + 1)

        elif move in "^":
            collisionw = 0
            closest_free = 0
            # find closes wall in given direction
            w = wdcol[robot[1]]
            for ww in sorted(list(w)):
                if ww < robot[0] and ww > collisionw:
                    collisionw = ww

            for erow in edcol[robot[1]]:
                if erow < robot[0] and collisionw < erow:
                    will_move = True
                    if erow > closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdcol[robot[1]]):
                if (
                    box < collisionw
                    or robot[0] < box
                    or box - 1 not in edcol[robot[1]]
                    or box < closest_free
                ):
                    continue

                edcol[robot[1]].remove(box - 1)
                edcol[robot[1]].add(box)
                bdcol[robot[1]].remove(box)
                bdcol[robot[1]].add(box - 1)

                edrow[box - 1].remove(robot[1])
                edrow[box].add(robot[1])
                bdrow[box].remove(robot[1])
                bdrow[box - 1].add(robot[1])
                # If a box has moved, we can move as well

            edcol[robot[1]].add(robot[0])
            edcol[robot[1]].remove(robot[0] - 1)
            edrow[robot[0]].add(robot[1])
            edrow[robot[0] - 1].remove(robot[1])
            robot = (robot[0] - 1, robot[1])

        elif move in "v":
            # find closes wall in given direction
            collisionw = float("inf")
            closest_free = float("inf")
            w = wdcol[robot[1]]
            for ww in sorted(list(w)):
                if ww > robot[0] and ww < collisionw:
                    collisionw = ww

            for erow in edcol[robot[1]]:
                if erow > robot[0] and collisionw > erow:
                    will_move = True
                    if erow < closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdcol[robot[1]], reverse=True):
                if (
                    box > collisionw
                    or robot[0] > box
                    or box + 1 not in edcol[robot[1]]
                    or box > closest_free
                ):
                    continue

                edcol[robot[1]].remove(box + 1)
                edcol[robot[1]].add(box)
                bdcol[robot[1]].remove(box)
                bdcol[robot[1]].add(box + 1)

                edrow[box + 1].remove(robot[1])
                edrow[box].add(robot[1])
                bdrow[box].remove(robot[1])
                bdrow[box + 1].add(robot[1])
                # If a box has moved, we can move as well

            edcol[robot[1]].add(robot[0])
            edcol[robot[1]].remove(robot[0] + 1)
            edrow[robot[0]].add(robot[1])
            edrow[robot[0] + 1].remove(robot[1])
            robot = (robot[0] + 1, robot[1])

        # end of move loop
    tot = 0
    for row in bdrow:
        for col in bdrow[row]:
            tot += 100 * int(row) + col
    return tot


def print_room(rows, cols, walldict, boxdict, robot):
    room = [["."] * cols for _ in range(rows)]
    for r in walldict:
        for c in walldict[r]:
            room[r][c] = "#"

    for r in boxdict:
        for c in boxdict[r]:
            if p2:
                room[r][c] = "["
                room[r][c + 1] = "]"
            else:
                room[r][c] = "O"

    room[robot[0]][robot[1]] = "@"

    for r in room:
        print("".join(r))


# First: 49ms
@benchmark
def part2(data):
    """Solve part 2."""
    global p2
    p2 = True
    g = []
    for row in data[0]:
        rs = "".join(row)
        rs = rs.replace("#", "##")
        rs = rs.replace("O", "[]")
        rs = rs.replace(".", "..")
        rs = rs.replace("@", "@.")
        g.append(rs)

    G = GridChar("\n".join(g))

    moves: str = data[1]
    walls = G.find_all("#")
    # Just keep track of left side of boxes, but still check for right side later
    boxes = G.find_all("[")
    empty = G.find_all(".")
    robot = G.find_all("@")[0]

    # dicts of walls indexed with row or col
    wdrow = defaultdict(set)
    bdrow = defaultdict(set)
    edrow = defaultdict(set)
    for row, col in walls:
        wdrow[row].add(col)
    for row, col in boxes:
        bdrow[row].add(col)
    for row, col in empty:
        edrow[row].add(col)

    def move_possible(row: int, col: int, drow) -> bool:
        # only viable for vertical movement, default upwards
        if col in wdrow[row + drow] or col + 1 in wdrow[row + drow]:
            # Collision with wall
            return False

        if col in edrow[row + drow] and col + 1 in edrow[row + drow]:
            # Completly empty above
            return True

        if col in bdrow[row + drow]:
            # Perfectly aligned box above
            return move_possible(row + drow, col, drow)

        if col - 1 in bdrow[row + drow]:
            # Right side of box above
            if col + 1 in bdrow[row + drow]:
                # Two boxes above
                return move_possible(row + drow, col - 1, drow) and move_possible(
                    row + drow, col + 1, drow
                )

            return move_possible(row + drow, col - 1, drow)

        # Left side of box above right side of this one
        return move_possible(row + drow, col + 1, drow)

    def move_boxes(row: int, col: int, drow: int):
        # only viable for vertical movement, default upwards
        def move_self():
            edrow[row + drow].remove(col)
            edrow[row + drow].remove(col + 1)
            edrow[row].add(col)
            edrow[row].add(col + 1)

            bdrow[row].remove(col)
            bdrow[row + drow].add(col)

        if col in wdrow[row + drow] or col + 1 in wdrow[row + drow]:
            # Collision with wall
            raise RuntimeError(f"Ran into wall on move {row=}, {col=}, {drow=}")

        if col in edrow[row + drow] and col + 1 in edrow[row + drow]:
            # Completly empty above
            move_self()
            return

        if col in bdrow[row + drow]:
            # Perfectly aligned box above
            move_boxes(row + drow, col, drow)
            move_self()
            return

        if col - 1 in bdrow[row + drow]:
            # Right side of box above
            move_boxes(row + drow, col - 1, drow)

        if col + 1 in bdrow[row + drow]:
            # Left side of box above right side of this one
            move_boxes(row + drow, col + 1, drow)

        move_self()
        return

    def move_robot(dr, dc):
        edrow[robot[0] + dr].remove(robot[1] + dc)
        edrow[robot[0]].add(robot[1])
        return (robot[0] + dr, robot[1] + dc)

    for move in moves:
        # print_room(G.rows, G.cols, wdrow, bdrow, robot)
        # print(move)
        will_move = False
        robrow, robcol = robot
        if move in "<":
            # almost same as p1
            collisionw = 0
            closest_free = 0
            # find closes wall in given direction
            w = wdrow[robot[0]]
            for ww in sorted(list(w)):
                if ww < robot[1] and ww > collisionw:
                    collisionw = ww

            for erow in edrow[robot[0]]:
                if erow < robot[1] and collisionw < erow:
                    will_move = True
                    if erow > closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdrow[robrow]):
                if (
                    box < collisionw
                    or robcol < box
                    or box - 1 not in edrow[robrow]
                    or box < closest_free
                ):
                    continue

                edrow[robrow].remove(box - 1)
                edrow[robrow].add(box + 1)
                bdrow[robrow].remove(box)
                bdrow[robrow].add(box - 1)

                # If a box has moved, we can move as well

            robot = move_robot(0, -1)

        elif move in ">":
            # almost same as p1
            collisionw = float("inf")
            closest_free = float("inf")
            # find closes wall in given direction
            w = wdrow[robot[0]]
            for ww in sorted(list(w)):
                if ww > robot[1] and ww < collisionw:
                    collisionw = ww

            for erow in edrow[robot[0]]:
                if erow > robot[1] and collisionw > erow:
                    will_move = True
                    if erow < closest_free:
                        closest_free = erow

            if not will_move:
                continue

            for box in sorted(bdrow[robrow], reverse=True):
                if (
                    box > collisionw
                    or robcol > box
                    or box + 2 not in edrow[robrow]
                    or box > closest_free
                ):
                    continue

                edrow[robrow].remove(box + 2)
                edrow[robrow].add(box)
                bdrow[robrow].remove(box)
                bdrow[robrow].add(box + 1)

                # If a box has moved, we can move as well

            robot = move_robot(0, 1)

        elif move in "^":
            if robcol in wdrow[robrow - 1]:
                # Walking into wall
                continue
            elif robcol in edrow[robrow - 1]:
                # Moving into empty space
                robot = move_robot(-1, 0)
                continue

            if robcol in bdrow[robrow - 1]:
                # Left side of box above
                if move_possible(robrow - 1, robcol, -1):
                    move_boxes(robrow - 1, robcol, -1)
                    robot = move_robot(-1, 0)

            elif robcol - 1 in bdrow[robrow - 1]:
                # Right side of box above
                if move_possible(robrow - 1, robcol - 1, -1):
                    move_boxes(robrow - 1, robcol - 1, -1)
                    robot = move_robot(-1, 0)

        elif move in "v":
            if robcol in wdrow[robrow + 1]:
                # Walking into wall
                continue
            elif robcol in edrow[robrow + 1]:
                # Moving into empty space
                robot = move_robot(1, 0)
                continue

            if robcol in bdrow[robrow + 1]:
                # Left side of box below
                if move_possible(robrow + 1, robcol, 1):
                    move_boxes(robrow + 1, robcol, 1)
                    robot = move_robot(1, 0)

            elif robcol - 1 in bdrow[robrow + 1]:
                # Right side of box below
                if move_possible(robrow + 1, robcol - 1, 1):
                    move_boxes(robrow + 1, robcol - 1, 1)
                    robot = move_robot(1, 0)

        # end of move loop

    tot = 0
    for row in bdrow:
        for col in bdrow[row]:
            tot += 100 * int(row) + col
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
