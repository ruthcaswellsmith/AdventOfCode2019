from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations
from math import lcm
from typing import List

from utils import read_file


@dataclass
class XYZ:
    x: int
    y: int
    z: int

    def increment(self, deltas: XYZ):
        self.x += deltas.x
        self.y += deltas.y
        self.z += deltas.z

    def negate(self) -> XYZ:
        return XYZ(-self.x, -self.y, -self.z)


class Moon:
    def __init__(self, pos: XYZ):
        self.pos = pos
        self.vel = XYZ(0, 0, 0)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return sum([abs(getattr(self.pos, attr)) for attr in ['x', 'y', 'z']])

    def kinetic_energy(self):
        return sum([abs(getattr(self.vel, attr)) for attr in ['x', 'y', 'z']])

    def dimension_is_equal(self, other: Moon, attr: str) -> bool:
        return getattr(self.pos, attr) == getattr(other.pos, attr) and \
               getattr(self.vel, attr) == getattr(other.vel, attr)

    def compare_positions(self, other: Moon):
        return XYZ((self.pos.x < other.pos.x) - (self.pos.x > other.pos.x),
                   (self.pos.y < other.pos.y) - (self.pos.y > other.pos.y),
                   (self.pos.z < other.pos.z) - (self.pos.z > other.pos.z))


class JupitersMoons:
    def __init__(self, moons: List[Moon]):
        self.moons = moons
        self.pairs = list(combinations(self.moons, 2))

    def step(self, num_steps: int):
        for _ in range(num_steps):
            self.apply_gravity()
            self.apply_velocity()

    def apply_gravity(self):
        for pair in self.pairs:
            deltas = pair[0].compare_positions(pair[1])
            pair[0].vel.increment(deltas)
            pair[1].vel.increment(deltas.negate())

    def apply_velocity(self):
        for moon in self.moons:
            moon.pos.increment(moon.vel)


class CycleFinder:
    def __init__(self, moons: List[Moon]):
        self.num_moons = len(moons)
        self.tortoise = JupitersMoons(deepcopy(moons))
        self.hare = JupitersMoons(deepcopy(moons))
        self.total_steps = 0
        self.periods = {}

    @property
    def cycle_length(self):
        return lcm(*self.periods.values())

    def find_cycle(self):
        while len(self.periods) < 3:
            self.tortoise.step(1)
            self.hare.step(2)
            self.total_steps += 1
            for attr in ['x', 'y', 'z']:
                if attr not in self.periods and self.check_for_period(attr):
                    self.periods[attr] = self.total_steps

    def check_for_period(self, attr: str) -> bool:
        return True if \
            all([self.tortoise.moons[i].dimension_is_equal(self.hare.moons[i], attr) for i in range(self.num_moons)]) \
            else False


def main():
    filename = 'input/Day12.txt'
    data = read_file(filename)

    moons = [Moon(
        XYZ(*[int(ele) for ele in line.strip('<>').replace('x=', '').replace('y=', '').replace('z=', '').split(',')]))
             for line in data]
    jupiter_moons = JupitersMoons(moons)
    jupiter_moons.step(1000)
    print(f"The total energy of the system is {sum([moon.total_energy() for moon in jupiter_moons.moons])}")

    cycle_finder = CycleFinder(moons)
    cycle_finder.find_cycle()
    print(f"The length of the cycle is {cycle_finder.cycle_length}")


if __name__ == '__main__':
    main()
