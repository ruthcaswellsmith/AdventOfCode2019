from __future__ import annotations

from utils import read_file
from intcode import Program


def main():
    filename = 'input/Day9.txt'
    data = read_file(filename)

    program = Program(data[0])
    program.add_input_value(1)
    program.run()
    print(f"The answer to part 1 is {program.outputs.popleft()}")

    program = Program(data[0])
    program.add_input_value(2)
    program.run()
    print(f"The answer to part 2 is {program.outputs.popleft()}")


if __name__ == '__main__':
    main()
