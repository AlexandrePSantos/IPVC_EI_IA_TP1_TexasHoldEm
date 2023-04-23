from random import shuffle

from games.game_simulator import GameSimulator
from games.texasholdem.card import Rank, Suit, TexasCard
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState


class TexasSimulator(GameSimulator):

    def __init__(self, player1: TexasPlayer, player2: TexasPlayer):
        super().__init__([player1, player2])
        """
        deck of cards
        """
        self.__deck = [TexasCard(rank, suit) for rank in Rank for suit in Suit]
        self.state = TexasState()
        self.deck_copy = self.__deck.copy()
        self.state.set_deck(self.deck_copy)

    def init_game(self):
        shuffle(self.deck_copy)
        # assign two cards to each player
        positions = self.get_player_positions()
        for player in positions:
            cards = self.deck_copy[:2]
            player.set_current_hand(cards)

        return self.state

    def get_remaining_cards(self):
        return self.__deck

    def before_end_game(self, state: TexasState):
        # if we reached the show down, we are going to reveal the cards to all players
        if state.is_showdown():
            state.get_current_hands()

    def end_game(self, state: TexasState):
        # ignored for this simulator
        pass
