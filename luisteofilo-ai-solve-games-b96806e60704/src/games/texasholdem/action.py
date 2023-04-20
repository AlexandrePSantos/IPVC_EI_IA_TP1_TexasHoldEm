from enum import Enum


class TexasAction(Enum):
    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE = 3
    BET = 4
    BLIND = 5
    BIG_BLIND = 6
