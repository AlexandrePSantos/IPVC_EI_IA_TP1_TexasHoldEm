from games.texasholdem.evaluate import TexasEvaluator
from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State

evaluator = TexasEvaluator()


class GreedyBasicTexasPlayer(TexasPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TexasState):
        # print(f"\n> Player {self.get_current_pos() + 1} with hand {self.get_current_hand()}")
        # state.display()
        cards = []
        if len(state.get_combined_cards()) > 0:
            if self.get_current_pos() == 0:
                cards = state.get_combined_cards0()
            elif self.get_current_pos() == 1:
                cards = state.get_combined_cards1()
        value = evaluator.single_hand_value(cards)
        if value <= 1:
            return TexasAction.PASS
        elif 1 < value <= 3:
            return TexasAction.CALL
        elif value > 3:
            return TexasAction.RAISE
        else:
            return TexasAction.RAISE

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
