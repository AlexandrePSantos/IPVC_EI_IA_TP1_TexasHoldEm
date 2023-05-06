import random

from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State


class GreedyTrainedTexasPlayer(TexasPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.file_path = "\luisteofilo-ai-solve-games-b96806e60704\src\games\texasholdem\greedy_training"
        self.Q_table = {}
        self.epsilon = 0.1
        self.load_q_table()

    def get_action(self, state: TexasState):
        state_key = state.get_state_key(self.get_current_pos())

        # Choose action with highest Q-value
        if state_key in self.Q_table and random.random() > self.epsilon:
            action = max(self.Q_table[state_key], key=self.Q_table[state_key].get)
        else:
            action = random.choice(state.get_legal_actions(self.get_current_pos()))

        return action

    def event_action(self, pos: int, action, new_state: State):
        # Update Q-table based on new state
        old_state_key = new_state.get_previous_state_key(pos)
        new_state_key = new_state.get_state_key(pos)
        reward = new_state.get_reward(pos)
        alpha = 0.5
        gamma = 0.9
        if old_state_key in self.Q_table and new_state_key in self.Q_table[old_state_key]:
            max_q = max(self.Q_table[new_state_key].values())
            self.Q_table[old_state_key][action] += alpha * (reward + gamma * max_q - self.Q_table[old_state_key][action])

        self.save_q_table()

    def event_end_game(self, final_state: State):
        # ignore
        pass

    def load_q_table(self):
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    state, action, value = line.strip().split(',')
                    if state not in self.Q_table:
                        self.Q_table[state] = {}
                    self.Q_table[state][int(action)] = float(value)
        except FileNotFoundError:
            print(f"No Q-table file found at {self.file_path}, creating a new file")

    def save_q_table(self):
        with open(self.file_path, 'w') as f:
            for state, values in self.Q_table.items():
                for action, value in values.items():
                    f.write(f"{state},{action},{value}\n")
