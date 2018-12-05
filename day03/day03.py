import numpy as np
from typing import Tuple, NamedTuple
import re


class Rectangle(NamedTuple):
    id: int
    x_lo: int
    y_lo: int
    width: int
    height: int

    @staticmethod
    def rgx() -> str:
        return "#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"

    @staticmethod
    def from_claim(claim: str) -> 'Rectrangle':
        id, x_lo, y_lo, width, height = [int(x) for x in re.match(Rectangle.rgx(), claim).groups()]
        return Rectangle(id, x_lo, y_lo, width, height)

def build_fabric(
        id: int,
        x: int,
        y: int,
        dx: int,
        dy: int,
        size: Tuple[int, int] = (1000, 1000)) -> np.ndarray:

    fabric = np.zeros(size, dtype=int)
    last_id = np.zeros(size, dtype=int)

    for idd, xx, yy, dxx, dyy in zip(id, x, y, dx, dy):
        fabric[xx:xx+dxx, yy:yy+dyy] += 1
        last_id[xx:xx+dxx, yy:yy+dyy] = idd

    return fabric, last_id

def size_of_overlap(fabric: np.ndarray) -> int:
    overlap = (fabric > 1).sum()
    return overlap

def solve1a(data):
    # Test fabric
    test_id = [0, 1, 2]
    test_xx = [1, 3, 5]
    test_yy = [3, 1, 5]
    test_dxx = [4, 4, 2]
    test_dyy = [4, 4, 2]

    test_fabric, _ = build_fabric(
        test_id, test_xx, test_yy, test_dxx, test_dyy, size=(10, 10))
    assert size_of_overlap(test_fabric) == 4

    # Build fabric
    fabric, _ = build_fabric(
        data['id'], data['x'], data['y'], data['width'], data['height'])
    return fabric, size_of_overlap(fabric)

def solve2a(data):
    fabric, _ = build_fabric(
        data['id'], data['x'], data['y'], data['width'], data['height'])

    for idd, xx, yy, ww, hh in zip(
            data['id'], data['x'], data['y'], data['width'], data['height']):
        if (fabric[xx:xx+ww, yy:yy+hh] == 1).all():
            return idd

    return None


def main():
    rgx = "#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
    data = np.fromregex(
            'day03/input.txt',
            rgx,
            [('id', np.int), ('x', np.int), ('y', np.int), ('width', np.int), ('height', np.int)]
    )

    print(solve1a(data)[1])
    print(solve2a(data))


if __name__ == '__main__':
    main()