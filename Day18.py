from __future__ import annotations

from collections import defaultdict, deque
from typing import List, Tuple, Dict
import heapq
from functools import lru_cache

import numpy as np

from utils import read_file, Part


class Maze:
    def __init__(self, data: List[str]):
        self.data = data
        self.num_rows, self.num_cols = len(data), len(data[0])
        self.grid = np.array([list(string) for string in data])
        self.graph = defaultdict(set)
        self.nodes = []
        self.start, self.keys, self.doors = [], {}, {}
        self.build_graph()

    def is_on_grid(self, x: int, y: int) -> bool:
        return True if 0 <= x < self.num_rows and 0 <= y < self.num_cols else False

    def build_graph(self):
        for row, line in enumerate(self.grid):
            for col, ele in enumerate(line):
                char = self.grid[row, col]
                if char != '#':
                    node = (row, col)
                    self.nodes.append(node)
                    if char == '@':
                        self.start.append((row, col))
                    elif char.isupper():
                        self.doors[(row, col)] = str(char)
                    elif char.islower():
                        self.keys[(row, col)] = str(char)
                    for deltas in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        n_x, n_y = row + deltas[0], col + deltas[1]
                        if self.is_on_grid(n_x, n_y) and self.grid[n_x, n_y] != '#':
                            self.graph[node].add((n_x, n_y))
                            self.graph[n_x, n_y].add(node)

    @lru_cache
    def get_reachable_keys(self, pos: Tuple, keys) -> Dict:
        """
        pos: current position
        keys: a frozenset of keys we are holding
        returns a dictionary {key: distance}
        """

        q = deque()
        q.append((pos, 0))
        visited = set()
        reachable_keys = {}

        while q:
            pos, dist = q.popleft()
            visited.add(pos)

            for n in self.graph[pos]:
                if n not in visited:
                    visited.add(n)

                    if n in self.doors and not self.doors[n].lower() in keys:
                        continue

                    if n in self.keys and not self.keys[n] in keys:
                        reachable_keys[self.keys[n]] = (n, dist + 1)
                        continue
                    q.append((n, dist + 1))

        return reachable_keys

    def find_shortest_path(self) -> int:
        """Dijkstra for upper level search
        returns minimum distance to any position where we are holding all keys
        priority queue holds current distance and a tuple which is (pos, set of keys)
        we are holding)"""

        visited = set()
        priority_queue = [(0, (tuple(self.start), frozenset()))]
        distances = {(tuple(self.start), frozenset()): 0}

        while priority_queue:
            dist, (pos, keys) = heapq.heappop(priority_queue)
            if len(keys) == len(self.keys):
                return dist

            if (pos, keys) in visited:
                continue
            visited.add((pos, keys))

            for i, p in enumerate(pos):
                for key, (new_p, key_dist) in self.get_reachable_keys(p, keys).items():
                    new_keys = frozenset(keys | {key})
                    new_dist = dist + key_dist
                    new_pos = pos[:i] + (new_p,) + pos[i+1:]

                    if (new_pos, new_keys) not in visited and new_dist < distances.get((new_pos, new_keys), float('inf')):
                        distances[(new_pos, new_keys)] = new_dist
                        heapq.heappush(priority_queue, (new_dist, (new_pos, new_keys)))

    def update_for_part2(self):
        orig_start = self.start[0]
        new_walls = [orig_start,
                     (orig_start[0] + 1, orig_start[1]),
                     (orig_start[0] - 1, orig_start[1]),
                     (orig_start[0], orig_start[1] + 1),
                     (orig_start[0], orig_start[1] - 1),
                     ]
        for wall in new_walls:
            self.nodes.remove(wall)
            del self.graph[wall]
            for node, adj_list in self.graph.items():
                if wall in adj_list:
                    adj_list.remove(wall)
            self.start = [
                (orig_start[0] + 1, orig_start[1] + 1),
                (orig_start[0] + 1, orig_start[1] - 1),
                (orig_start[0] - 1, orig_start[1] + 1),
                (orig_start[0] - 1, orig_start[1] - 1),
            ]


def main():
    filename = 'input/Day18.txt'
    data = read_file(filename)
    maze = Maze(data)
    print(f"The shortest path is {maze.find_shortest_path()}")

    maze = Maze(data)
    maze.update_for_part2()
    print(f"The shortest path is {maze.find_shortest_path()}")


if __name__ == '__main__':
    main()
