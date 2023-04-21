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
        self.community_cards = [None, None, None, None, None]
        self.cur_bet_round = 0

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

        return TexasState()

    def draw_community_card(self):
        # determine which community card to draw based on the current betting round
        if self.cur_bet_round == 1:
            card_index = 3
        elif self.cur_bet_round == 2:
            card_index = 4
        else:
            return

        # draw the next community card if it hasn't already been drawn
        if self.community_cards[card_index] is None:
            self.community_cards[card_index] = self.__deck.pop()

        # increment the current betting round
        self.cur_bet_round += 1

    def get_remaining_cards(self):
        return self.__deck

    def get_cur_bet_round(self):
        return self.cur_bet_round

    def hand_cummunity(self):
        hands = []
        positions = self.get_player_positions()
        for player in positions:
            hand = player.get_current_hand()
            combined_hand = hand + self.community_cards
            hand.append(combined_hand)
        return hands

    def before_end_game(self, state: TexasState):
        # reveal all the cards
        if state.is_showdown():
            for pos in range(0, self.num_players()):
                player = self.get_player(pos)
                combined_hand = self.hand_community(player)
                state.draw_card(pos, combined_hand)

    def end_game(self, state: TexasState):
        # ignored for this simulator
        pass
