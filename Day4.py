from __future__ import annotations
from typing import List

from utils import read_file, Part


class Password:
    def __init__(self, line: str):
        self.low, self.high = [int(ele) for ele in line.split('-')]
        self.count = 0

    def reset(self):
        self.count = 0

    def count_possibilities(self, part: Part):
        current = self.low
        while current <= self.high:
            digits = [ele for ele in str(current)]
            if sorted(digits) == digits:
                if part == Part.PT1 and self.has_double_digit(current, digits) or \
                        part == Part.PT2 and self.has_double_only_digit(current, digits):
                    self.count += 1
                current += 1
            else:
                digits = self.get_next_sorted_number(digits)
                current = int(''.join(digits))

    @staticmethod
    def get_next_sorted_number(digits: List[str]):
        for i in range(len(digits) - 1):
            if digits[i] > digits[i+1]:
                for j in range(i+1, len(digits)):
                    digits[j] = digits[i]
                return digits

    @staticmethod
    def has_double_digit(current: int, digits: List[str]) -> bool:
        return any(k * 2 in str(current) for k in set(digits))

    @staticmethod
    def has_double_only_digit(current: int, digits: List[str]) -> bool:
        return any(k * 2 in str(current) and k * 3 not in str(current) for k in set(digits))


def main():
    filename = 'input/Day4.txt'
    data = read_file(filename)

    password = Password(data[0])
    password.count_possibilities(Part.PT1)
    print(f"The answer to part 1 is {password.count}")

    password.reset()
    password.count_possibilities(Part.PT2)
    print(f"The answer to part 2 is {password.count}")


if __name__ == '__main__':
    main()
