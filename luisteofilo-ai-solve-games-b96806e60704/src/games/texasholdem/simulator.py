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
        self.community_cards = [None, None, None, None, None]
        self.current_betting_round = 0

    def init_game(self):
        shuffle(self.__deck)
        # assign two cards to each player
        positions = self.get_player_positions()
        for player in positions:
            cards = self.__deck[:2]
            player.set_current_hand(cards)
            self.__deck = self.__deck[2:]

        # assign three community cards
        for i in range(3):
            self.community_cards[i] = self.__deck.pop()

        self.current_betting_round = 1

        return TexasState()

    def draw_community_card(self):
        # determine which community card to draw based on the current betting round
        if self.current_betting_round == 1:
            card_index = 3
        elif self.current_betting_round == 2:
            card_index = 4
        else:
            return

        # draw the next community card if it hasn't already been drawn
        if self.community_cards[card_index] is None:
            self.community_cards[card_index] = self.__deck.pop()

        # increment the current betting round
        self.current_betting_round += 1

    def before_end_game(self, state: TexasState):
        # draw the next community card if we're not in the final betting round
        if self.current_betting_round < 4:
            self.draw_community_card()
        # reveal all the cards when the game is over, one player folds, or last round of betting
        if state.is_showdown() or state.get_current_betting_round() == 4:
            for pos in range(self.num_players()):
                state.draw_card(pos, self.__deck[pos])

    def end_game(self, state: TexasState):
        # ignored for this simulator
        pass
