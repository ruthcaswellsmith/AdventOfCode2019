from __future__ import annotations

from typing import List
from collections import defaultdict
import math

from utils import read_file


class Reaction:
    def __init__(self, amount: int, components: List[str]):
        self.amount = amount
        self.level = None
        self.components = defaultdict(int)
        for i in range(0, len(components), 2):
            self.components[components[i+1].rstrip(',')] = int(components[i])


class Reactions:
    def __init__(self, data: List[str]):
        self.reactions = {}
        for line in data:
            pts = line.split()
            self.reactions[pts[-1]] = Reaction(int(pts[-2]), pts[:pts.index("=>")])
        self.ore_required = defaultdict(int)
        for component in self.reactions.keys():
            self.reactions[component].level = self.calculate_level(component, 0)
        self.reactions['ORE'] = Reaction(1, ['1', 'ORE'])
        self.reactions['ORE'].level = 0

    def calculate_level(self, component: str, level: int):
        if component == 'ORE':
            return level
        return max([self.calculate_level(comp, level + 1) for comp in self.reactions[component].components.keys()])

    def calculate_required_ore(self, amount_of_fuel: int) -> int:
        needed = defaultdict(int)
        needed['FUEL'] = amount_of_fuel
        max_level = max([self.reactions[comp].level for comp in needed])
        components = list(needed.keys()).copy()
        while not max_level == 0:
            for comp in components:
                if self.reactions[comp].level == max_level:
                    amount = needed[comp]
                    reaction = self.reactions[comp]
                    reactions_required = math.ceil(amount / reaction.amount)
                    for component in reaction.components:
                        needed[component] += reactions_required * reaction.components[component]
                    del needed[comp]
            max_level = max([self.reactions[comp].level for comp in needed])
            components = list(needed.keys()).copy()
        return needed['ORE']

    def find_amount_of_fuel(self, available_ore: int) -> int:
        ore_for_one_fuel = self.calculate_required_ore(1)
        low = available_ore // ore_for_one_fuel
        high = 2 * low
        while low <= high:
            mid = (low + high) // 2
            unused_ore = available_ore - self.calculate_required_ore(mid)
            if unused_ore < 0:
                high = mid - 1
            else:
                low = mid + 1
        return low - 1


def main():
    filename = 'input/Day14.txt'
    data = read_file(filename)

    reactions = Reactions(data)
    print(f"The total ore required is {reactions.calculate_required_ore(1)}")

    print(f"The amount of fuel produced is {reactions.find_amount_of_fuel(1_000_000_000_000)}")


if __name__ == '__main__':
    main()
