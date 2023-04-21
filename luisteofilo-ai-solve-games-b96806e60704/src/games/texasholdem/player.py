from abc import ABC
from typing import List
from games.player import Player
from games.texasholdem.card import TexasCard


class TexasPlayer(Player, ABC):

    def __init__(self, name):
        super().__init__(name)

        """
        score will store the money earned (or lost)
        """
        self.__score = 0

        """
        here we are storing the number of games
        """
        self.__num_games = 0

        """
        we also need to store the current cards we are holding
        """
        self.__current_hand = [None, None]

    """
    assigns 2 cards to the player
    """
    def set_current_hand(self, cards: List[TexasCard]):
        self.__current_hand = cards

    """
    gets the current player's hand
    """
    def get_current_hand(self):
        return self.__current_hand

    """
    gets the score
    """
    def get_score(self):
        return self.__score

    """
    gets the score
    """
    def get_expected_value(self):
        return self.__score * 1.0 / self.__num_games

    def event_new_game(self):
        self.__num_games += 1

    def event_result(self, pos: int, result: int):
        if pos == self.get_current_pos():
            self.__score += result

    def print_stats(self):
        print(f"Player {self.get_name()} | Total profit: ${self.__score} "
              f"| Profit per game: ${self.get_expected_value()}")
