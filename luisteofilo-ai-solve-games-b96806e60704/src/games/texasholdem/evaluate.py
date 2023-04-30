from typing import List

from games.texasholdem.card import Rank, Suit, TexasCard


class TexasEvaluator:
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
