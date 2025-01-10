from __future__ import annotations

from typing import NamedTuple
from enum import Enum
import numpy as np

from utils import read_file
from intcode import Program, Status


class XYPair(NamedTuple):
    x: int
    y: int

    def move(self, direction: Direction) -> XYPair:
        return XYPair(self.x + direction.value.x, self.y + direction.value.y)


class Turn(Enum):
    LEFT = 0
    RIGHT = 1


class Direction(XYPair, Enum):
    UP = XYPair(0, -1)
    RIGHT = XYPair(1, 0)
    DOWN = XYPair(0, 1)
    LEFT = XYPair(-1, 0)

    @property
    def as_complex(self) -> complex:
        return complex(self.value[0], self.value[1])

    def turn(self, turn: Turn) -> Direction:
        res = complex(0, -1) * self.as_complex if \
            turn == Turn.LEFT else complex(0, 1) * self.as_complex
        return Direction(XYPair(int(res.real), int(res.imag)))


class Robot:
    def __init__(self, line: str):
        self.direction = Direction.UP
        self.pos = XYPair(0, 0)
        self.painted = {}
        self.brain = Program(line)

    @property
    def color_of_panel(self):
        return self.painted.get(self.pos, 0)

    def process_input(self, input_value: int):
        self.brain.add_input_value(input_value)
        self.brain.run()

    def get_result(self) -> XYPair:
        return XYPair(self.brain.get_output_value(), self.brain.get_output_value())

    def process_result(self, value: XYPair):
        self.painted[self.pos] = value.x
        self.direction = self.direction.turn(Turn(value.y))
        self.pos = self.pos.move(self.direction)

    def display_painted_tiles(self):
        max_x = max(self.painted.keys(), key=lambda point: point.x).x
        max_y = max(self.painted.keys(), key=lambda point: point.y).y
        grid = np.zeros((max_x + 1, max_y + 1), dtype=int)
        for xypair, color in self.painted.items():
            grid[xypair.x, xypair.y] = color
        [print(" ".join([str(ele) if ele == 1 else '.' for ele in grid.T[i, :]])) for i in range(grid.T.shape[0])]


def main():
    filename = 'input/Day11.txt'
    data = read_file(filename)

    robot = Robot(data[0])
    robot.process_input(0)
    while robot.brain.status != Status.TERMINATED:
        robot.process_result(robot.get_result())
        robot.process_input(robot.color_of_panel)
    print(f"The number of painted tiles is {len(robot.painted)}")

    robot = Robot(data[0])
    robot.process_input(1)
    while robot.brain.status != Status.TERMINATED:
        robot.process_result(robot.get_result())
        robot.process_input(robot.color_of_panel)
    robot.display_painted_tiles()


if __name__ == '__main__':
    main()
