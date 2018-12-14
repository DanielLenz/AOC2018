from typing import Set, NamedTuple, List, Dict, Set
import re

TESTINPUT = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

TESTRESULT = "CABDFE"

Preconditions = Dict[str, Set[str]]


class Step(NamedTuple):
    first: str
    second: str

    @staticmethod
    def from_line(line: str) -> "Step":
        rgx = "Step ([A-Z]) must be finished before step ([A-Z]) can begin."
        match = re.match(rgx, line)
        first, second = match.groups()

        return Step(first, second)

def get_preconditions(steps: List[Step]) -> Preconditions:

    unique_steps = {item for step in steps for item in [step.first, step.second]}
    preconds = {step: set() for step in unique_steps}

    for step in steps:
        preconds[step.second].add(step.first)

    return preconds

def find_order(steps: List[Step]) -> str:
    order = []

    preconds = get_preconditions(steps)

    while preconds:
        candidates = sorted([k for k, v in preconds.items() if not v])
        next_item = min(candidates)
        order.append(next_item)

        for req in preconds.values():
            if next_item in req:
                req.remove(next_item)

        del preconds[next_item]

    return "".join(order)


class WorkItem(NamedTuple):
    worker_id: int
    item: str
    start_time: int
    end_time: int


def get_step_time(step: str, base: int=60) -> int:
    step_time = ord(step) - ord('A') + 1 + base
    return step_time


def find_time(steps: List[Step], num_workers: int, base: int=60) -> int:
    preconds = get_preconditions(steps)

    time = 0

    work_items = [None for _ in range(num_workers)]

    while preconds or any(work_items):
        # Check if anyone is done, and remove those
        for i, work_item in enumerate(work_items):
            if work_item and work_item.end_time <= time:
                # This item is finished
                work_items[i] = None

                for reqs in preconds.values():
                    if work_item.item in reqs:
                        reqs.remove(work_item.item)
                
        # # Find items still in progress 
        # in_progress = {work_item.item for work_item in work_items if work_item}

        # Find available workers
        available_workers = [i for i in range(num_workers) if work_items[i] is None]

        # Find candidates for work
        candidates = sorted(
            [step for step, reqs in preconds.items() if not reqs], reverse=True)

        # Assign as much work as possible
        while available_workers and candidates:
            worker_id = available_workers.pop()
            item = candidates.pop()

            work_items[worker_id] = WorkItem(
                worker_id=worker_id,
                item=item,
                start_time=time,
                end_time=time+get_step_time(item, base),
            )

            del preconds[item]

        if any(work_items):
            time = min(work_item.end_time for work_item in work_items if work_item)

    return time



if __name__ == "__main__":
    testlines = TESTINPUT.split("\n")
    teststeps = [Step.from_line(line) for line in testlines]

    # s = Step.from_line(testlines[0])
    # print(s)

    with open('input.txt') as f:
        steps = [Step.from_line(line.strip()) for line in f]
    
    # print(steps)
    # print(find_order(steps))
    assert get_step_time('A') == 61
    assert get_step_time('Z') == 86
    assert get_step_time('B', base=0) == 2

    assert find_time(teststeps, num_workers=2, base=0) == 15

    print(find_time(steps, base=60, num_workers=5))