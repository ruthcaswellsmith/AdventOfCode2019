from __future__ import annotations

from typing import List
import array

from utils import read_file


class SpaceDeck:
    def __init__(self, num_cards: int, shuffles: List[str]):
        self.cards = array.array('i', [i for i in range(num_cards)])
        self.shuffles = shuffles

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


def main():
    filename = 'input/Day22.txt'
    data = read_file(filename)

    space_deck = SpaceDeck(10007, data)
    space_deck.process_shuffles()
    print(f"The 2019th card is {space_deck.cards.index(2019)}.")


if __name__ == '__main__':
    main()
