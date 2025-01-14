from __future__ import annotations

from typing import Dict, List
import numpy as np

from utils import read_file, Part


class FFT:
    def __init__(self, line: str, part: Part):
        self.part = part
        if part == part.PT1:
            self.input = np.array([int(ele) for ele in line])
            self.length = self.input.shape[0]
            self.patterns = self.get_patterns()
        else:
            self.input = np.array([int(ele) for ele in line[int(line[:7]):]])
            self.length = self.input.shape[0]

    def get_patterns(self) -> Dict[int, List]:
        patterns = {i: np.zeros(self.length, dtype=int) for i in range(self.length)}
        base_pattern = [1, 0, -1, 0]
        for i in range(self.length):
            arr = patterns[i]
            pos, bp_ind = i, 0
            done = False
            while not done:
                for j in range(i + 1):
                    if bp_ind in [0, 2]:
                        arr[pos] = base_pattern[bp_ind]
                    pos += 1
                    if pos == self.length:
                        done = True
                        break
                if done:
                    break
                bp_ind = (bp_ind + 1) % 4
        return patterns

    def process(self, num_iterations: int):
        if self.part == Part.PT1:
            return self.process_pt1(num_iterations)
        else:
            return self.process_pt2(num_iterations)

    def process_pt1(self, num_iterations: int) -> str:
        for iteration in range(num_iterations):
            output = np.zeros(self.length, dtype=int)
            for i in range(self.length):
                output[i] = abs(np.sum(self.input * self.patterns[i])) % 10
            self.input = output
        return ''.join(map(str, self.input))[:8]

    def process_pt2(self, num_iterations: int) -> str:
        for iteration in range(num_iterations):
            output = np.zeros(self.length, dtype=int)
            for i in range(self.length):
                if i == 0:
                    total = np.sum(self.input)
                else:
                    total -= self.input[i - 1]
                output[i] = total % 10
            self.input = output
        return ''.join(map(str, self.input))[:8]


def main():
    filename = 'input/Day16.txt'
    data = read_file(filename)

    fft = FFT(data[0], Part.PT1)
    print(f"The answer to Part 1 is {fft.process(100)}")

    fft = FFT(10_000*data[0], Part.PT2)

    print(f"The answer to Part 2 is {fft.process(100)}")


if __name__ == '__main__':
    main()
