from enum import Enum


class TexasAction(Enum):
    """
    a pass is either a check (no money is in the table) or a fold (if there is a bet)
    a bet is either a regular bet (no money in the table) or a call (if there is a bet)
    """
    PASS = 0
    BET = 1

    # FOLD = 0
    # CHECK = 1
    # CALL = 2
    # RAISE = 3
    # BET = 4
    # ALLIN = 5

    # FOLD -> desiste da mão
    # CHECK -> desiste da ronda atual mas continua com a mão
    # CALL -> igualar aposta mais alta feita
    # RAISE -> aumenta o valor da aposta e passa a ser a mais alta
