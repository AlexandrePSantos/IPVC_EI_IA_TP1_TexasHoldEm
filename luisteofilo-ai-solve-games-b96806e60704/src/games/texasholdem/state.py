from games.texasholdem.action import TexasAction
from games.texasholdem.card import TexasCard
from games.state import State
from typing import List


class TexasState(State):

    def __init__(self):
        super().__init__()
        """
        the sequence of plays
        """
        self.__sequence = []
        """
        the acting player index
        """
        self.__acting_player = 0
        """
        indicates if the game is finished
        """
        self.__is_finished = False
        """
        the cards that were seen so far and the deck
        """
        self.__deck = []
        self.__hands = []
        self.__community_cards = [None, None, None, None, None]
        """
        bets
        """
        self.__bets = [1, 1]
        """
        indicates if the game is in showdown (actions are finished and players are about to reveal the cards)
        """
        self.__is_showdown = False
        self.cur_bet_round = 0

    @staticmethod
    def get_num_players():
        return 2

    def set_deck(self, deck):
        self.__deck = deck

    def validate_action(self, action) -> bool:
        return not self.__is_finished and action is not None

    def update(self, action):
        # only need to check the outcome of the action if none was added until now
        if len(self.__sequence) > 0:
            last_action = self.__sequence[-1]

            if last_action == TexasAction.BET:
                self.__is_finished = True
                if action == TexasAction.BET:
                    self.__is_showdown = True
            else:
                if action == TexasAction.PASS:
                    self.__is_finished = True
                    self.__is_showdown = True

        self.__sequence.append(action)

        # if someone is betting, we are going to increase its bet amount
        if action == TexasAction.BET:
            self.__bets[self.__acting_player] += 1

        # check if the first round of betting is complete (both players have acted)
        if len(self.__sequence) == 2:
            # draw community cards
            self.draw_community_card()

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    def set_community_cards(self, cards: List[TexasCard]):
        self.__community_cards = cards

    def draw_community_card(self):
        if self.cur_bet_round <= 1:
            for i in range(3):
                if self.__community_cards[i] is None:
                    self.__community_cards[i] = self.__deck.pop()
            self.cur_bet_round += 1
        elif self.cur_bet_round == 2:
            if self.__community_cards[self.cur_bet_round] is None:
                self.__community_cards[self.cur_bet_round] = self.__deck.pop()
            self.cur_bet_round += 1
        elif self.cur_bet_round <= 4:
            if self.__community_cards[self.cur_bet_round] is None:
                self.__community_cards[self.cur_bet_round] = self.__deck.pop()
            self.cur_bet_round += 1

    def get_comm_cards(self):
        return self.__community_cards

    def display(self):
        for action in self.__sequence:
            print('b' if action == TexasAction.BET else 'p', end="")
        print(f": pot = {self.get_pot()}")

    def display_community_cards(self):
        print("Community Cards: " + ", ".join(str(card) for card in self.__community_cards if card is not None))

    """
    get the total amount that was put into bets so far
    """
    def get_pot(self):
        return sum(self.__bets)

    def is_finished(self) -> bool:
        return self.__is_finished

    def get_acting_player(self) -> int:
        return self.__acting_player

    def get_cur_bet_round(self):
        return self.cur_bet_round

    def clone(self):
        cloned = TexasState()
        cloned.__bets = self.__bets.copy()
        cloned.__sequence = self.__sequence.copy()
        cloned.__is_finished = self.__is_finished
        cloned.__acting_player = self.__acting_player
        for i in range(0, len(self.__hands)):
            cloned.__hands[i] = self.__hands[i].copy()
        cloned.__community_cards = self.__community_cards.copy()
        cloned.__is_showdown = self.__is_showdown
        return cloned

    def get_result(self, pos):
        # no result if the game is not finished
        if not self.__is_finished:
            return None

        # if we are finished and we have a showdown, the cards must be available
        if self.__is_showdown:
            for card in self.__hands:
                if card is None:
                    return None

        pot = self.get_pot()
        opp_pos = 1 if pos == 0 else 0

        if self.__is_showdown:
            # noinspection PyTypeChecker
            # if there is a showdown, we will give 1 or 2 to the player with the best card and -1 or -2 to the looser
            return (1 if self.__hands[pos] > self.__hands[opp_pos] else -1) * (pot / 2)
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            return 1 if self.__bets[pos] > self.__bets[opp_pos] else -1

    def before_results(self):
        pass

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence

    # def hand_community(self):
    #     combination = []
    #     positions = self.get_player_positions()
    #     for player in positions:
    #         combination = player.get_current_hand()
    #         combined_hand = self.__hands + self.__community_cards
    #         combination.append(combined_hand)
    #     return combination
    #