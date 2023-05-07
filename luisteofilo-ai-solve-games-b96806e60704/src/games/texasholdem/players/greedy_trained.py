from games.texasholdem.action import TexasAction
from games.texasholdem.player import TexasPlayer
from games.texasholdem.state import TexasState
from games.state import State
import random


class GreedyTrainedTexasPlayer(TexasPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.Q_table = {}
        self.visited_states = []
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9

    def get_action(self, state: TexasState):
        state_key = self.get_state_key(state)

        # Choose action with highest Q-value
        if state_key in self.Q_table and random.random() > self.epsilon:
            action = max(self.Q_table[state_key], key=self.Q_table[state_key].get)
        else:
            action = random.choice([TexasAction.PASS, TexasAction.CALL, TexasAction.RAISE])
        self.visited_states.append((state_key, action))
        return action

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # Calculate the final reward
        reward = final_state.get_pot()

        # Iterate over all state-action pairs encountered during the game
        for state_key, action in self.visited_states:
            # Calculate the estimated value of the next state
            next_state_key = self.get_state_key(final_state)
            next_state_value = self.Q_table.get(next_state_key,
                                                {TexasAction.PASS: 0, TexasAction.CALL: 0, TexasAction.RAISE: 0})
            next_state_max_value = max(next_state_value.values())

            # Retrieve the Q-value for the current state-action pair
            q_value = self.Q_table.get(state_key, {TexasAction.PASS: 0, TexasAction.CALL: 0, TexasAction.RAISE: 0})
            old_value = q_value[action]

            # Update the Q-value based on the Bellman equation
            new_value = old_value + self.alpha * (reward + self.gamma * next_state_max_value - old_value)
            q_value[action] = new_value

            # Store the updated Q-value in the Q-table
            self.Q_table[state_key] = q_value

    def get_state_key(self, state: State):
        # Extract relevant features from the state
        player_pos = str(self.get_current_pos())
        community_cards = [card for card in state.get_community_cards() if card is not None]
        community_cards_str = ','.join(map(str, community_cards))

        player_hand = ','.join(map(str, state.get_current_hands()[int(player_pos)]))

        # Combine the features into a string representation of the state
        state_key = f"{player_pos},{community_cards_str},{player_hand}"

        return state_key
