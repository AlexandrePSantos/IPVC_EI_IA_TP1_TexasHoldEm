from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.card import Rank, Suit, TexasCard
from games.texasholdem.evaluate import TexasEvaluator
from games.state import State
from typing import List


class TexasState(State):

    def __init__(self):
        super().__init__()
        self.__sequence = []
        self.__acting_player = 0
        self.__is_finished = False
        self.__bets = [1, 1]
        self.__is_showdown = False
        # new attributes
        self.__deck = []
        self.__hands = [[] for _ in range(2)]
        self.__parsed_hands = [[] for _ in range(2)]
        self.__community_cards = [None, None, None, None, None]
        self.__hand_values = []

    def get_num_players(self):
        return 2

    def set_hands(self, hands):
        self.__hands = hands

    def set_deck(self, deck):
        self.__deck = deck

    # HANDS ATUAIS
    def get_current_hands(self):
        return self.__hands

    # VALIDA AÇÕES
    def validate_action(self, action) -> bool:
        return not self.__is_finished and action is not None

    # ATUALIZAR ESTADO D JOGO
    def update(self, action):
        # only need to check the outcome of the action if none was added until now
        if len(self.__sequence) > 0:
            last_action = self.__sequence[-1]

            if last_action == TexasAction.BET and len(self.__sequence) == 8:
                self.__is_finished = True
                if action == TexasAction.BET and len(self.__sequence) == 8:
                    self.__is_showdown = True
            else:
                if action == TexasAction.PASS and len(self.__sequence) == 8:
                    self.__is_finished = True
                    self.__is_showdown = True

        self.__sequence.append(action)

        # if someone is betting, we are going to increase its bet amount
        if action == TexasAction.BET:
            self.__bets[self.__acting_player] += 1

        # primeira ronda de apostas feita metem tres cards na mesa      !!FLOP!!
        if len(self.__sequence) == 2:
            print(self.__sequence)
            # draw community cards
            for i in range(3):
                if self.__community_cards[i] is None:
                    self.__community_cards[i] = self.__deck.pop()
            self.__hand_values = self.calculate_hand_value()
        # segunda ronda metem mais uma carta                            !!TURN!!
        elif len(self.__sequence) == 4:
            print(self.__sequence)
            self.__community_cards[3] = self.__deck.pop()
            self.__hand_values = self.calculate_hand_value()
        # terceira ronda após apostas metem mais uma e será a última    !!RIVER!!
        elif len(self.__sequence) == 6:
            print(self.__sequence)
            self.__community_cards[4] = self.__deck.pop()
            self.__hand_values = self.calculate_hand_value()
        # ultima ronda de bets !!SHOWDOWN!!
        elif len(self.__sequence) == 8:
            self.__is_finished = True

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    def get_pot(self):
        # print(self.__bets)
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
        for i in range(0, len(self.__hands)):
            cloned.__hands[i] = self.__hands[i].copy()
        cloned.__community_cards = self.__community_cards.copy()
        cloned.__is_showdown = self.__is_showdown
        return cloned

    # PREVISÃO DE RESULTADOS
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
            player_hand_value = self.__hand_values[pos]
            opponent_hand_value = self.__hand_values[opp_pos]

            # determine the winner based on hand value
            if player_hand_value > opponent_hand_value:
                return pot
            elif opponent_hand_value > player_hand_value:
                return -pot
            else:
                if self.__bets[pos] == self.__bets[opp_pos]:
                    return self.__bets[pos]
                else:
                    return pot / 2
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            if self.__bets[pos] > self.__bets[opp_pos]:
                return pot
            elif self.__bets[pos] == self.__bets[opp_pos]:
                return self.__bets[pos]
            else:
                return 0

    def before_results(self):
        pass

    def is_finished(self) -> bool:
        return self.__is_finished

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence

    # CONVERTER CARTAS DE STR PARA VALOR NUMERICO
    def parse_hands(self) -> List[List[TexasCard]]:
        parsed_hands = []
        for i, hand in enumerate(self.__hands):
            # print(f"hand {i}: {hand}")
            parsed_hand = []
            for card_str in hand:
                # print(f"card_str: {card_str}")
                card_str = str(card_str)
                rank_str = card_str[:-1]
                # print(f"rank_str: {rank_str}")
                suit_str = card_str[-1]
                # print(f"suit_str: {suit_str}")
                rank = Rank(int(rank_str))
                suit = Suit(suit_str)
                card = TexasCard(rank, suit)
                parsed_hand.append(card)
            print(f"parsed_hand {i}: {parsed_hand}")
            self.__parsed_hands.append(parsed_hand)
        # community cards
        parsed_community_cards = []
        counter = 0
        for card_str in self.__community_cards:
            if card_str is None:
                break
            card_str = str(card_str)
            rank_str = card_str[:-1]
            suit_str = card_str[-1]
            rank = Rank(int(rank_str))
            suit = Suit(suit_str)
            card = TexasCard(rank, suit)
            if card not in parsed_community_cards:
                parsed_community_cards.append(card)
        self.__parsed_hands[0].append(parsed_community_cards)
        self.__parsed_hands[1].append(parsed_community_cards)
        print(self.__parsed_hands)
        return self.__parsed_hands

    # [[11C, 2C, 11H, 7C, 2H], [14H, 10D, 11H, 7C, 2H]]
    # CALCULAR HANDS -> List[int]
    def calculate_hand_value(self):
        self.parse_hands()
        # print(self.get_current_hands())
        # print("# parse hand" + str(self.__parsed_hands))
        # for parsed_hand in self.__parsed_hands:
        #     # Combine parsed hand and community cards into a single list
        #     cards = [c for c in parsed_hand if c is not None]
        #     cards.sort(key=lambda c: c.rank.value, reverse=True)
        #     # Check for highest-ranking hand first, move on to lower-ranking hands if highest-ranking not present
        #     if TexasEvaluator.is_royal_flush(cards):
        #         self.__hand_values.append(10)
        #     elif TexasEvaluator.is_straight_flush(cards):
        #         self.__hand_values.append(9)
        #     elif TexasEvaluator.is_four_of_a_kind(cards):
        #         self.__hand_values.append(8)
        #     elif TexasEvaluator.is_full_house(cards):
        #         self.__hand_values.append(7)
        #     elif TexasEvaluator.is_flush(cards):
        #         self.__hand_values.append(6)
        #     elif TexasEvaluator.is_straight(cards):
        #         self.__hand_values.append(5)
        #     elif TexasEvaluator.is_three_of_a_kind(cards):
        #         self.__hand_values.append(4)
        #     elif TexasEvaluator.is_two_pair(cards):
        #         self.__hand_values.append(3)
        #     elif TexasEvaluator.is_pair(cards):
        #         self.__hand_values.append(2)
        #     else:
        #         self.__hand_values.append(1)
        # return self.__hand_values

    # DISPLAY
    def display(self):
        for action in self.__sequence:
            print('b' if action == TexasAction.BET else 'p', end="")
        print(f": pot = {self.get_pot()}")

    def display_community_cards(self):
        print("Community Cards: " + ", ".join(str(card) for card in self.__community_cards if card is not None))
