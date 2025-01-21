from __future__ import annotations

from intcode import Program


class ASCII:
    def __init__(self, line: str):
        self.program = Program(line)

    def execute_command(self, command: str):
        self.program.reset()
        for ch in command:
            self.program.add_input_value(ord(ch))
        self.program.add_input_value(10)
        self.program.run()

    def display_output(self):
        msg = ""
        try:
            while self.program.outputs:
                output = chr(self.program.get_output_value())
                msg += output
        except ValueError:
            print(f"Non-ASCII output is {output}")
        print(f"{msg}")
