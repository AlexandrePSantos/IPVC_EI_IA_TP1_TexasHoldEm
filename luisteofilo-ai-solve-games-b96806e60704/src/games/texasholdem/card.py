from enum import Enum


class TexasCard(Enum):
    """
    A standard deck of cards for Texas Hold'em poker
    """
    TwoOfHearts = 0
    ThreeOfHearts = 1
    FourOfHearts = 2
    FiveOfHearts = 3
    SixOfHearts = 4
    SevenOfHearts = 5
    EightOfHearts = 6
    NineOfHearts = 7
    TenOfHearts = 8
    JackOfHearts = 9
    QueenOfHearts = 10
    KingOfHearts = 11
    AceOfHearts = 12
    TwoOfDiamonds = 13
    ThreeOfDiamonds = 14
    FourOfDiamonds = 15
    FiveOfDiamonds = 16
    SixOfDiamonds = 17
    SevenOfDiamonds = 18
    EightOfDiamonds = 19
    NineOfDiamonds = 20
    TenOfDiamonds = 21
    JackOfDiamonds = 22
    QueenOfDiamonds = 23
    KingOfDiamonds = 24
    AceOfDiamonds = 25
    TwoOfClubs = 26
    ThreeOfClubs = 27
    FourOfClubs = 28
    FiveOfClubs = 29
    SixOfClubs = 30
    SevenOfClubs = 31
    EightOfClubs = 32
    NineOfClubs = 33
    TenOfClubs = 34
    JackOfClubs = 35
    QueenOfClubs = 36
    KingOfClubs = 37
    AceOfClubs = 38
    TwoOfSpades = 39
    ThreeOfSpades = 40
    FourOfSpades = 41
    FiveOfSpades = 42
    SixOfSpades = 43
    SevenOfSpades = 44
    EightOfSpades = 45
    NineOfSpades = 46
    TenOfSpades = 47
    JackOfSpades = 48
    QueenOfSpades = 49
    KingOfSpades = 50
    AceOfSpades = 51

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

    def __str__(self):
        rank_names = {
            0: "2",
            1: "3",
            2: "4",
            3: "5",
            4: "6",
            5: "7",
            6: "8",
            7: "9",
            8: "10",
            9: "J",
            10: "Q",
            11: "K",
            12: "A"
        }
        suit_names = {
            0: "hearts",
            1: "diamonds",
            2: "clubs",
            3: "spades"
        }
        rank = rank_names[self.value % 13]
        suit = suit_names[self.value // 13]
        return rank + suit


"""
   # kuhn poker is played with 3 cards with no suits
    
    Jack = 0
    Queen = 1
    King = 2

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

    def __str__(self):
        return {
            0: "J",
            1: "Q",
            2: "K"
        }[self.value]
"""