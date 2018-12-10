#! /usr/bin/env python

from typing import List
import unittest
import sys



def reacts(ch1: str, ch2: str) -> bool:
    if (ch1.lower() == ch2.lower()) and (ch1.isupper() ^ ch2.isupper()):
        return True
    else:
        return False


def parse_input(input_str: str) -> List[str]:
    list_of_chars = [ch for ch in input_str]

    return list_of_chars


def reduce_polymer(input_str: str) -> str:
    original_chars = parse_input(input_str)
    reduced_list = reduce_list(original_chars)
    reduced_chars = "".join(reduced_list)

    return reduced_chars


def reduce_list(list_in: List[str]) -> List[str]:
    lo, hi = 0, 1
    while True:
        if reacts(list_in[lo], list_in[hi]):
            # Popping low twice removes low and high
            list_in.pop(lo)
            list_in.pop(lo)

            # We move back by one, making sure that we catch new reactions
            lo = max(0, lo-1)
            hi = lo+1
        else:
            lo += 1
            hi += 1
        if hi >= len(list_in):
            break

    return list_in


def remove_unittype(input_str: str, unittype) -> str:
    trans = str.maketrans(
        '', '',
        f"{unittype.lower(), unittype.upper()}")

    return input_str.translate(trans)


def length_of_optimized_polymer(input_str: str) -> str:
    unittypes = set(input_str.lower())

    min_length = sys.maxsize

    for unittype in unittypes:
        # First remove all chars of one type
        optimized_polymer = remove_unittype(input_str, unittype)
        # Second, reduce the optimized string
        reduced_optimized_polymer = reduce_polymer(optimized_polymer)
        if len(reduced_optimized_polymer) < min_length:
            min_length = len(reduced_optimized_polymer)

    return min_length


class TestDay05(unittest.TestCase):
    def setUp(self):
        self.input = "dabAcCaCBAcCcaDA"
    
    def test_construction(self):
        expected = [
           "d", "a", "b", "A", "c", "C", "a", "C",
           "B", "A", "c", "C", "c", "a", "D", "A"]
        
        actual = parse_input(self.input)

        self.assertSequenceEqual(expected, actual, seq_type=List)

    def test_reduce_polymer(self):
        expected = "dabCBAcaDA"
        self.assertEqual(expected, reduce_polymer(self.input))

    def test_reacts(self):
        is_true = [('a', 'A'), ('B', 'b')]
        is_false = [('a', 'a'), ('\t', '\t'), ('B', 'B'), ('D', 'c')]

        for inp in is_true:
            self.assertTrue(reacts(*inp))

        for inp in is_false:
            self.assertFalse(reacts(*inp))

    def test_reduce(self):
        expected = "dabCBAcaDA"

        self.assertEqual(
            expected, reduce_polymer(self.input)
        )


    def test_remove_unittype(self):
        expected = "dbcCCBcCcD"

        self.assertEqual(
            expected,
            remove_unittype(self.input, 'a')
        )

    def test_reduce_optimized(self):
        expected = 4

        self.assertEqual(
            expected,
            length_of_optimized_polymer(self.input)
        )

def main():
    with open('input.txt') as f:
        input_str = [line.strip() for line in f][0]

    reduced_polymer = reduce_polymer(input_str)
    print(len(reduced_polymer))

    length = length_of_optimized_polymer(input_str)
    print(length)

if __name__ == "__main__":
    # unittest.main()
    main()

