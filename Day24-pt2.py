from __future__ import annotations

from typing import List
from collections import defaultdict
import numpy as np
from dataclasses import dataclass
from copy import deepcopy

from utils import read_file


NEIGHBORS = defaultdict(list)
for i in range(1, 26):
    if i == 13:
        continue
    for n in [+1, -1, +5, -5]:
        new_pos = i + n
        if 0 < new_pos < 26 and new_pos != 13:
            NEIGHBORS[i].append((new_pos, 0))

for i in range(1, 5):
    NEIGHBORS[5*i].remove((5*i + 1, 0))
for i in range(1, 5):
    NEIGHBORS[5*i + 1].remove((5*i, 0))

# Add neighbors from level -1
for i in range(1, 6):
    NEIGHBORS[i].append((8, -1))
for i in range(21, 26):
    NEIGHBORS[i].append((18, -1))
for i in [1, 6, 11, 16, 21]:
    NEIGHBORS[i].append((12, -1))
for i in [5, 10, 15, 20, 25]:
    NEIGHBORS[i].append((14, -1))

# Add neighbors from level 1
for i in range(1, 6):
    NEIGHBORS[8].append((i, 1))
for i in range(21, 26):
    NEIGHBORS[18].append((i, 1))
for i in range(5):
    NEIGHBORS[12].append((5*i + 1, 1))
for i in range(1, 6):
    NEIGHBORS[14].append((5*i, 1))


@dataclass
class Bitmask:
    num: int

    def set_bit(self, n: int) -> Bitmask:
        return Bitmask(self.num | (1 << n))

    def clear_bit(self, n: int) -> Bitmask:
        return Bitmask(self.num & ~(1 << n))

    def toggle_bit(self, n: int) -> Bitmask:
        return Bitmask(self.num ^ (1 << n))

    def is_bit_set(self, n: int) -> bool:
        return (self.num & (1 << n)) != 0

    def num_bits_set(self) -> int:
        return bin(self.num).count('1')


class Eris:
    def __init__(self, data: List[str]):
        t = '0'
        for row, line in enumerate(data):
            for col, ele in enumerate(line):
                t = ('1' if ele == '#' else '0') + t
        self.bugs = {
            0: Bitmask(int(t, 2)),
        }

    def sum_neighbors(self, level: int, pos: int) -> np.array:
        return sum([self.bugs.get(level + l, Bitmask(0)).is_bit_set(p) for p, l in NEIGHBORS[pos]])

    def process(self, num_minutes):
        for _ in range(num_minutes):
            self.process_minute()

    def process_minute(self):
        min_level, max_level = min(self.bugs.keys()) - 1, max(self.bugs.keys()) + 1
        for level in [min_level, max_level]:
            self.bugs[level] = Bitmask(0)

        # Now process each level starting at lowest
        new_bugs = deepcopy(self.bugs)
        for level in range(min_level, max_level + 1):
            bitmask = self.bugs[level]
            for pos in range(1, 26):
                if pos == 13:
                    continue
                neighbors = self.sum_neighbors(level, pos)
                if bitmask.is_bit_set(pos) and neighbors != 1:
                    new_bugs[level] = new_bugs[level].toggle_bit(pos)
                elif not bitmask.is_bit_set(pos) and neighbors in [1, 2]:
                    new_bugs[level] = new_bugs[level].toggle_bit(pos)
        self.bugs = new_bugs

        # If no bugs in the new levels delete them
        for level in [min_level, max_level]:
            if self.bugs[level] == Bitmask(0):
                del self.bugs[level]


def main():
    filename = 'input/Day24.txt'
    data = read_file(filename)

    eris = Eris(data)
    eris.process(200)
    print(f"The number of bugs is {sum([bug.num_bits_set() for bug in eris.bugs.values()])}")


if __name__ == '__main__':
    main()
