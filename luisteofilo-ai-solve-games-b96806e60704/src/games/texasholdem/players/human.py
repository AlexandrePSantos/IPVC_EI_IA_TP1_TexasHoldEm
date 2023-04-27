from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State


class HumanTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TexasState):
        print(f"> You are player human {self.get_current_pos()} with cards {self.get_current_hand()}")
        state.display()
        return {
            "b": TexasAction.BET,
            "bet": TexasAction.BET,
            "p": TexasAction.PASS,
            "pass": TexasAction.PASS
        }.get(input("Choose an action (pass/p or bet/b): "))

    def event_action(self, pos: int, action, new_state: State):
        print(f"> player {pos} {action}")
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        print(f"> player {pos} got ${result}")
