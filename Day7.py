from __future__ import annotations

from typing import Tuple
from itertools import permutations

from utils import read_file
from intcode import Program, Status


class Amplifier:
    def __init__(self, line: str, phase: int):
        self.program = Program(line)
        self.add_input(phase)
        self.next = None

    @property
    def outputs(self):
        return self.program.outputs

    @property
    def status(self):
        return self.program.status

    def run(self):
        self.program.run()

    def add_input(self, val: int):
        self.program.input_handler.add_input(val)

    def get_output(self):
        return self.program.outputs.popleft()


class AmplifierPipeline:
    def __init__(self, line: str, phases: Tuple):
        self.amplifiers = [Amplifier(line, phase) for phase in phases]
        for i in range(len(self.amplifiers)-1):
            self.amplifiers[i].next = self.amplifiers[i+1]
        self.amplifiers[len(self.amplifiers)-1].next = self.amplifiers[0]
        self.amplifiers[0].add_input(0)

    @property
    def thruster_output(self):
        return self.amplifiers[0].program.input_handler.values.pop()

    def run(self):
        while not all([amp.status == Status.TERMINATED for amp in self.amplifiers]):
            for amp in self.amplifiers:
                amp.run()
                while amp.outputs:
                    amp.next.add_input(amp.get_output())
        return self.thruster_output


def main():
    filename = 'input/Day7.txt'
    data = read_file(filename)

    phases = [ele for ele in range(5)]
    results = [AmplifierPipeline(data[0], p).run() for p in permutations(phases, 5)]
    print(f"The answer to part 1 is {max(results)}")

    phases = [ele for ele in range(5, 10)]
    results = [AmplifierPipeline(data[0], p).run() for p in permutations(phases, 5)]
    print(f"The answer to Part 2 is {max(results)}")


if __name__ == '__main__':
    main()
