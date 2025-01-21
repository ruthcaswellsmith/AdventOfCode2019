from __future__ import annotations

from enum import Enum
from typing import NamedTuple, List, Dict, Union

import numpy as np

from intcode import Program, Status
from utils import read_file

SIZE = 50


class XYPair(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return XYPair(self.x + other.x, self.y + other.y)

    def get_direction_to_travel(self, other) -> Direction:
        return Direction.DOWN if other.x > self.x else \
            Direction.UP if other.x < self.x else \
            Direction.RIGHT if other.y > self.y else \
            Direction.LEFT


class Turn(str, Enum):
    LEFT = 'L'
    RIGHT = 'R'


class Direction(str, Enum):
    # format (symbol, deltas)
    UP = ('^', XYPair(-1, 0))
    RIGHT = ('>', XYPair(0, 1))
    DOWN = ('v', XYPair(1, 0))
    LEFT = ('<', XYPair(0, -1))

    def __new__(cls, value: int, deltas: XYPair):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.deltas = deltas
        return obj

    def get_direction_to_turn(self, other) -> Union[None, Turn]:
        return None if self == other else \
            {
                (Direction.UP, Direction.RIGHT): Turn.RIGHT,
                (Direction.UP, Direction.LEFT): Turn.LEFT,
                (Direction.DOWN, Direction.RIGHT): Turn.LEFT,
                (Direction.DOWN, Direction.LEFT): Turn.RIGHT,
                (Direction.RIGHT, Direction.DOWN): Turn.RIGHT,
                (Direction.RIGHT, Direction.UP): Turn.LEFT,
                (Direction.LEFT, Direction.DOWN): Turn.LEFT,
                (Direction.LEFT, Direction.UP): Turn.RIGHT,
            }[(self, other)]

    def get_next_pos(self, pos: XYPair) -> XYPair:
        return XYPair(pos.x + self.deltas.x, pos.y + self.deltas.y)


class ASCII:
    def __init__(self, line: str):
        self.program = Program(line)
        self.grid = np.zeros((SIZE, SIZE), dtype=int)
        self.robot_pos, self.robot_dir = None, None
        self._populate_grid()
        self.nodes = self._build_graph()
        self.intersections = [xypair for xypair, adj_list in self.nodes.items() if len(adj_list) == 4]
        self.start = self.robot_pos
        self.end = [xypair for xypair, adj_list in self.nodes.items() if \
                    len(adj_list) == 1 and xypair != self.robot_pos][0]
        self.visited = set()

    @property
    def answer_pt1(self):
        return sum([pair.x * pair.y for pair in self.intersections])

    def _populate_grid(self):
        self.program.run()
        i, j = 0, 0
        while self.program.outputs:
            val = self.program.get_output_value()
            if val == 10:
                i += 1
                j = 0
            else:
                self.grid[i, j] = 1 if val != 46 else 0
                if val not in [35, 46]:
                    self.robot_pos = XYPair(i, j)
                    self.robot_dir = Direction(chr(val))
                j += 1

    def _build_graph(self) -> Dict[XYPair, List[XYPair]]:
        nodes = {}
        for pos in [XYPair(int(x), int(y)) for x, y in np.argwhere(self.grid == 1)]:
            adj_list = []
            for d in Direction:
                n = XYPair(pos.x + d.deltas.x, pos.y + d.deltas.y)
                if self.grid[n.x, n.y] == 1:
                    adj_list.append(n)
            nodes[pos] = adj_list
        return nodes

    def find_path(self):
        pos, direction, movements = self.robot_pos, self.robot_dir, []
        path = [pos]
        prev, steps = None, 0
        movement = ''
        while pos != self.end:
            neighbors = self.nodes[pos]
            if len(neighbors) == 1:
                n = neighbors[0]
            elif len(neighbors) == 2:
                # We have no choice but to continue (may involve a turn or not)
                n = [n for n in neighbors if n != prev][0]
            else:
                # We are at an intersection; we know we can just go straight
                n = direction.get_next_pos(pos)

            # Now we know where we are going
            prev = pos
            pos = n
            path.append(pos)
            if prev.get_direction_to_travel(pos) == direction:
                steps += 1
            else:
                new_direction = prev.get_direction_to_travel(pos)
                if steps > 0:
                    movement += str(steps)
                    movements.append(movement)
                movement = direction.get_direction_to_turn(new_direction).value
                direction = new_direction
                steps = 1

        movement += str(steps)
        movements.append(movement)
        return movements

    def encapsulate_movements(self, movements: List[str]):
        functions = self.get_functions(movements)

        if not functions:
            print(f"We haven't found our functions.  Exiting")
            exit()

        movements_str = " ".join(movements)
        main_routine = movements_str
        for function, string in functions.items():
            main_routine = main_routine.replace(string, function)

        main_routine = self.reformat_str(main_routine)
        functions = {key: self.reformat_str(val) for key, val in functions.items()}
        return main_routine, functions

    @staticmethod
    def reformat_str(string: str) -> str:
        string = string.replace('R', 'R,').replace('L', 'L,')
        string = ",".join(string.split(' '))
        return string

    @staticmethod
    def get_functions(movements: List[str]) -> Dict:
        """Strategy is to first find an A. It can at most be 7 instructions long but must
        be no more than 20 characters in total inc. commas.  I'm going to also assume every function
        must be at least 3 instructions long and must repeat at least 3 times.
        After we find a possible A, we try to find all possible B's,
        then see if we can find a C that works."""

        movements_str = ' '.join(movements)

        functions = {}
        for a in [movements[:i] for i in range(7, 3, -1)]:
            functions['A'] = " ".join(a)
            new_movements_str = movements_str
            if len(",".join(a)) > 20 or new_movements_str.count(" ".join(a)) < 3:
                continue
            new_movements_str = new_movements_str.replace(" ".join(a), "-")
            movements_a = [p.strip() for p in new_movements_str.split('-') if p.strip()]

            # Now look at first element and see if this could be B
            b = movements_a[0]
            functions['B'] = b
            if len(','.join(b.split(' '))) > 20:
                # we'll have to try splitting this into b and c
                print(f"We need smarter code because possible b is too long.")
                exit()
            if len(b.split(' ')) < 3:
                # we need a different a
                continue
            # remove b from movements
            new_movements_str = new_movements_str.replace(b, "-")
            new_movements = [p.strip() for p in new_movements_str.split('-') if p.strip()]

            # Now first element can be c and if that covers everything
            c = new_movements[0]
            functions['C'] = c
            if len(','.join(c.split(' '))) > 20 or len(c.split(' ')) < 3:
                # we need a different a
                continue
            new_movements_str = new_movements_str.replace(c, "-")
            new_movements = [p.strip() for p in new_movements_str.split('-') if p.strip()]

            if not new_movements:
                return functions
            continue

    def execute_movements(self, main_routine, functions):
        self.program.reset()
        self.program.memory[0] = 2
        self.program.run()

        for ch in main_routine:
            self.program.add_input_value(ord(ch))
        self.program.add_input_value(10)
        self.program.run()

        for function in functions:
            for ch in functions[function]:
                self.program.add_input_value(ord(ch))
            self.program.add_input_value(10)
            self.program.run()

        self.program.add_input_value(ord('n'))
        self.program.add_input_value(10)
        self.program.run()
        return self.program.outputs[-1]


def main():
    filename = 'input/Day17.txt'
    data = read_file(filename)

    ascii = ASCII(data[0])
    print(f"The answer to Part 1 is {ascii.answer_pt1}")

    movements = ascii.find_path()
    main_routine, functions = ascii.encapsulate_movements(movements)
    res = ascii.execute_movements(main_routine, functions)
    print(f"The vacuum robot collected {res} dust.")


if __name__ == '__main__':
    main()
