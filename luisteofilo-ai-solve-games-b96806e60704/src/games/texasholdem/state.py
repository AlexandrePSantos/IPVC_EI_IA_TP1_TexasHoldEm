from games.texasholdem.action import TexasAction
from games.texasholdem.card import Rank, Suit, TexasCard
from games.texasholdem.evaluate import TexasEvaluator
from games.state import State
from typing import List

evaluate = TexasEvaluator()


class TexasState(State):

    def __init__(self):
        super().__init__()
        self.__sequence = []
        self.__acting_player = 0
        self.__is_finished = False
        self.__is_showdown = False
        self.__bets = [1, 2]
        # new attributes
        self.__deck = []
        self.__combined_hc_cc = []
        self.__hands = [[] for _ in range(2)]
        self.__community_cards = [None, None, None, None, None]
        self.__hand_values = []

    @staticmethod
    def get_num_players():
        return 2

    def set_hands(self, hands):
        self.__hands = hands

    def set_deck(self, deck):
        self.__deck = deck

    def get_current_hands(self):
        return self.__hands

    def get_community_cards(self):
        return self.__community_cards

    def get_combined_cards(self, pos):
        return self.__combined_hc_cc

    def get_combined_cards1(self):
        return self.__combined_hc_cc[1]

    def get_combined_cards0(self):
        return self.__combined_hc_cc[0]

    def get_bets(self):
        return self.__bets

    # VALIDA AÇÕES
    def validate_action(self, action) -> bool:
        return not self.__is_finished and action is not None

    # ATUALIZAR ESTADO D JOGO
    def update(self, action):
        self.__sequence.append(action)

        if action == TexasAction.CALL or action == TexasAction.RAISE or action == TexasAction.PASS:
            if len(self.__sequence) == 8:
                self.__is_finished = True
                self.__is_showdown = True
            elif len(self.__sequence) == 6:      # fourth round (river)
                print(f"\n> Round 4 - River <")
                self.__community_cards[4] = self.__deck.pop()
                self.__combined_hc_cc = self.combine_cards()
                self.__hand_values = evaluate.calculate_hand_value(self.__combined_hc_cc)
            elif len(self.__sequence) == 4:    # third round (turn)
                print(f"\n> Round 3 - Turn <")
                self.__community_cards[3] = self.__deck.pop()
                self.__combined_hc_cc = self.combine_cards()
                self.__hand_values = evaluate.calculate_hand_value(self.__combined_hc_cc)
            elif len(self.__sequence) == 2:    # second round (flop)
                print(f"\n> Round 2 - Flop <")
                for i in range(3):
                    if self.__community_cards[i] is None:
                        self.__community_cards[i] = self.__deck.pop()
                self.__combined_hc_cc = self.combine_cards()
                self.__hand_values = evaluate.calculate_hand_value(self.__combined_hc_cc)

        oth_player = 1 if self.__acting_player == 0 else 0
        # if someone is betting, we are going to increase its bet amount
        if action == TexasAction.CALL:
            self.__bets[self.__acting_player] = self.__bets[oth_player]
        if action == TexasAction.RAISE:
            self.__bets[self.__acting_player] = self.__bets[oth_player] + 1

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    # DISPLAY
    def display(self):
        print(f"> Community cards = {self.get_community_cards()}")
        print(f"> Pot = {self.get_pot()}")
        print(f"> Bets = {self.get_bets()}")

    def get_pot(self):
        return sum(self.__bets)

    def get_acting_player(self) -> int:
        return self.__acting_player

    # CLONAR ESTADO ATUAL
    def clone(self):
        cloned = TexasState()
        cloned.__bets = self.__bets.copy()
        cloned.__sequence = self.__sequence.copy()
        cloned.__is_finished = self.__is_finished
        cloned.__acting_player = self.__acting_player
        cloned.__hands = self.__hands
        cloned.__community_cards = self.__community_cards
        cloned.__combined_hc_cc = self.__combined_hc_cc
        cloned.__is_showdown = self.__is_showdown
        return cloned

    # PREVISÃO DE RESULTADOS
    def get_result(self, pos):
        # no result if the game is not finished
        if not self.__is_finished:
            return None

        # if we are finished and we have a showdown, the cards must be available
        if self.__is_showdown:
            for hand in self.__hands:
                for card in hand:
                    if card is None:
                        return None

        pot = self.get_pot()
        opp_pos = 1 if pos == 0 else 0
        player_hand_value = self.__hand_values[pos]
        opponent_hand_value = self.__hand_values[opp_pos]

        if self.__is_showdown:
            # if there is a showdown, we will give 1 or 2 to the player with the best card and -1 or -2 to the looser
            if player_hand_value > opponent_hand_value:
                return 1 * pot
            elif player_hand_value == opponent_hand_value:
                return 1 * (pot / 2)
            elif player_hand_value < opponent_hand_value:
                return -1 * pot
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            return 1 if self.__bets[pos] > self.__bets[opp_pos] else -1

    def before_results(self):
        pass

    def is_finished(self) -> bool:
        return self.__is_finished

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence

    # # COMBINE HANDS WITH COMMUNITY CARDS
    def combine_cards(self) -> List[List[TexasCard]]:
        combined_hc_cc = []
        for hand in self.__hands:
            combined_hand = hand + [card for card in self.__community_cards if card is not None]
            combined_hc_cc.append(combined_hand)
        self.__combined_hc_cc = combined_hc_cc
        return combined_hc_cc
