RAW = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split("\n")

# Want to find guard with most minutes asleep total,
# then find the minute during which this guard is most often asleep

from typing import List, NamedTuple, Tuple, List
from collections import Counter
import unittest
import re

class Timestamp(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int

class Nap(NamedTuple):
    guard_id: int
    sleep: int  # Minute at which he falls asleep
    wake: int # Minute at which he wakes up

def parse_line(line: str) -> List:
    rgx = r"\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] (.*)"
    parsed_input = re.match(rgx, line).groups()

    return parsed_input

def parse_comment(line: str) -> int:
    """E.g. 'Guard #10 begins shift' will return 10
    """

    rgx = "Guard #([0-9]+) begins shift"
    out = re.match(rgx, line)
    
    return out

def find_naps(entries: List[str]) -> List[Nap]:
    naps: List[Nap] = []
    entries = sorted(entries)

    guard_id = sleep = wake = None

    for entry in entries:
        year, month, day, hours, minute, comment = parse_line(entry)
        ts = Timestamp(*map(int, [year, month, day, hours, minute]))
        guard_status = parse_comment(comment)
    
        if guard_status:
            assert sleep is None and wake is None
            guard_id = int(guard_status.groups()[0])
        
        elif "falls asleep" in comment:
            assert guard_id is not None and sleep is None and wake is None
            sleep = int(minute)

        elif "wakes up" in comment:
            assert guard_id is not None and sleep is not None and wake is None
            wake = int(minute)

            naps.append(Nap(guard_id, sleep, wake))
            wake = sleep = None

    return naps

def sleepiest_guard(naps: List[Nap]) -> int:
    sleep_counts = Counter()
    for nap in naps:
        sleep_counts[nap.guard_id] += (nap.wake - nap.sleep)

    return sleep_counts.most_common(1)[0][0]

def sleepiest_minute(naps: List[Nap], guard_id: int) -> int:
    minutes = Counter()

    for nap in naps:
        if nap.guard_id == guard_id:
            for minute in range(nap.sleep, nap.wake):
                minutes[minute] += 1

    [(minute1, count1), (minute2, count2)] = minutes.most_common(2)
    assert count1 > count2
    return minute1

    # assert sleepiest_guard

def most_regular_sleeper(naps: List[Nap]) -> Tuple[int, int]:
    counts = Counter()

    for nap in naps:
        for minute in range(nap.sleep, nap.wake):
            counts[(nap.guard_id, minute)] += 1

    [((gid1, min1), count1), ((gid2, min2), count2)] = counts.most_common(2)

    assert count1 > count2

    return (gid1, min1)


class Tests(unittest.TestCase):
    def test_regex(self):
        testline = "[1518-03-11 00:01] Guard #1091 begins shift"
        expected = ["1518", "03", "11", "00", "01", "Guard #1091 begins shift"]

        self.assertSequenceEqual(
            parse_line(testline),
            expected
        )

    def test_guard_regex(self):
        testline = "Guard #10 begins shift"
        expected = "10"

        self.assertEqual(
            parse_comment(testline).groups()[0],
            expected
        )

    def test_sleepiest(self):
        expected = 10
        naps = find_naps(RAW)

        self.assertEqual(
            sleepiest_guard(naps),
            expected            
        )

    def test_sleepiest_minute(self):
        expected = 24
        naps = find_naps(RAW)
        guard_id = sleepiest_guard(naps)

        self.assertEqual(
            sleepiest_minute(naps, guard_id),
            expected
        )

    def test_most_regular_sleeper(self):
        expected_id, expected_minute = 99, 45
        naps = find_naps(RAW)

        actual_id, actual_minute = most_regular_sleeper(naps)

        self.assertEqual(
            actual_id,
            expected_id
        )

        self.assertEqual(
            actual_minute,
            expected_minute
        )

if __name__ == "__main__":
    # unittest.main()

    with open('input.txt') as f:
        lines = [line.strip() for line in f]

    naps = find_naps(lines)
    guard = sleepiest_guard(naps)
    minute = sleepiest_minute(naps, guard)
    print("Guard:", guard, "Minute:", minute, "Product:", guard*minute)

    regular_id, regular_min = most_regular_sleeper(naps)
    print(regular_id * regular_min)