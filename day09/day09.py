import sys
from typing import NamedTuple, List
from collections import deque


def play_marbles_old(num_players: int, highest_marble: int) -> List[int]:
    scores = [0 for _ in range(num_players)]

    marbles = [0]
    curr = 0  # Index of current marble
    current_player = 0

    for marble in range(1, highest_marble + 1):
        # print(current_player, marbles, curr, marble)
        if marble % 23 == 0:
            # Remove marble
            curr = (curr - 7) % len(marbles)
            bonus = marbles.pop(curr)
            # Update score
            scores[current_player] += bonus + marble

            curr = curr % len(marbles)
        else:
            curr = ((curr + 1) % len(marbles)) + 1
            marbles.insert(curr, marble)

        current_player = (current_player + 1) % num_players


    return scores


def play_marbles(num_players: int, highest_marble: int) -> List[int]:
    """We use a deque, always keeping the current marble at index 0."""
    scores = [0 for _ in range(num_players)]

    marbles = deque([0])
    current_player = 0

    def move_left(n: int=1) -> None:
        for _ in range(n):
            val = marbles.pop()
            marbles.appendleft(val)

    def move_right(n: int=1) -> None:
        for _ in range(n):
            val = marbles.popleft()
            marbles.append(val)

    for marble in range(1, highest_marble + 1):
        # print(current_player, marbles, curr, marble)
        if marble % 23 == 0:
            scores[current_player] += marble
            # Remove marble
            move_left(7)
            scores[current_player] += marbles.popleft()
        else:
            move_right(2)
            marbles.appendleft(marble)

        current_player = (current_player + 1) % num_players

    return scores



if __name__ == "__main__":
    n_players_test, last_marble_test, expected_test = 9, 25, 32
    play_marbles(n_players_test, last_marble_test)
    # sys.exit()

    # Tests
    test_ins = [(9, 25), (10, 1618), (13, 7999), (17, 1104), (21, 6111), (30, 5807)]
    test_outs = [32, 8317, 146373, 2764, 54718, 37305]

    for test_in, test_out in zip(test_ins, test_outs):
        # print(test_in)
        assert max(play_marbles(*test_in)) == test_out

    # Actual data 
    n_players, last_marble = 466, 71436
    print(max(play_marbles(n_players, last_marble)))
    print(max(play_marbles(n_players, last_marble*100)))


