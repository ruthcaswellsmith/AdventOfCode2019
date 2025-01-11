from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Tuple

import numpy as np

from intcode import Program, Status
from utils import read_file


class XYPair(NamedTuple):
    x: int
    y: int


class Tile(int, Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Arcade:
    def __init__(self, line: str):
        self.program = Program(line)
        self.grid = np.zeros((36, 24), dtype=int)
        self.score = 0

    @property
    def ball_position(self) -> Tuple[int, int]:
        return tuple([int(i) for i in np.argwhere(self.grid == Tile.BALL.value)[0]])

    @property
    def paddle_position(self) -> Tuple[int, int]:
        return tuple([int(i) for i in np.argwhere(self.grid == Tile.PADDLE.value)[0]])

    def get_joystick_position(self):
        """Move towards the ball"""
        return -1 if self.ball_position[0] < self.paddle_position[0] \
            else 1 if self.ball_position[0] > self.paddle_position[0] \
            else 0

    def run(self):
        self.program.run()
        while self.program.outputs:
            pos = XYPair(self.program.get_output_value(), self.program.get_output_value())
            if pos == XYPair(-1, 0):
                self.score = self.program.get_output_value()
            else:
                tile = Tile(self.program.get_output_value())
                self.grid[pos.x, pos.y] = tile.value

    def play_game(self):
        """Set it up so we can play for free and set up the board"""
        self.program.memory[0] = 2
        self.run()
        while self.program.status not in [Status.TERMINATED]:
            self.program.add_input_value(self.get_joystick_position())
            self.run()


def main():
    filename = 'input/Day13.txt'
    data = read_file(filename)

    arcade = Arcade(data[0])
    arcade.run()
    print(f"The number of block tiles is {sum(sum(arcade.grid == Tile.BLOCK.value))}")

    arcade = Arcade(data[0])
    arcade.play_game()
    print(f"The final score is {arcade.score}")


if __name__ == '__main__':
    main()
