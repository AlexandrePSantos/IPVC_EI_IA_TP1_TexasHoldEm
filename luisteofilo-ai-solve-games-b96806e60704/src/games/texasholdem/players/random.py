from random import choice

from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State


class RandomTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TexasState):
        print(f"\n> Player {self.get_current_pos() + 1} with hand {self.get_current_hand()}")
        state.display()
        return choice([TexasAction.CALL, TexasAction.RAISE, TexasAction.PASS])

    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
