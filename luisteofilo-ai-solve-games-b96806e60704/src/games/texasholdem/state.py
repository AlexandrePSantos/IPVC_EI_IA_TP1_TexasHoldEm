from games.texasholdem.action import TexasAction
from games.texasholdem.card import TexasCard
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
        self.__community_cards = [None, None, None, None, None]
        self.__parsed_hands = []

    def get_num_players(self):
        return 2

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
        # segunda ronda metem mais uma carta                            !!TURN!!
        elif len(self.__sequence) == 4:
            print(self.__sequence)
            self.__community_cards[3] = self.__deck.pop()
        # terceira ronda após apostas metem mais uma e será a última    !!RIVER!!
        elif len(self.__sequence) == 6:
            print(self.__sequence)
            self.__community_cards[4] = self.__deck.pop()
        # ultima ronda de bets !!SHOWDOWN!!
        elif len(self.__sequence) == 8:
            self.__is_finished = True

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    def get_pot(self):
        print(self.__bets)
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
            player_hand_value = self.calculate_hand_value()[pos]
            opponent_hand_value = self.calculate_hand_value()[opp_pos]

            # determine the winner based on hand value
            if player_hand_value > opponent_hand_value:
                return pot
            elif opponent_hand_value > player_hand_value:
                return -pot
            else:
                return pot / 2
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            return pot if self.__bets[pos] > self.__bets[opp_pos] else pot

    def before_results(self):
        pass

    def is_finished(self) -> bool:
        return self.__is_finished

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence

    # CONVERTER CARTAS DE STR PARA VALOR NUMERICO
    @staticmethod
    def parse_hand(hand: List[TexasCard]) -> List[int]:
        return [card.parse() for card in hand]

    def parse_hands(self):
        self.__parsed_hands = []
        for hand in self.__hands:
            parsed_hand = TexasState.parse_hand(hand)
            if self.__community_cards:
                parsed_hand += TexasState.parse_hand(self.__community_cards)
            self.__parsed_hands.append(parsed_hand)

    # CALCULAR HANDS
    def calculate_hand_value(self) -> List[int]:
        hand_values = []
        for parsed_hand in self.__parsed_hands:
            # Combine parsed hand and community cards into a single list
            cards = parsed_hand
            # Sort the cards by rank
            cards.sort(key=lambda c: c.rank.value, reverse=True)
            # Check for highest-ranking hand first, move on to lower-ranking hands if highest-ranking not present
            if TexasEvaluator.is_royal_flush(cards):
                print("10")
                hand_values.append(10)
            elif TexasEvaluator.is_straight_flush(cards):
                print("2")
                hand_values.append(9)
            elif TexasEvaluator.is_four_of_a_kind(cards):
                print("3")
                hand_values.append(8)
            elif TexasEvaluator.is_full_house(cards):
                print("4")
                hand_values.append(7)
            elif TexasEvaluator.is_flush(cards):
                print("5")
                hand_values.append(6)
            elif TexasEvaluator.is_straight(cards):
                print("6")
                hand_values.append(5)
            elif TexasEvaluator.is_three_of_a_kind(cards):
                print("7")
                hand_values.append(4)
            elif TexasEvaluator.is_two_pair(cards):
                print("8")
                hand_values.append(3)
            elif TexasEvaluator.is_pair(cards):
                print("9")
                hand_values.append(2)
            else:
                print("1")
                hand_values.append(1)
        return hand_values

    # DISPLAY
    def display(self):
        for action in self.__sequence:
            print('b' if action == TexasAction.BET else 'p', end="")
        print(f": pot = {self.get_pot()}")

    def display_community_cards(self):
        print("Community Cards: " + ", ".join(str(card) for card in self.__community_cards if card is not None))
