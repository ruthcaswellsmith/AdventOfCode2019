from __future__ import annotations

from enum import Enum
from typing import NamedTuple
import numpy as np

from intcode import Program
from utils import read_file

SIZE = 50


class XYPair(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return XYPair(self.x + other.x, self.y + other.y)


class Direction(int, Enum):
    # format (command, deltas)
    NORTH = (1, XYPair(0, -1))
    SOUTH = (2, XYPair(0, 1))
    WEST = (3, XYPair(-1, 0))
    EAST = (4, XYPair(1, 0))

    def __new__(cls, value: int, deltas: XYPair):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.deltas = deltas
        return obj

    def opposite(self):
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST
        }
        return opposites[self]


class StatusCode(int, Enum):
    WALL = 0
    SPACE = 1
    OXYGEN_TANK = 2


class Grid:
    def __init__(self, line: str):
        self.droid = Program(line)
        self.grid = np.zeros((SIZE, SIZE), dtype=int)
        self.visited = set()
        self.tank_pos, self.distance_to_tank = None, None

    def find_oxygen_tank(self):
        inital_pos = XYPair(0, 0)
        self.visited.add(inital_pos)
        self.explore(inital_pos)

    def explore(self, pos: XYPair, direction: Direction = None, level: int = 1):
        directions_to_explore = [d for d in Direction if pos + d.deltas not in self.visited]
        for d in directions_to_explore:
            new_pos = pos + d.deltas
            self.visited.add(new_pos)
            status_code = self.execute_command(d)
            if status_code == StatusCode.WALL:
                self.grid[(new_pos.x + SIZE//2, new_pos.y + SIZE//2)] = 1
            elif status_code in [StatusCode.SPACE, StatusCode.OXYGEN_TANK]:
                if status_code == StatusCode.OXYGEN_TANK:
                    self.distance_to_tank = level
                    self.tank_pos = XYPair(new_pos.x + SIZE//2, new_pos.y + SIZE//2)
                    self.grid[(new_pos.x + SIZE//2, new_pos.y + SIZE//2)] = 2
                self.explore(new_pos, d, level + 1)
            else:
                raise ValueError(f"Unexpected Status Code!")

        if level > 1:
            # We're backing up so this should return a space
            status_code = self.execute_command(direction.opposite())
            if status_code != StatusCode.SPACE:
                raise ValueError(f"No space to back up!")

    def fill_with_oxygen(self):
        self.visited = set()
        self.visited.add(self.tank_pos)
        return self.flood_fill(self.tank_pos)

    def flood_fill(self, pos: XYPair, minutes: int = 0) -> int:
        directions_to_explore = [d for d in Direction if pos + d.deltas not in self.visited]
        levels = []
        if not directions_to_explore:
            return minutes
        for d in directions_to_explore:
            new_pos = pos + d.deltas
            self.visited.add(new_pos)
            if self.grid[new_pos] == 1:
                levels.append(minutes)
            else:
                levels.append(self.flood_fill(new_pos, minutes + 1))
        return max(levels)

    def execute_command(self, direction: Direction) -> StatusCode:
        self.droid.add_input_value(direction.value)
        self.droid.run()
        return StatusCode(self.droid.get_output_value())


def main():
    filename = 'input/Day15.txt'
    data = read_file(filename)

    grid = Grid(data[0])
    grid.find_oxygen_tank()
    print(f"The distance to the tank is {grid.distance_to_tank}")

    minutes = grid.fill_with_oxygen()
    print(f"It will take {minutes} minutes to fill with oxygen.")


if __name__ == '__main__':
    main()
