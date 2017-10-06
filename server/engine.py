from collections import namedtuple
from enum import Enum
import random

NUMBER_DISTRIBUTION = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}

Color = Enum('Color', 'WHITE RED YELLOW GREEN BLUE')

Card = namedtuple('Card', 'color value')

class Deck:
    def __init__(self, shuffle_seed=random.random):
        self.cards = []
        for color in Color:
            for value in range(1, 6):
                for _ in range(NUMBER_DISTRIBUTION[value]):
                    self.cards.append(Card(color, value))
        random.shuffle(self.cards, shuffle_seed)

class Game:
    def __init__(self, players):
        pass
