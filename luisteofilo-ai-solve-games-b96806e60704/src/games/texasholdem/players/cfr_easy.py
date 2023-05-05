from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.texasholdem.cfr.trainer import TexasTrainer
from games.state import State
from random import random


class CFREasyTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.__trainer = TexasTrainer()
        self.__trainer.train(1000)

    def get_action(self, state: TexasState):
        print(f"\n> Player {self.get_current_pos() + 1} with hand {self.get_current_hand()}")
        state.display()
        cards = []
        if len(state.get_combined_cards()) > 0:
            if self.get_current_pos() == 0:
                cards = state.get_combined_cards0()
            elif self.get_current_pos() == 1:
                cards = state.get_combined_cards1()
        info_set = f"{cards}"
        for action in state.get_sequence():
            if action == TexasAction.PASS:
                info_set += 'p'
            elif action == TexasAction.CALL:
                info_set += 'c'
            elif action == TexasAction.RAISE:
                info_set += 'r'
        prob = self.__trainer.get_avg_strategy(info_set)[0]

        return TexasAction.PASS if random() <= prob * 0.5 else TexasAction.RAISE if random() <= prob else TexasAction.CALL

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass