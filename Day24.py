from __future__ import annotations

from typing import List
import numpy as np

from utils import read_file

SIZE = 5


class Eris:
    def __init__(self, data: List[str]):
        self.grid = np.array([[int(ele == '#') for ele in line] for line in data])
        self.layouts = []

    def sum_neighbors(self) -> np.array:
        """This zero-pads the array and shifts it in each direction, then
        sums the neighbors"""
        shifted_left = np.hstack((self.grid, np.zeros((SIZE, 1), dtype=int)))[:, 1:]
        shifted_right = np.hstack((np.zeros((SIZE, 1), dtype=int), self.grid))[:, :SIZE]
        shifted_up = np.vstack((self.grid, np.zeros((1, SIZE), dtype=int)))[1:]
        shifted_down = np.vstack((np.zeros((1, SIZE), dtype=int), self.grid))[:SIZE]
        return shifted_left + shifted_right + shifted_up + shifted_down

    def get_biodiversity(self):
        biodiversity = 0
        res = np.argwhere(self.grid == 1)
        for row, col in res:
            ind = SIZE * row + (col + 1)
            biodiversity += 2 ** (ind- 1)
        return biodiversity

    def process(self):
        done = False
        while not done:
            self.layouts.append(self.grid)
            self.process_minute()
            for layout in self.layouts:
                if np.array_equal(layout, self.grid):
                    done = True

    def process_minute(self):
        neighbors = self.sum_neighbors()
        self.grid = ((self.grid == 1) & (neighbors == 1)) | ((self.grid == 0) & np.isin(neighbors, [1, 2]))


def main():
    filename = 'input/Day24.txt'
    data = read_file(filename)

    eris = Eris(data)
    eris.process()
    print(f"The biodiversity of the first repeating layout is {eris.get_biodiversity()}")


if __name__ == '__main__':
    main()
