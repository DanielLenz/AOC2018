from typing import Tuple
# from dataclasses import dataclass
from collections import Iterable
import itertools as it

INPUT = 6042


class Powercell:
    def __init__(self, x: int, y: int, serial_number: int) -> None:
        self.x = x
        self.y = y
        self.serial_number = serial_number
        self._rack_id = None
        self._power = None
        self._block_power = 0

    @property
    def rack_id(self):
        if self._rack_id is None:
            self._rack_id = self.x + 10
        return self._rack_id

    @property
    def power(self):
        if self._power is None:
            self._power = (self.rack_id * self.y + self.serial_number) * self.rack_id
            self._power = (self.power // 100) % 10
            self._power -= 5

        return self._power

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, id={self.rack_id}, power={self.power}, block_power={self.block_power})"

    @property
    def block_power(self):
        return self._block_power

    @block_power.setter
    def block_power(self, val):
        self._block_power = val

    def inc_block_power(self, val):
        self.block_power += val


class Grid:
    def __init__(self, serial_number: int, width: int=300, height: int=300):
        self.serial_number = serial_number
        self.height = height
        self.width = width
        self.build_cells()
    
    def build_cells(self):
        self.cells = [[None for x in range(self.width)] for y in range(self.height)]
        for x, y in it.product(range(self.width), range(self.height)):
            self.cells[x][y] = Powercell(x+1, y+1, self.serial_number)

    def calc_block_powers(self, blocksize=3):
        self.blockpowers = [[0 for i in range(self.width)] for j in range(self.height)] 
        for i, j in it.product(range(self.width), range(self.height)):
                # If edge cell, set to -inf
                if self.cells[i][j].x > (self.width - blocksize) or self.cells[i][j].y > (self.height - blocksize):
                    self.blockpowers[i][j] = float('-inf')
                # Else add value to all cells in block
                else:
                    for di, dj in it.product(range(blocksize), repeat=2):
                        self.blockpowers[i-di][j-dj] += self.cells[i][j].power

    def find_maxpower_block(self):
        flatcells = [cell for row in self.cells for cell in row]
        flatblockpowers = [cell for row in self.blockpowers for cell in row]

        maxpower = max(flatblockpowers)
        maxcell = flatcells[flatblockpowers.index(maxpower)]

        return maxcell, maxpower


def find_best_gridsize(grid: Grid) -> Tuple[Powercell, int, int]:
    blocksizes = range(1, 15)
    maxpower = float('-inf')
    maxblocksize = -1

    for blocksize in blocksizes:
        print(f"Testing blocksize {blocksize} of {blocksizes[-1]}...")
        grid.calc_block_powers(blocksize)
        cell, power = grid.find_maxpower_block()

        if power > maxpower:
            maxpower = power
            maxcell = cell
            maxblocksize = blocksize

    return maxcell, maxpower, maxblocksize

if __name__ == "__main__":
    testcells = [
        Powercell(*p)
        for p in [[3, 5, 8], [122, 79, 57], [217, 196, 39], [101, 153, 71]]
    ]

    testpowers = [4, -5, 0, 4]

    for cell, power in zip(testcells, testpowers):
        assert cell.power == power

    # testgrids = [Grid(18), Grid(42)]
    # test_blockpowers = [(33, 45), (21, 61)]

    # for g, b in zip(testgrids, test_blockpowers):
    #     g.calc_block_powers()
    #     max_cell, _ = g.find_maxpower_block()

    #     assert b == (max_cell.x, max_cell.y)

    # grid = Grid(6042)
    # grid.calc_block_powers()

    # max_cell, _ = grid.find_maxpower_block()
    # print(max_cell)

    # Part 2
    ########

    grid = Grid(6042)
    print(find_best_gridsize(grid))
