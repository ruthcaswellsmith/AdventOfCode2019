from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple
import math

from utils import read_file


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class AsteroidMap:
    def __init__(self, data: List[str]):
        self.asteroids = {(i, j): defaultdict(list)
                          for j, line in enumerate(data)
                          for i, ele in enumerate(line) if ele == '#'}
        self.get_angles()
        self.sort_asteroids_by_distance()
        self.vaporized = []

    @property
    def answer_pt2(self):
        a = self.vaporized[199]
        return 100 * a[0] + a[1]

    @property
    def monitoring_station(self) -> Tuple[int, int]:
        return max(self.asteroids, key=lambda k: len(self.asteroids[k]))

    def visible_asteroids(self, asteroid: Tuple[int, int]) -> int:
        return len(self.asteroids[asteroid])

    def get_angles(self):
        for a1 in self.asteroids:
            for a2 in self.asteroids:
                if a1 != a2:
                    theta = self.get_angle(a1, a2)
                    self.asteroids[a1][theta].append(a2)

    @staticmethod
    def get_angle(a1: Tuple[int, int], a2: Tuple[int, int]):
        """This calculates the angle off vertical of the vector from a1 to a2"""
        if a1[0] == a2[0]:
            return 0 if a1[1] > a2[1] else math.pi
        if a1[1] == a2[1]:
            return math.pi / 2 if a1[0] < a2[0] else 3 * math.pi / 2
        angle = math.atan2(a2[0] - a1[0], a1[1] - a2[1])
        return angle + 2 * math.pi if angle < 0 else angle

    def sort_asteroids_by_distance(self):
        for origin, angles in self.asteroids.items():
            for angle, asteroids in angles.items():
                asteroids.sort(key=lambda a: manhattan_distance(origin, a), reverse=True)

    def vaporize(self):
        angles = self.asteroids[self.monitoring_station]
        sorted_angles = sorted(angles.keys())
        while any(angles.values()):
            for angle in sorted_angles:
                if angles[angle]:
                    self.vaporized.append(angles[angle].pop())


def main():
    filename = 'input/Day10.txt'
    data = read_file(filename)

    asteroid_map = AsteroidMap(data)
    monitoring_station = asteroid_map.monitoring_station
    print(f"The best monitoring station is {monitoring_station} with"
          f" {asteroid_map.visible_asteroids(monitoring_station)} visible asteroids.")

    asteroid_map.vaporize()
    print(f"The answer to Part 2 is {asteroid_map.answer_pt2}")


if __name__ == '__main__':
    main()
