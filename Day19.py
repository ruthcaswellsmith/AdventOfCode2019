from __future__ import annotations

from typing import NamedTuple, Tuple
import numpy as np

from intcode import Program
from utils import read_file

SIZE = 50


class XYPair(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return XYPair(self.x + other.x, self.y + other.y)


class TractorBeam:
    def __init__(self, line: str):
        self.line = line
        self.program = Program(line)
        self.grid = np.zeros((SIZE, SIZE), dtype=int)
        self.slope = None
        self.intercept = None

    def test_point(self, x: int, y: int) -> int:
        self.program = Program(self.line)
        for val in [x, y]:
            self.program.add_input_value(val)
        self.program.run()
        return self.program.get_output_value()

    def scan_grid(self):
        for y in range(0, SIZE):
            for x in range(SIZE):
                self.grid[x, y] = self.test_point(x, y)

    def find_location(self):
        # Find lower left corner
        coords = np.argwhere(self.grid == 1)
        bottom_row = coords[coords[:, 0] == 49]
        y = bottom_row[:, 1].min()
        x = 49

        found = False
        while not found:
            x, y = self.get_next_left_bound(x, y)
            if self.test_point(x - 99, y + 99):
                found = True
        return XYPair(x - 99,  y)

    def get_next_left_bound(self, x: int, y: int) -> Tuple:
        for delta in range(2, 10):
            if self.test_point(x + delta, y + 1):
                if not self.test_point(x + delta + 1, y + 1):
                    return x + delta, y + 1
        raise ValueError("Were off the beam.")


def main():
    filename = 'input/Day19.txt'
    data = read_file(filename)

    tractor_beam = TractorBeam(data[0])
    tractor_beam.scan_grid()
    print(f"The answer to Part 1 is {np.sum(tractor_beam.grid)}")

    res = tractor_beam.find_location()
    print(f"The answer to Part 2 is {10_000 * res.x + res.y}")


if __name__ == '__main__':
    main()
