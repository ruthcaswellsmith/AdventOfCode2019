from utils import read_file


def calculate_fuel(mass: int):
    return mass // 3 - 2


def fuel_sequence(mass):
    while mass > 0:
        mass = max(0, calculate_fuel(mass))
        yield mass


if __name__ == '__main__':
    filename = 'input/Day1.txt'
    data = read_file(filename)

    masses = [int(line) for line in data]
    print(f"The answer to part 1 is {sum([calculate_fuel(m) for m in masses])}")
    print(f"The answer to part 2 is {sum(sum(fuel_sequence(mass)) for mass in masses)}")
