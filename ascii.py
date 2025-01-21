from __future__ import annotations

from intcode import Program


class ASCII:
    def __init__(self, line: str):
        self.program = Program(line)

    def execute_command(self, command: str):
        for ch in command:
            self.program.add_input_value(ord(ch))
        self.program.add_input_value(10)
        self.program.run()

    def display_output(self):
        msg = ''
        while self.program.outputs:
            try:
                output = self.program.get_output_value()
                msg += chr(output)
            except ValueError:
                return output
        print(msg)
