import numpy as np
from collections import Counter
from typing import List, Set, Dict


def get_char_counts(word: str) -> Set[int]:
    c = Counter(word)
    char_count = set(c.values())

    # We don't care about element that occur only
    # once, using try/except is an easy way to
    # remove them
    try:
        char_count.remove(1)
    except KeyError:
        pass

    return char_count


def get_checksum(list_of_ids: List[str]) -> int:
    total_counts = dict() # type: Dict[int, int]
    for entry in list_of_ids:
        char_counts = get_char_counts(entry)
        # If an element occurs more than once, we save the
        # number of occurences
        for char_count in char_counts:
            if char_count in total_counts:
                total_counts[char_count] += 1
            else:
                total_counts[char_count] = 1

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
