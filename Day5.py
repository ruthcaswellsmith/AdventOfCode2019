from __future__ import annotations
from collections import deque

from utils import read_file
from typing import List
from enum import Enum, auto


class ParameterMode(int, Enum):
    POSITION = 0
    IMMEDIATE = 1

    @classmethod
    def get_mode(cls, mode: int) -> ParameterMode:
        try:
            return next(m for m in cls if m.value == mode)
        except StopIteration:
            raise ValueError(f"Invalid mode: {mode}")


class OpcodeType(int, Enum):
    # Format: (opcode_value, num_params)
    ADD = (1, 3)
    MULTIPLY = (2, 3)
    INPUT = (3, 1)
    OUTPUT = (4, 1)
    JUMP_IF_TRUE = (5, 2)
    JUMP_IF_FALSE = (6, 2)
    LESS_THAN = (7, 3)
    EQUALS = (8, 3)
    TERMINATE = (99, 0)

    def __new__(cls, value, num_params):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.num_params = num_params
        return obj

    @property
    def parameter_count(self):
        return self.num_params

    @classmethod
    def get_opcode_type(cls, opcode_type: int) -> OpcodeType:
        try:
            return next(o for o in cls if o.value == opcode_type)
        except StopIteration:
            raise ValueError(f"Invalid Opcode Type: {opcode_type}")


class Operator:
    def __init__(self, opcode_type: OpcodeType, param_modes: List[ParameterMode]):
        self.opcode_type = opcode_type
        self.param_modes = param_modes

    @staticmethod
    def get_parameter_modes(param_modes: str) -> List[ParameterMode]:
        return [ParameterMode.get_mode(int(mode)) for mode in param_modes]

    @classmethod
    def get_operator(cls, opcode: int) -> Operator:
        opcode_str = str(opcode).zfill(5)
        opcode_type = OpcodeType.get_opcode_type(int(opcode_str[-2:]))
        return cls(
            opcode_type,
            cls.get_parameter_modes(reversed(opcode_str[:3]))[:opcode_type.num_params]
        )


class InputHandler:
    def __init__(self):
        self.values = deque()

    def add_input(self, val: int):
        self.values.append(val)

    def get_input(self) -> int:
        return self.values.popleft()


class Status(str, Enum):
    WAITING_FOR_INPUT = auto()
    TERMINATED = auto()
    PROCESSING = auto()


class Program:
    def __init__(self, line: str):
        self.initial_memory = [int(ele) for ele in line.split(',')]
        self.memory: List[int] = []
        self.ptr: int = 0
        self.status = Status.WAITING_FOR_INPUT
        self.reset()

        self.execution_methods = {
            OpcodeType.ADD: self._add,
            OpcodeType.MULTIPLY: self._multiply,
            OpcodeType.INPUT: self._input,
            OpcodeType.OUTPUT: self._output,
            OpcodeType.JUMP_IF_TRUE: self._jump_if_true,
            OpcodeType.JUMP_IF_FALSE: self._jump_if_false,
            OpcodeType.LESS_THAN: self._less_than,
            OpcodeType.EQUALS: self._equals
        }
        self.input_handler = InputHandler()
        self.outputs = deque()

    def reset(self):
        self.memory = self.initial_memory.copy()
        self.ptr = 0

    def add_input_value(self, val: int):
        self.input_handler.add_input(val)

    def run(self):
        op = Operator.get_operator(self.memory[self.ptr])
        self.update_status(op)
        while self.status not in [Status.WAITING_FOR_INPUT, Status.TERMINATED]:
            self.ptr += 1
            positions = [self._get_parameter_pos(op, i) for i in range(op.opcode_type.num_params)]
            self.execute_operation(op.opcode_type, positions)

            op = Operator.get_operator(self.memory[self.ptr])
            self.update_status(op)

    def update_status(self, op: Operator):
        if op.opcode_type == OpcodeType.INPUT and not self.input_handler.values:
            self.status = Status.WAITING_FOR_INPUT
        elif op.opcode_type == OpcodeType.TERMINATE:
            self.status = Status.TERMINATED
        else:
            self.status = Status.PROCESSING

    def execute_operation(self, opcode_type: OpcodeType, positions: List[int]):
        self.execution_methods[opcode_type](opcode_type, positions)

    def _get_parameter_pos(self, op: Operator, num_param: int) -> int:
        return self.ptr + num_param if op.param_modes[num_param] == ParameterMode.IMMEDIATE else \
            self.memory[self.ptr + num_param]

    def _add(self, opcode_type: OpcodeType, positions: List[int]):
        self.memory[positions[2]] = self.memory[positions[0]] + self.memory[positions[1]]
        self.ptr += opcode_type.num_params

    def _multiply(self, opcode_type: OpcodeType, positions: List[int]):
        self.memory[positions[2]] = self.memory[positions[0]] * self.memory[positions[1]]
        self.ptr += opcode_type.num_params

    def _input(self, opcode_type: OpcodeType, positions: List[int]):
        self.memory[positions[0]] = self.input_handler.get_input()
        self.ptr += opcode_type.num_params

    def _output(self, opcode_type: OpcodeType, positions: List[int]):
        self.outputs.append(self.memory[positions[0]])
        self.ptr += opcode_type.num_params

    def _jump_if_true(self, opcode_type: OpcodeType, positions: List[int]):
        self.ptr = self.memory[positions[1]] if \
            self.memory[positions[0]] != 0 else \
            self.ptr + opcode_type.num_params

    def _jump_if_false(self, opcode_type: OpcodeType, positions: List[int]):
        self.ptr = self.memory[positions[1]] if \
            self.memory[positions[0]] == 0 else \
            self.ptr + opcode_type.num_params

    def _less_than(self, opcode_type: OpcodeType, positions: List[int]):
        self.memory[positions[2]] = 1 if \
            self.memory[positions[0]] < self.memory[positions[1]] else \
            0
        self.ptr += opcode_type.num_params

    def _equals(self, opcode_type: OpcodeType, positions: List[int]):
        self.memory[positions[2]] = 1 if \
            self.memory[positions[0]] == self.memory[positions[1]] else \
            0
        self.ptr += opcode_type.num_params


def main():
    filename = 'input/Day5.txt'
    data = read_file(filename)

    program = Program(data[0])
    program.add_input_value(1)
    program.run()
    print(f"The answer to part 1 is {program.outputs.pop()}")

    program.reset()
    program.add_input_value(5)
    program.run()
    print(f"The answer to part 2 is {program.outputs.pop()}")


if __name__ == '__main__':
    main()
