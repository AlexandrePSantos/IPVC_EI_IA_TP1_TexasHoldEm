from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State
from random import random


class CFREasyTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.__trainer = TexasTrainer()
        self.__trainer.train(100000)

    def get_action(self, state: TexasState):
        info_set = f"{self.get_current_card()}"
        for action in state.get_sequence():
            if action == TexasAction.PASS:
                info_set += 'p'
            else:
                info_set += 'b'
        prob = self.__trainer.get_avg_strategy(info_set)[0]

        return TexasAction.PASS if random() <= prob else TexasAction.BET

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass