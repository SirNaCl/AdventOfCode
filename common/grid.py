from abc import ABC
from itertools import product
from networkx import (
    Graph,
    grid_2d_graph,
    shortest_path,
)

import common.parsing

GRID_VALUE = "val"


class GridBase(ABC):
    def __init__(self, grid):
        self.grid = grid

    def neighbours_idx(self, row, col):
        r_itr = {0}
        if row < self.rows:
            r_itr.add(1)
        if row > 0:
            r_itr.add(-1)

        c_itr = {0}
        if col < self.cols:
            c_itr.add(1)
        if col > 0:
            c_itr.add(-1)

        itr = set(product(r_itr, c_itr))
        itr.remove((0, 0))

        return [(row + r, col + c) for r, c in itr]

    def neighbours(self, row, col):
        return [self.grid[r][c] for r, c in self.neighbours_idx(row, col)]

    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0])

    def __getitem__(self, idx):
        return self.grid[idx]

    def __eq__(self, rhs) -> bool:
        if self.rows != rhs.rows or self.cols != rhs.cols:
            return False
        return all(
            self[r][c] == rhs[r][c] for r in range(self.rows) for c in range(self.cols)
        )

    def find_all(self, target):
        coords = []
        for ri in range(self.rows):
            for ci in range(self.cols):
                if self.grid[ri][ci] == target:
                    coords.append((ri, ci))
        return coords

    def replace(self, target, value):
        for row, col in self.find_all(target):
            self.grid[row][col] = value

    def to_graph(self, ignore=[], orthogonal=True) -> Graph:
        g = grid_2d_graph(self.rows, self.cols)

        if not orthogonal:
            g.add_edges_from(
                [
                    ((r, c), (r + 1, c + 1))
                    for c in range(self.cols - 1)
                    for r in range(self.rows - 1)
                ]
                + [
                    ((r + 1, c), (r, c + 1))
                    for c in range(self.cols - 1)
                    for r in range(self.rows - 1)
                ]
            )

        for n in list(g):
            nrow, ncol = n
            if self.grid[nrow][ncol] in ignore:
                g.remove_node(n)
                continue
            g.nodes[n][GRID_VALUE] = self.grid[nrow][ncol]
        return g

    def shortest_path(self, source: tuple, target: tuple, ignore=[], orthogonal=True):
        g = self.to_graph(ignore, orthogonal)
        return shortest_path(g, source, target)

    def shortest_path_only_source(self, source, ignore=[], orthogonal=True):
        g = self.to_graph(ignore, orthogonal)
        return shortest_path(g, source)


class GridInt(GridBase):
    def __init__(self, data: str, separator=None):
        if separator is None:
            g = [[int(c) for c in row] for row in data.split("\n")]
        else:
            g = [[int(c) for c in row.split(separator)] for row in data.split("\n")]
        super().__init__(g)

    def copy(self):
        n = GridInt("1")
        n.grid = [r.copy() for r in self.grid]
        return n


class GridChar(GridBase):
    def __init__(self, data, separator=None):
        if separator is None:
            g = [[c for c in row] for row in data.split("\n")]
        else:
            g = [[c for c in row.split(separator)] for row in data.split("\n")]
        super().__init__(g)

    def copy(self):
        n = GridChar("")
        n.grid = [r.copy() for r in self.grid]
        return n


TEST_DATA = """\
1 2 3
4 5 6
7 8 9\
"""

TEST_DATA2 = """\
123
456
789\
"""

if __name__ == "__main__":
    G = GridInt(TEST_DATA, " ")
    # Should contain every number except 5 (secret of sudoku btw)
    assert sum(G.neighbours(1, 1)) == 40
    assert G[1][1] == 5
    assert G.find_all(5) == [(1, 1)]
    assert len(G.to_graph([5]).nodes) == 8
    assert len(G.to_graph(orthogonal=False)[(0, 0)]) == 3
    assert len(G.to_graph(orthogonal=True)[(0, 0)]) == 2
    # shortest path includes source and target
    assert len(G.shortest_path((0, 0), (2, 2))) == 5
    assert len(G.shortest_path((0, 0), (2, 2), orthogonal=False)) == 3
    G.replace(4, 5)
    assert G[1][0] == 5
    c = G.copy()
    G[1][0] = 4
    assert c[1][0] == 5
    # No separator = split all chars
    assert G == GridInt(TEST_DATA2)
