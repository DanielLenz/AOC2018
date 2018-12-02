import numpy as np
from collections import Counter
from typing import List


def get_checksum(list_of_ids: List[str]):
    total_counts = dict()
    for entry in list_of_ids:
        c = Counter(entry)
        n_repeats = set(c.values())

        # We don't care about element that occur only
        # once, using try/except is an easy way to
        # remove them
        try:
            n_repeats.remove(1)
        except KeyError:
            pass

        # If an element occurs more than once, we save the
        # number of occurences
        for n_repeat in n_repeats:
            if n_repeat in total_counts:
                total_counts[n_repeat] += 1
            else:
                total_counts[n_repeat] = 1

    # The checksum is the product of all occurences > 1
    checksum = np.multiply.reduce(list(total_counts.values()))

    return checksum

def find_similar_ids(list_of_ids: List[str]):
    length = len(list_of_ids[0])

    for i in range(length - 1):
        d_cut = [dd[0:i] + dd[i+1:] for dd in list_of_ids]
        c = Counter(d_cut)
        candidate = c.most_common(1)[0]
        if candidate[1] == 2:
            return candidate[0]
    raise ValueError()


def solve1(d):
    checksum = get_checksum(d)
    print(checksum)


def solve2(d):
    similar_id = find_similar_ids(d)
    print(similar_id)

def main():
    d = np.loadtxt('input.txt', dtype=str)
    solve1(d)
    solve2(d)

if __name__ == '__main__':
    main()
