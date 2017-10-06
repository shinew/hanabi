from collections import namedtuple, defaultdict
from enum import Enum
from random import sample

VALUE_DISTRIBUTION = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}

NUM_TIME_TOKENS = 8

NUM_BOMBS = 4

Color = Enum('Color', 'WHITE RED YELLOW GREEN BLUE')

Card = namedtuple('Card', 'color value')

GameState = Enum('GameState', 'NOT_STARTED PLAYING FINISHED')

def gen_cards(shuffle):
    cards = []
    for color in Color:
        for value in range(1, 6):
            for _ in range(VALUE_DISTRIBUTION[value]):
                cards.append(Card(color, value))
    return shuffle(cards)

class Game:
    def __init__(
            self,
            gid,
            pids=[],
            shuffle=lambda x: sample(x, k=len(x)),
            time_tokens=NUM_TIME_TOKENS,
            bombs=NUM_BOMBS):
        self.gid = gid
        self.pids = pids
        self.shuffle = shuffle
        self.deck = gen_cards(shuffle)
        self.time_tokens = time_tokens
        self.bombs = bombs
        self.playing_index = 0
        self.hands = defaultdict(list)
        self.table = defaultdict(int)
        self.state = GameState.PLAYING

    def add_pid(self, pid):
        assert self.state == GameState.NOT_STARTED
        assert 0 <= len(self.pids) <= 4
        self.pids.append(pid)

    def start(self):
        assert self.state == GameState.NOT_STARTED
        assert 2 <= len(self.pids) <= 5
        self.state = GameState.PLAYING
        self.pids = self.shuffle(self.pids)
