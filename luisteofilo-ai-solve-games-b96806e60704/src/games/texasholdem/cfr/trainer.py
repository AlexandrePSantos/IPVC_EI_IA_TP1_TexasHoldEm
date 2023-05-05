from random import shuffle
from deuces import Card, Evaluator
from games.texasholdem.card import Rank, Suit, TexasCard

evaluator = Evaluator()


class TexasTrainer:
    PASS = 0
    CALL = 1
    RAISE = 2
    NUM_ACTIONS = 3

    # TODO - DONE
    class Node:
        def __init__(self, info_set):
            self.__info_set = info_set
            self.__regret_sum = [0.0] * TexasTrainer.NUM_ACTIONS
            self.__strategy = [0.0] * TexasTrainer.NUM_ACTIONS
            self.__strategy_sum = [0.0] * TexasTrainer.NUM_ACTIONS

        def get_strategy(self, realization_weight):
            normalizing_sum = 0.0
            for a in range(0, TexasTrainer.NUM_ACTIONS):
                self.__strategy[a] = self.__regret_sum[a] if self.__regret_sum[a] > 0 else 0
                normalizing_sum += self.__strategy[a]

            for a in range(0, TexasTrainer.NUM_ACTIONS):
                if normalizing_sum > 0:
                    self.__strategy[a] /= normalizing_sum
                else:
                    self.__strategy[a] = 1.0 / TexasTrainer.NUM_ACTIONS
                self.__strategy_sum[a] += realization_weight * self.__strategy[a]
            return self.__strategy

        def get_average_strategy(self):
            avg_strategy = [0.0] * TexasTrainer.NUM_ACTIONS
            normalizing_sum = 0.0
            for a in range(0, TexasTrainer.NUM_ACTIONS):
                normalizing_sum += self.__strategy_sum[a]
            for a in range(0, TexasTrainer.NUM_ACTIONS):
                if normalizing_sum > 0:
                    avg_strategy[a] = self.__strategy_sum[a] / normalizing_sum
                else:
                    avg_strategy[a] = 1.0 / TexasTrainer.NUM_ACTIONS
            return avg_strategy

        def add_regret_sum(self, a, val):
            self.__regret_sum[a] += val

        def __str__(self):
            return f"{self.__info_set}: {str(self.get_average_strategy())}"

    def __init__(self):
        self.__node_map = {}

    # TODO - DONE
    def train(self, iterations):
        cards = [TexasCard(rank, suit) for rank in Rank for suit in Suit]
        util = 0.0
        for i in range(0, iterations):
            shuffle(cards)
            util += self.cfr(cards, "", 1.0, 1.0)
        print(f"Average game value: {util/iterations}")
        for n in self.__node_map:
            print(self.__node_map[n])

    # TODO - DOING
    def cfr(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player
        if plays >= 8:
            terminal_pass = history[plays - 1] == 'p'
            terminal_call = history[plays - 1] == 'c'
            double_raise = history[plays-2:plays] == "rr"
            is_player_card_higher = cards[player] > cards[opponent]
            if terminal_pass:
                if history[-2:] == "pp":
                    return 1 if is_player_card_higher else -1
                else:
                    return 1
            elif terminal_call:
                if history[-2:] == "cc":
                    return 1 if is_player_card_higher else -1
                else:
                    return 0
            elif double_raise:
                return 2 if is_player_card_higher else -2

        info_set = f"{cards[player]}{history}"
        node = self.__node_map.get(info_set)
        if node is None:
            node = TexasTrainer.Node(info_set)
            self.__node_map[info_set] = node

        strategy = node.get_strategy(p0 if player == 0 else p1)
        util = [0.0] * TexasTrainer.NUM_ACTIONS
        node_util = 0.0

        for a in range(0, TexasTrainer.NUM_ACTIONS):
            next_history = f"{history}{'p' if a == 0 else 'b'}"
            util[a] = - self.cfr(cards, next_history, p0 * strategy[a], p1) if player == 0 else - self.cfr(cards, next_history, p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]

        for a in range(0, TexasTrainer.NUM_ACTIONS):
            regret = util[a] - node_util
            node.add_regret_sum(a, (p1 if player == 0 else p0) * regret)

        return node_util

    # TODO - DONE
    def get_avg_strategy(self, info_set):
        node = self.__node_map.get(info_set)
        return node.get_average_strategy()
