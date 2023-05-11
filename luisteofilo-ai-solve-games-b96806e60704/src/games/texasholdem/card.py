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
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class TexasCard:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"

    def __str__(self):
        rank = self.rank.value if self.rank.value < 10 else {
            10: "T",
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }[self.rank.value]
        return f"{rank}{self.suit.value}"


