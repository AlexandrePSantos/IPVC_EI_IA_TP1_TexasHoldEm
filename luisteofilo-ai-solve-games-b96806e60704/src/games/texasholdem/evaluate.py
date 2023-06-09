from typing import List

from games.texasholdem.card import Rank, Suit, TexasCard


class TexasEvaluator:
    # RANKINGS
    @staticmethod
    def is_royal_flush(cards: List[TexasCard]) -> bool:
        suits = set(card.suit for card in cards)
        if len(suits) == 1:
            ranks = set(card.rank for card in cards)
            if ranks == {Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE}:
                return True
        return False

    @staticmethod
    def is_straight_flush(cards: List[TexasCard]) -> bool:
        # First check if there is a flush
        if not TexasEvaluator.is_flush(cards):
            return False

        # Sort the cards by rank
        cards.sort(key=lambda c: c.rank.value, reverse=True)

        # Check for a straight within the flush
        for i in range(4):
            if cards[i].rank.value != cards[i + 1].rank.value + 1:
                return False

        # If we get here, we have a straight flush
        return True

    @staticmethod
    def is_four_of_a_kind(cards: List[TexasCard]) -> bool:
        ranks = [card.rank for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 4:
                return True
        return False

    @staticmethod
    def is_full_house(cards: List[TexasCard]) -> bool:
        # First check if there is a three of a kind
        if not TexasEvaluator.is_three_of_a_kind(cards):
            return False

        # Check if there is a pair among the remaining two cards
        ranks = [card.rank for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 2:
                return True
        return False

    @staticmethod
    def is_flush(cards: List[TexasCard]) -> bool:
        suits = set(card.suit for card in cards)
        if len(suits) == 1:
            return True
        return False

    @staticmethod
    def is_straight(cards: List[TexasCard]) -> bool:
        # Make a list of the card rank values
        ranks = sorted(card.rank.value for card in cards)
        # Check if there are 5 different ranks and the difference between the highest and lowest rank is 4
        return len(set(ranks)) == 5 and ranks[-1] - ranks[0] == 4

    @staticmethod
    def is_three_of_a_kind(cards: List[TexasCard]) -> bool:
        ranks = [card.rank.value for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 3:
                return True
        return False

    @staticmethod
    def is_two_pair(cards: List[TexasCard]) -> bool:
        ranks = sorted(card.rank.value for card in cards)
        pairs = 0
        for i in range(len(ranks) - 1):
            if ranks[i] == ranks[i + 1]:
                pairs += 1
        return pairs == 2

    @staticmethod
    def is_pair(cards: List[TexasCard]) -> bool:
        ranks = [card.rank for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 2:
                return True
        return False

    # CALCULAR HAND VALUES (BOTH PLAYERS)
    @staticmethod
    def calculate_hand_value(cards):
        __combined_cards = cards
        hand_values = []
        for hand in __combined_cards:
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
        if len(set(hand_values)) == 1:
            max_card_ranks = [max(hand[:2], key=lambda c: c.rank.value).rank.value for hand in __combined_cards]
            max_rank = max(max_card_ranks)
            for i, rank in enumerate(max_card_ranks):
                if rank == max_rank:
                    hand_values[i] += 0.1
        return hand_values

    @staticmethod
    def single_hand_value(cards):
        hand = cards
        if TexasEvaluator.is_royal_flush(hand):
            value = 10
        elif TexasEvaluator.is_straight_flush(hand):
            value = 9
        elif TexasEvaluator.is_four_of_a_kind(hand):
            value = 8
        elif TexasEvaluator.is_full_house(hand):
            value = 7
        elif TexasEvaluator.is_flush(hand):
            value = 6
        elif TexasEvaluator.is_straight(hand):
            value = 5
        elif TexasEvaluator.is_three_of_a_kind(hand):
            value = 4
        elif TexasEvaluator.is_two_pair(hand):
            value = 3
        elif TexasEvaluator.is_pair(hand):
            value = 2
        else:
            value = 1
        return value
