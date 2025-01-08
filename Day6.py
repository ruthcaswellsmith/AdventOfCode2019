from __future__ import annotations
from utils import read_file
from typing import List, Dict
from collections import deque


class Node:
    def __init__(self, value: str):
        self.value = value
        self.children = []
        self.parent = None

    def add_child(self, child: Node):
        self.children.append(child)

    def add_parent(self, parent: Node):
        self.parent = parent


class OrbitMap:
    def __init__(self, data: List[str]):
        self.nodes: Dict[str, Node] = {}
        for line in data:
            orbited, orbiting = line.split(')')
            orbited_node = self.nodes.setdefault(orbited, Node(orbited))
            orbiting_node = self.nodes.setdefault(orbiting, Node(orbiting))
            orbited_node.add_child(orbiting_node)
            orbiting_node.add_parent(orbited_node)
        self.root = self.nodes['COM']

    def count_orbits(self):
        orbits = 0
        queue = deque([(self.root, 0)])

        while queue:
            node, depth = queue.popleft()
            orbits += (depth + 1) * len(node.children)
            queue.extend((child, depth + 1) for child in node.children)
        return orbits

    def get_ancestors(self, node: Node) -> List[Node]:
        ancestors = []
        while node != self.root:
            node = node.parent
            ancestors.append(node)
        return ancestors

    def get_orbital_transfers(self, val1: str, val2: str) -> int:
        ancestors1 = self.get_ancestors(self.nodes[val1])
        ancestors2 = self.get_ancestors(self.nodes[val2])
        indices = self.find_first_common_ancestor(ancestors1, ancestors2)
        return sum(indices)

    @staticmethod
    def find_first_common_ancestor(ancestors1: List[Node], ancestors2: List[Node]):
        return next(((ancestors1.index(x), ancestors2.index(x)) for x in ancestors1 if x in ancestors2), None)


def main():
    filename = 'input/Day6.txt'
    data = read_file(filename)

    orbit_map = OrbitMap(data)
    print(f"The answer to part 1 is {orbit_map.count_orbits()}")
    print(f"The answer to part 2 is {orbit_map.get_orbital_transfers('YOU', 'SAN')}")


if __name__ == '__main__':
    main()
