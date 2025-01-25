from __future__ import annotations

from typing import List
import array

from utils import read_file, Part


class SpaceDeck:
    def __init__(self, num_cards: int, shuffles: List[str], part: Part):
        self.num_cards = num_cards
        if part == Part.PT1:
            self.cards = array.array('i', [i for i in range(num_cards)])
        self.shuffles = shuffles
        self.A, self.B = None, None

    def process_shuffles(self):
        for shuffle in self.shuffles:
            self.cards = self.shuffle(shuffle)

    def shuffle(self, shuffle: str):
        if "deal into new stack" in shuffle:
            return self.deal_into_new_stack()
        elif "cut" in shuffle:
            return self.cut(int(shuffle.split(' ')[-1]))
        elif "deal with increment" in shuffle:
            return self.deal_with_increment(int(shuffle.split(' ')[-1]))
        else:
            raise ValueError('Unexpected shuffle!')

    def deal_into_new_stack(self):
        self.cards.reverse()
        return self.cards

    def cut(self, n: int):
        if n >= 0:
            return self.cards[n:] + self.cards[:n]
        else:
            return self.cards[n:] + self.cards[:len(self.cards) + n]

    def deal_with_increment(self, n: int):
        t, ptr = array.array('i', (len(self.cards) * [0])), 0
        for i in range(len(self.cards)):
            t[ptr] = self.cards[i]
            ptr = (ptr + n) % len(self.cards)
        return t

    def get_coefficients(self, iterations: int):
        a, b = self.compose_polynomials()
        self.A, self.B = self.modpow_polynomial(a, b, iterations)

    def modpow_polynomial(self, a: int, b: int, m: int):
        # We have to raise f(x) = ax + b to the number of iterations
        # We use binary exponentiation which makes it O(log n) instead of O(n)
        if m == 0:
            return 1, 0
        if m % 2 == 0:
            return self.modpow_polynomial(a * a % self.num_cards, (a * b + b) % self.num_cards, m // 2)
        else:
            c, d = self.modpow_polynomial(a, b, m - 1)
            return a * c % self.num_cards, (a * d + b) % self.num_cards

    def compose_polynomials(self):
        # This is our starting point f(x) = x
        a, b = 1, 0
        for shuffle in reversed(self.shuffles):
            # Now we compose g(f(x)) for each shuffle so that
            # we keep modifying a and b
            if "deal into new stack" in shuffle:
                # g(x) = self.num_cards - 1 - x
                a = -a
                b = self.num_cards - b - 1
            elif "cut" in shuffle:
                # g(x) = (x + n) % self.num_cards
                n = int(shuffle.split(' ')[-1])
                b = (b + n) % self.num_cards
            elif "deal with increment" in shuffle:
                # g(x) = modinv(n, self.num_cards) * x % self.num_cards
                n = int(shuffle.split(' ')[-1])
                # We can do this because of Fermat's Little Theorem which
                # states that modinv(N, D) == pow(n, D-2, D) if D is prime
                z = pow(n, self.num_cards - 2, self.num_cards)
                a = a * z % self.num_cards
                b = b * z % self.num_cards
            else:
                raise ValueError('Unexpected shuffle!')
        return a, b

    def card_at_pos(self, pos: int):
        return (self.A * pos + self.B) % self.num_cards


def main():
    filename = 'input/Day22.txt'
    data = read_file(filename)

    space_deck = SpaceDeck(10007, data, Part.PT1)
    space_deck.process_shuffles()
    print(f"The 2019th card is {space_deck.cards.index(2019)}.")

    space_deck = SpaceDeck(119315717514047, data, Part.PT2)
    space_deck.get_coefficients(iterations=101741582076661)
    print(f"The card at position 2020 is {space_deck.card_at_pos(2020)}.")


if __name__ == '__main__':
    main()
