from __future__ import annotations

from typing import List

from ascii import ASCII
from utils import read_file


class SpringDroid:
    def __init__(self, line: str):
        self.ascii = ASCII(line)

    def execute_program(self, commands: List[str]):
        self.ascii.program.run()
        self.ascii.display_output()
        for cmd in commands:
            self.ascii.execute_command(cmd)
        return self.ascii.display_output()


def main():
    filename = 'input/Day21.txt'
    data = read_file(filename)

    springdroid = SpringDroid(data[0])
    commands = [
        "NOT B J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT A T",
        "OR T J",
        "WALK"
    ]
    print(f"The answer to Part 1 is {springdroid.execute_program(commands)}")

    springdroid = SpringDroid(data[0])
    commands = [
        "NOT B J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "AND H J",
        "NOT A T",
        "OR T J",
        "RUN"
    ]
    print(f"The answer to Part 2 is {springdroid.execute_program(commands)}")


if __name__ == '__main__':
    main()
