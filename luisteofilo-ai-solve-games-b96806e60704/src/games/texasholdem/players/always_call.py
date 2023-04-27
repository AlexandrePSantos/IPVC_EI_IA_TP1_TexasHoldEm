from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State


class AlwaysCallTexasHoldEmPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TexasState):
        return TexasAction.CALL

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
