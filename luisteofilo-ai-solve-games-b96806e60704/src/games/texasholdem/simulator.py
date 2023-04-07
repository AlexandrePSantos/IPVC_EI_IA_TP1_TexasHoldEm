from random import shuffle

from games.game_simulator import GameSimulator
from games.texasholdem.card import TexasCard
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState


class TexasSimulator(GameSimulator):

    def __init__(self, player1: TexasPlayer, player2: TexasPlayer):
        super().__init__([player1, player2])
        """
        deck of cards
        """
        deck = list(TexasCard)
        self.__deck = deck
        # self.__deck = [TexasCard.Jack, TexasCard.Queen, TexasCard.King]

    def init_game(self):
        # shuffle the deck
        shuffle(self.__deck)

        # assign two cards to each player
        positions = self.get_player_positions()
        for player in positions:
            cards = self.__deck[:2]
            player.set_current_cards(cards)
            self.__deck = self.__deck[2:]

        # assign three community cards
        for i in range(3):
            self.state.add_community_card(self.__deck.pop())

        return TexasState()

        # assign a card to each player
        # positions = self.get_player_positions()
        # for pos in range(0, len(positions)):
        #     positions[pos].set_current_card(self.__deck[pos])

    def before_end_game(self, state: TexasState):
        # reveal all the cards when the game is over, one player folds, or last round of betting
        if state.is_game_over() or state.get_active_players() == 1 or state.get_current_betting_round() == 4:
            for pos in range(self.num_players()):
                state.draw_card(pos, self.__deck[pos])

        # if we reached the showdown, we are going to reveal the cards to all players
        # if state.is_showdown():
        #     for pos in range(0, self.num_players()):
        #         state.draw_card(pos, self.__deck[pos])

    def end_game(self, state: TexasState):
        # ignored for this simulator
        pass
