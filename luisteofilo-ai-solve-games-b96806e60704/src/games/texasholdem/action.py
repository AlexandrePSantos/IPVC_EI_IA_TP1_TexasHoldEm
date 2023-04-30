from enum import Enum


class TexasAction(Enum):
    """
    a pass is either a check (no money is in the table) or a fold (if there is a bet)
    a bet is either a regular bet (no money in the table) or a call (if there is a bet)
    """
    PASS = 0,
    CALL = 1,
    RAISE = 2

    # 0 - PASS -> FOLD ou CHECK
    # 1 - CALL -> iguala ás mão do oponente se for mais alta
    # 2 - RAISE ->  mete +1 que o valor do oponente

    # FOLD -> desiste da mão
    # CHECK -> desiste da ronda atual mas continua com a mão
    # CALL -> igualar aposta mais alta feita
    # RAISE -> aumenta o valor da aposta e passa a ser a mais alta
