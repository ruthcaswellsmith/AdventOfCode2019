from __future__ import annotations

from typing import List, Tuple

from intcode import Program
from utils import read_file


class Network:
    def __init__(self, line: str):
        self.computers = [Program(line) for _ in range(50)]
        for i, computer in enumerate(self.computers):
            computer.add_input_value(i)
            computer.run()
        self.first_nat_y, self.last_nat_x, self.last_nat_y = None, None, None
        self.nat_delivered_y = set()

    def process(self):
        while True:
            packets = self.read_packets()
            idle = False if packets else True
            if idle and self.last_nat_x and self.last_nat_y:
                if self.last_nat_y in self.nat_delivered_y:
                    return self.first_nat_y, self.last_nat_y
                self.nat_deliver()
            self.process_packets(packets)
            self.run_computers()

    def run_computers(self):
        for id in range(50):
            if len(self.computers[id].input_handler.values) == 0:
                self.computers[id].add_input_value(-1)
            self.computers[id].run()

    def process_packets(self, packets: List[Tuple]):
        for addr, x, y in packets:
            if addr == 255:
                self.process_nat_packet(x, y)
            elif not 0 <= addr < 50:
                raise ValueError("Invalid Address!")
            else:
                self.process_regular_packet(addr, x, y)

    def process_regular_packet(self, addr: int, x: int, y: int):
        for val in [x, y]:
            self.computers[addr].add_input_value(val)

    def process_nat_packet(self, x: int, y: int):
        if not self.first_nat_y:
            self.first_nat_y = y
        self.last_nat_x, self.last_nat_y = x, y

    def nat_deliver(self):
        self.computers[0].add_input_value(self.last_nat_x)
        self.computers[0].add_input_value(self.last_nat_y)
        self.nat_delivered_y.add(self.last_nat_y)

    def read_packets(self):
        packets = []
        for id in range(50):
            while len(self.computers[id].outputs) >= 3:
                addr = self.computers[id].get_output_value()
                x = self.computers[id].get_output_value()
                y = self.computers[id].get_output_value()
                packets.append((addr, x, y))
        return packets


def main():
    filename = 'input/Day23.txt'
    data = read_file(filename)

    network = Network(data[0])
    first_nat_y, first_duplicate_nat_y = network.process()
    print(f"The answer to Part 1 is {first_nat_y}")
    print(f"The answer to Part 2 is {first_duplicate_nat_y}")


if __name__ == '__main__':
    main()
