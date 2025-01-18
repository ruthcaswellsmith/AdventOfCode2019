from __future__ import annotations

from collections import defaultdict, deque
from typing import List, Union

import numpy as np

from utils import read_file, Part


class Maze:
    def __init__(self, data: List[str]):
        self.data = data
        self.num_rows, self.num_cols = len(data), len(data[0])
        self.start, self.end = None, None
        self.grid = np.array([list(string) for string in data])
        self.portals = defaultdict(list)
        self.get_portals()
        self.get_portals(transpose=True)
        self.portals_lookup = self.transform_portals()
        self.graph = self.build_graph()

    def is_on_grid(self, x: int, y: int):
        return True if 0 <= x < self.num_rows and 0 <= y < self.num_cols else False

    def build_graph(self):
        graph = defaultdict(set)
        for row, line in enumerate(self.grid):
            for col, ele in enumerate(line):
                if self.grid[row, col] == '.':
                    for deltas in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        n_x, n_y = row + deltas[0], col + deltas[1]
                        if self.is_on_grid(n_x, n_y) and self.grid[n_x, n_y] == '.':
                            graph[row, col].add((n_x, n_y))
                            graph[n_x, n_y].add((row, col))
        return graph

    def transform_portals(self):
        portals_lookup = {}
        for portal, points in self.portals.items():
            pt1, pt2 = points[0], points[1]
            if pt1[0] == 2 or pt1[0] == self.num_rows - 3 or pt1[1] == 2 or pt1[1] == self.num_cols - 3:
                portals_lookup[pt1] = ('OUTER', pt2)
                portals_lookup[pt2] = ('INNER', pt1)
            else:
                portals_lookup[pt2] = ('OUTER', pt1)
                portals_lookup[pt1] = ('INNER', pt2)
        return portals_lookup

    @staticmethod
    def is_portal(chunk: str) -> bool:
        return True if all([chunk[0].isalpha(), chunk[1].isalpha(), chunk[2] == '.']) else False

    def identify_portal(self, chunk: str) -> Union[None, str]:
        return 'L' if self.is_portal(chunk) else 'R' if self.is_portal(chunk[::-1]) else None

    def add_portal(self, chunk: str, x: int, y: int):
        name = "".join(chunk[:2])
        if name == 'AA':
            self.start = (x, y)
        elif name == 'ZZ':
            self.end = (x, y)
        else:
            self.portals[name].append((x, y))

    def get_portals(self, transpose=False):
        grid = self.grid.T if transpose else self.grid

        for x in range(grid.shape[0]):
            for y in range(grid.shape[1] - 2):
                chunk = grid[x, y:y + 3]
                portal = self.identify_portal(chunk)
                if portal:
                    coords = (
                        (y + 2 if portal == 'L' else y) if transpose else x,
                        x if transpose else (y + 2 if portal == 'L' else y)
                    )
                    self.add_portal(
                        chunk[:2] if portal == 'L' else chunk[::-1][:2][::-1],
                        coords[0],
                        coords[1]
                    )

    def find_shortest_path(self, part: Part, max_depth=30):
        q = deque()
        q.append((self.start, 0, [(self.start, 0)]))
        visited = set()

        while q:
            node, level, path = q.popleft()
            visited.add((node, level))

            if node == self.end:
                return len(path)

            neighbors = [(node, level) for node in self.graph[node] if not (node in [self.start, self.end] and level > 0)]
            if node in self.portals_lookup:
                portal_type, dest = self.portals_lookup[node]
                if part == Part.PT1:
                    neighbors.append((dest, level))
                else:
                    if level > 0 and portal_type == 'OUTER':
                        neighbors.append((dest, level - 1))
                    elif portal_type == 'INNER' and level < max_depth:
                        neighbors.append((dest, level + 1))
            for n, level in neighbors:
                if (n, level) not in visited:
                    q.append((n, level, (path + [(n, level)])))


def main():
    filename = 'input/Day20.txt'
    data = read_file(filename)
    maze = Maze(data)
    print(f"The shortest path is {maze.find_shortest_path(Part.PT1) - 1}")

    print(f"The shortest path is {maze.find_shortest_path(Part.PT2) - 1}")


if __name__ == '__main__':
    main()
