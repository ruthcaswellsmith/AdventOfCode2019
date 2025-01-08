from __future__ import annotations

from collections import Counter
import numpy as np

from utils import read_file


class Image:
    WIDTH = 25
    HEIGHT = 6

    def __init__(self, line: str):
        self.encoded_image = line
        self.layer_size = self.WIDTH * self.HEIGHT
        self.num_layers = len(self.encoded_image) // self.layer_size
        self.counts = {}
        self.decoded_image = np.zeros((self.HEIGHT, self.WIDTH), dtype=int)

    def get_layer_with_least_zeros(self):
        layer = 0
        while layer < self.num_layers:
            ptr = layer * self.layer_size
            self.counts[layer] = Counter(self.encoded_image[ptr: ptr + self.layer_size])
            layer += 1
        return min(self.counts, key=lambda k: self.counts[k]['0'])

    def answer_pt1(self, layer_num: int):
        return self.counts[layer_num]['1'] * self.counts[layer_num]['2']

    def decode_image(self):
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                pixel_values = [self.encoded_image[layer * self.layer_size + row * self.WIDTH + col] for \
                                layer in range(self.num_layers)]
                self.decoded_image[row, col] = next(pixel for pixel in pixel_values if pixel != '2')


def main():
    filename = 'input/Day8.txt'
    data = read_file(filename)

    image = Image(data[0])
    layer = image.get_layer_with_least_zeros()
    print(f"The answer to Part 1 is {image.answer_pt1(layer)}")

    image.decode_image()
    print(image.decoded_image)


if __name__ == '__main__':
    main()
