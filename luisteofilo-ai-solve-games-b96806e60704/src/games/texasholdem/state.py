from games.texasholdem.action import TexasAction
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
        self.__is_showdown = False
        self.__bets = [1, 2]
        # new attributes
        self.__deck = []
        self.__hands = [[] for _ in range(2)]
        self.__parsed_hands = []
        self.__parsed_hands_no_comm = []
        self.__community_cards = [None, None, None, None, None]
        self.__hand_values = []

    @staticmethod
    def get_num_players():
        return 2

    def set_hands(self, hands):
        self.__hands = hands

    def set_deck(self, deck):
        self.__deck = deck

    # HANDS ATUAIS
    def get_current_hands(self):
        return self.__hands

    def get_bets(self):
        return self.__bets

    def get_community_cards(self):
        return self.__community_cards

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
                self.__hand_values = self.calculate_hand_value()
                print(f"> Community cards: {self.__community_cards}")
            elif len(self.__sequence) == 4:    # third round (turn)
                print(f"\n> Round 3 - Turn <")
                self.__community_cards[3] = self.__deck.pop()
                self.__hand_values = self.calculate_hand_value()
                print(f"> Community cards: {self.__community_cards}")
            elif len(self.__sequence) == 2:    # second round (flop)
                print(f"\n> Round 2 - Flop <")
                for i in range(3):
                    if self.__community_cards[i] is None:
                        self.__community_cards[i] = self.__deck.pop()
                self.__hand_values = self.calculate_hand_value()
                print(f"> Community cards: {self.__community_cards}")

        oth_player = 1 if self.__acting_player == 0 else 0
        # print(self.__sequence)

        # if someone is betting, we are going to increase its bet amount
        if action == TexasAction.CALL:
            self.__bets[self.__acting_player] = self.__bets[oth_player]
        if action == TexasAction.RAISE:
            self.__bets[self.__acting_player] = self.__bets[oth_player] + 1

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    # DISPLAY
    def display(self):
        print(f": Pot = {self.get_pot()}")
        print(f": Bets = {self.get_bets()}\n")

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
        for i in range(0, len(self.__hands)):
            cloned.__hands[i] = self.__hands[i]
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
                # print(pot)
                return 1 * pot
            elif player_hand_value == opponent_hand_value:
                # print(pot)
                return 1 * (pot / 2)
            elif player_hand_value < opponent_hand_value:
                return -1 * pot
            # return (1 if player_hand_value > opponent_hand_value else -1) * pot
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

    # CONVERTER E CALCULAR HANDS
    def parse_hands(self) -> List[List[TexasCard]]:
        # hand cards
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
            # print(f"parsed_hand {i}: {parsed_hand}")
            if parsed_hand not in parsed_hands:
                parsed_hands.append(parsed_hand)
        self.__parsed_hands_no_comm = parsed_hands
        self.__parsed_hands = parsed_hands
        # print(f"parsed_hands: {self.__parsed_hands}")
        # community cards
        parsed_community_cards = []
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
        self.__parsed_hands[0] += parsed_community_cards
        self.__parsed_hands[1] += parsed_community_cards
        return self.__parsed_hands

    def calculate_hand_value(self):
        self.parse_hands()
        hand_values = []
        for hand in self.__parsed_hands:
            hand_values.append(10 if TexasEvaluator.is_royal_flush(hand) else
                               9 if TexasEvaluator.is_straight_flush(hand) else
                               8 if TexasEvaluator.is_four_of_a_kind(hand) else
                               7 if TexasEvaluator.is_full_house(hand) else
                               6 if TexasEvaluator.is_flush(hand) else
                               5 if TexasEvaluator.is_straight(hand) else
                               4 if TexasEvaluator.is_three_of_a_kind(hand) else
                               3 if TexasEvaluator.is_two_pair(hand) else
                               2 if TexasEvaluator.is_pair(hand) else
                               1)
        # se ambos tiverem o mesmo valor será tida em conta a carta com rank mais alto
        # quem tem a carta mais alta ganha, se nenhum tiver uma carta mais alta é dividido o pot pelos 2
        if len(set(hand_values)) == 1:
            max_card_ranks = [max(hand[:2], key=lambda c: c.rank.value).rank.value for hand in self.__parsed_hands]
            max_rank = max(max_card_ranks)
            for i, rank in enumerate(max_card_ranks):
                if rank == max_rank:
                    hand_values[i] += 0.1
        # print(hand_values)
        return hand_values
