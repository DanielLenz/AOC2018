import numpy as np
from itertools import cycle

def part1(d):
    print('Part 1:', d.sum())

def part2(d):
    current_sum = 0
    seen = set()

    for val in cycle(d):
        if current_sum in seen:
            break
        else:
            seen.add(current_sum)
            current_sum += val 


    print(current_sum)

    return 0


def main():
    d = np.loadtxt('input.txt')

    part1(d)
    part2(d)

if __name__ == '__main__':
    main()
