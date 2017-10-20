from collections import namedtuple, defaultdict
from enum import Enum
import random

# card value -> # of cards of that value per color
VALUE_DISTRIBUTION = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}

# # players -> # cards/player
HAND_DISTRIBUTION = {
    2: 5,
    3: 5,
    4: 4,
    5: 4
 }

NUM_TIME_TOKENS = 8

NUM_BOMBS = 4

Color = Enum('Color', 'WHITE RED YELLOW GREEN BLUE')

Card = namedtuple('Card', 'color value')

State = Enum('State', 'NOT_STARTED PLAYING FINAL_ROUND ENDED')

Hint = namedtuple('Hint', 'indices type_ content')

HintType = Enum('HintType', 'COLOR VALUE')

def gen_cards():
    cards = []
    for color in Color:
        for value in range(1, 6):
            for _ in range(VALUE_DISTRIBUTION[value]):
                cards.append(Card(color, value))
    random.shuffle(cards)
    return cards

class Player:
    def __init__(self, pid):
        self.pid = pid
        self.hand =[]

class StateDFA:
    def __init__(self):
        self.state = State.NOT_STARTED
        self.whose_turn = 0
        self.ends_with = 0
        self.won = False
        self.lost = False

    def start(self, starting_player=0):
        assert self.state == State.NOT_STARTED
        self.state = State.PLAYING
        self.whose_turn = starting_player

    def play(self, num_cards_left):
        assert self.state == State.PLAYING or self.state == State.FINAL_ROUND
        if self.state == State.PLAYING:
            # TODO

class Game:
    def __init__(
            self,
            gid,
            pids=[],
            time_tokens=NUM_TIME_TOKENS,
            bombs=NUM_BOMBS):
        self.gid = gid
        self.players = list(map(lambda pid: Player(pid, []), pids))
        self.deck = gen_cards()
        self.discarded = []
        self.num_hints = time_tokens
        self.max_hints = time_tokens
        self.lives = bombs
        self.board = defaultdict(int)
        self.state = GameState.PLAYING

    def add_pid(self, pid):
        assert self.state == GameState.NOT_STARTED
        assert 0 <= len(self.pids) <= 4
        self.pids.append(pid)

    def start(self):
        assert self.state == GameState.NOT_STARTED
        assert 2 <= len(self.pids) <= 5
        self.state = GameState.PLAYING
        random.shuffle(self.pids)
        for pid in self.pids:
            for _ in range(HAND_DISTRIBUTION[len(self.pids)]):
                self.hands[pid].append(self.deck.pop())

    def hint(self, from_pid, to_pid, hint):
        assert self.state == GameState.PLAYING
        assert self.pids[self.playing_index] == from_pid
        assert to_pid in self.pids
        assert from_pid != to_pid
        assert self.validate_hint(hint, self.hands[to_pid])
        self.hints[to_pid].append(hint)

    def validate_hint(self, hint, hand):
        complete_indices = set()
        for i, card in enumerate(hand):
            if ((hint.type_ == HintType.COLOR and hint.contents == card.color) or
               (hint.type_ == HintType.VALUE and hint.contents == card.value)):
                complete_indices.add(i)
        return (complete_indices == set(hint.indices) and
                len(complete_indices) > 0)
