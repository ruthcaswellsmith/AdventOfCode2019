from utils import read_file
from typing import List
import operator


class Program:
    def __init__(self, line: str):
        self.initial_values = [int(ele) for ele in line.split(',')]
        self.values: List[int] = []
        self.ptr: int = 0
        self.reset()

    def reset(self):
        self.values = self.initial_values.copy()
        self.ptr = 0

    @staticmethod
    def get_operator(val: int):
        return operator.add if val == 1 else operator.mul if val == 2 else None

    def run(self, noun: int, verb: int):
        self.values[1], self.values[2] = noun, verb
        op = self.get_operator(self.values[self.ptr])
        while op:
            pos1, pos2, pos3 = self.values[self.ptr+1: self.ptr+4]
            self.values[pos3] = op(self.values[pos1], self.values[pos2])
            self.ptr += 4
            op = self.get_operator(self.values[self.ptr])
        return self.values[0]

    def find_input_for_target(self, target: int):
        for noun in range(100):
            self.reset()
            output = self.run(noun, 0)
            verb = target - output
            if verb < 100:
                return noun, verb


def main():
    filename = 'input/Day2.txt'
    data = read_file(filename)

    program = Program(data[0])
    print(f"The answer to part 1 is {program.run(12, 2)}")

    noun, verb = program.find_input_for_target(19690720)
    print(f"The answer to part 2 is {100 * noun + verb}")


if __name__ == '__main__':
    main()
