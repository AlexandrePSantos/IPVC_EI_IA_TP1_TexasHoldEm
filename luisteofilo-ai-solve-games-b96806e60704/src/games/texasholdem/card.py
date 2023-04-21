from enum import Enum


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'
    SPADES = 'spades'


class TexasCard:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank.value < other.rank.value

    def __str__(self):
        return f"{self.rank.name.lower()} of {self.suit.value}"
