from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State
from random import random


class CFRHardTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.__trainer = TexasTrainer()
        self.__trainer.train(100000)

    def get_action(self, state: TexasState):
        info_set = f"{self.get_current_card()}"
        for action in state.get_sequence():
            if action == TexasAction.PASS:
                info_set += 'p'
            elif action == TexasAction.CALL:
                info_set += 'c'
            elif action == TexasAction.RAISE:
                info_set += 'r'
        prob = self.__trainer.get_avg_strategy(info_set)[0]

        # Verificar esta parte para adicionar o RAISE
        return TexasAction.PASS if random() <= prob else TexasAction.CALL

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass