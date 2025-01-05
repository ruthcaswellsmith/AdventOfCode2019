from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from utils import read_file


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)

    def move(self, delta: 'Delta') -> 'Point':
        return Point(self.x + delta.dx, self.y + delta.dy)


@dataclass(frozen=True)
class Delta:
    dx: int
    dy: int


class Direction:
    DELTAS = {
        'L': Delta(-1, 0),
        'R': Delta(1, 0),
        'U': Delta(0, -1),
        'D': Delta(0, 1)
    }

    @classmethod
    def get(cls, direction: str) -> Delta:
        if direction not in cls.DELTAS:
            raise ValueError(f"Invalid direction: {direction}")
        return cls.DELTAS[direction]


class Wire:
    def __init__(self, line: str):
        self.moves = [(m[0], int(m[1:])) for m in line.split(',')]
        self.path: Dict[Point, int] = {}
        self._trace_path()

    def _trace_path(self):
        current = Point(0, 0)
        steps = 0
        for move in self.moves:
            delta = Direction.get(move[0])
            for step in range(1, move[1] + 1):
                steps += 1
                current = current.move(delta)
                if current not in self.path:
                    self.path[current] = steps

    def get_intersections(self, other: Wire):
        return set(self.path.keys() & other.path.keys())


def find_closest_intersection(wire1: Wire, wire2: Wire) -> int:
    return min(
        point.manhattan_distance()
        for point in wire1.get_intersections(wire2)
    )


def find_shortest_path_intersection(wire1: Wire, wire2: Wire) -> int:
    return min(
        wire1.path[point] + wire2.path[point]
        for point in wire1.get_intersections(wire2)
    )


def main():
    filename = 'input/Day3.txt'
    data = read_file(filename)

    wire1 = Wire(data[0])
    wire2 = Wire(data[1])

    print(f"The answer to part 1 is {find_closest_intersection(wire1, wire2)}")
    print(f"The answer to part 2 is {find_shortest_path_intersection(wire1, wire2)}")


if __name__ == '__main__':
    main()
