import re
from typing import Set, Tuple

TESTINPUT = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

State = Set[int]
Rule = Tuple[bool, bool, bool, bool, bool]
Rules = Set[Rule]

def parse_raw(input: str) -> Tuple[State, Rules]:
    lines = input.split('\n')
    
    # Parse initial state
    #####################
    rgx_init = "initial state: ([.#]*)"
    initial_state_raw = re.match(rgx_init, lines[0]).groups()[0]
    initial_state  = {i for i, plant in enumerate(initial_state_raw) if plant == '#'}

    # Parse the planting rules
    ##########################
    rules = set()
    rgx_rules = "([.#]{5}) => ([.#])"
    for line in lines[2:]:
        pattern, plant = re.match(rgx_rules, line).groups()
        if plant == '#':
            key = tuple([c == '#' for c in pattern])
            rules.add(key)

    return initial_state, rules


def step(state: State, rules: Rules) -> State:
    next_state = set()
    lo = min(state) - 2
    hi = max(state) + 2

    for plant in range(lo, hi + 1):
        key = tuple([
            other in state for other in
            [plant - 2, plant -1, plant, plant + 1, plant+2]])
        
        if key in rules:
            next_state.add(plant)

    return next_state

def count_plants(state: State, rules: Rules, n_generations: int=20) -> int:
    for _ in range(n_generations):
        state = step(state, rules)

    return sum(state)

if __name__ == "__main__":
    state, rules = parse_raw(TESTINPUT)
    assert count_plants(state, rules) == 325

    with open('input.txt') as f:
        raw = f.read().strip()

    state, rules = parse_raw(raw)
    # print(count_plants(state, rules))

    seen = {}   # Mapping from deltas => (generation, lowest)

    for gen in range(251):
        lowest = min(state)
        deltas = [plant - lowest for plant in state]
        key = tuple(sorted(deltas))
        print(gen, lowest, sum(state))

        if key in seen:
            print(key, seen[key])
        else:
            seen[key] = gen
        state = step(state, rules)
        gen += 1

    # In [7]: 4447 + 15 * (50_000_000_000 - 250)
    # Out[7]: 750000000697