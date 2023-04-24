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
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'


class TexasCard:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"

    def __str__(self):
        # if self.rank.value == 11:
        #     return f"J{self.suit.value}"
        # elif self.rank.value == 12:
        #     return f"Q{self.suit.value}"
        # elif self.rank.value == 13:
        #     return f"K{self.suit.value}"
        # elif self.rank.value == 14:
        #     return f"A{self.suit.value}"
        # else:
            return f"{self.rank.value}{self.suit.value}"

    def parse(self) -> int:
        rank_value = self.rank.value
        if rank_value <= 10:
            return rank_value
        elif rank_value == 11:
            return 11  # Jack
        elif rank_value == 12:
            return 12  # Queen
        elif rank_value == 13:
            return 13  # King
        elif rank_value == 14:
            return 14  # Ace

    # HEARTS = '♥'
    # DIAMONDS = '♦'
    # CLUBS = '♣'
    # SPADES = '♠'
