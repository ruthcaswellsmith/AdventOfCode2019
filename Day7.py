from __future__ import annotations

from typing import Tuple
from functools import reduce
from itertools import permutations

from utils import read_file
from Day5 import Program


class Amplifier:
    def __init__(self, line: str, phase: int):
        self.program = Program(line)
        self.phase = phase

    def run(self, input_signal: int):
        self.program.run([self.phase, input_signal])
        return self


class AmplifierPipeline:
    def __init__(self, line: str, phases: Tuple[int]):
        self.amplifiers = [Amplifier(line, phase) for phase in phases]

    def run(self):
        return reduce(
            lambda input_val, amplifier: amplifier.run(input_val).program.outputs[-1],
            self.amplifiers,
            0
        )


def main():
    filename = 'input/Day7.txt'
    data = read_file(filename)

    phases = [ele for ele in range(5)]
    results = [AmplifierPipeline(data[0], permutation).run() for permutation in permutations(phases, 5)]
    print(f"The answer to part 1 is {max(results)}")


if __name__ == '__main__':
    main()
