from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State


class HumanTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TexasState):
        print(f"\n> Player {self.get_current_pos() + 1} with hand {self.get_current_hand()}")
        state.display()
        return {
            "c": TexasAction.CALL,
            "call": TexasAction.CALL,
            "r": TexasAction.RAISE,
            "raise": TexasAction.RAISE,
            "p": TexasAction.PASS,
            "pass": TexasAction.PASS
        }.get(input("Choose an action (pass/p _ call/c _ r/raise): "))

    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        print(f"> player {pos} got ${result}")
