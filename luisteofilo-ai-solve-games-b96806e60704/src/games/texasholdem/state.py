from games.texasholdem.action import TexasAction
from games.texasholdem.card import TexasCard
from games.state import State


class TexasState(State):

    def __init__(self):
        super().__init__()
        """
        the sequence of plays
        """
        self.__sequence = []
        """
        the acting player index
        """
        self.__acting_player = 0
        """
        indicates if the game is finished
        """
        self.__is_finished = False
        """
        the cards that were seen so far
        """
        self.__cards = [None, None, None, None, None]
        """
        the current round of betting
        """
        self.__round = 0
        """
        the best that were done so far
        in this version of Poker, each player bet $1 each before starting the game
        """
        self.__bets = [0, 0]
        """
        the amount of chips each player has remaining
        """
        self.__chips = [100, 100]
        """
        indicates if the game is in showdown (actions are finished and players are about to reveal the cards)
        """
        self.__is_showdown = False

    @staticmethod
    def get_num_players():
        return 2

    def get_current_betting_round(self):
        return self.__round

    def validate_action(self, action) -> bool:
        return not self.__is_finished and action is not None

    def update(self, action):
        # handle blind and big blind actions
        if self.__sequence == []:  # first action
            self.__bets[0] = 1  # player 0 posts small blind
            self.__bets[1] = 2  # player 1 posts big blind
            self.__acting_player = 0  # first player to act after blinds
            self.__sequence.append(TexasAction.BLIND)
            self.__sequence.append(TexasAction.BIG_BLIND)
        else:
            last_action = self.__sequence[-1]

            # handle rest of the actions
            if last_action == TexasAction.BET or last_action == TexasAction.RAISE:
                self.__is_finished = True
                if action == TexasAction.FOLD:
                    self.__sequence.append(action)
                elif action == TexasAction.CALL:
                    self.__sequence.append(action)
                else:
                    self.__is_showdown = True
                    self.__sequence.append(action)
            elif last_action == TexasAction.CHECK:
                if action == TexasAction.CHECK:
                    self.__sequence.append(action)
                elif action == TexasAction.BET:
                    self.__bets[self.__acting_player] += 1
                    self.__sequence.append(action)
                else:
                    self.__is_finished = True
                    self.__is_showdown = True
                    self.__sequence.append(action)
            elif last_action == TexasAction.CALL:
                if action == TexasAction.CHECK:
                    self.__sequence.append(action)
                elif action == TexasAction.BET:
                    self.__bets[self.__acting_player] += 1
                    self.__is_finished = True
                    self.__is_showdown = True
                    self.__sequence.append(action)
                else:
                    self.__is_finished = True
                    self.__is_showdown = True
                    self.__sequence.append(action)
            elif last_action == TexasAction.FOLD:
                self.__is_finished = True
                self.__is_showdown = True
                self.__sequence.append(action)

        # if someone is betting, we are going to increase their bet amount
        if action == TexasAction.BET or action == TexasAction.RAISE:
            self.__bets[self.__acting_player] += 1

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    def display(self):
        for action in self.__sequence:
            if action == TexasAction.BET:
                print('b', end="")
            elif action == TexasAction.FOLD:
                print('f', end="")
            elif action == TexasAction.CALL:
                print('c', end="")
            elif action == TexasAction.RAISE:
                print('r', end="")
            else:
                print('p', end="")
        print(f": pot = {self.get_pot()}")

    """
    get the total amount that was put into bets so far
    """

    def get_pot(self):
        return sum(self.__bets)

    def is_finished(self) -> bool:
        return self.__is_finished

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned = TexasState()
        cloned.__bets = self.__bets.copy()
        cloned.__sequence = self.__sequence.copy()
        cloned.__is_finished = self.__is_finished
        cloned.__acting_player = self.__acting_player
        for i in range(0, len(self.__cards)):
            cloned.__cards[i] = self.__cards[i]
        cloned.__is_showdown = self.__is_showdown
        cloned.__round = self.__round
        return cloned

    def get_result(self, pos):
        # no result if the game is not finished
        if not self.__is_finished:
            return None

        # if we are finished and we have a showdown, the cards must be available
        if self.__is_showdown:
            for card in self.__cards:
                if card is None:
                    return None

        pot = self.get_pot()
        opp_pos = 1 if pos == 0 else 0

        if self.__is_showdown:
            # noinspection PyTypeChecker
            # if there is a showdown, we will give 1 or 2 to the player with the best card and -1 or -2 to the looser
            return (1 if self.__cards[pos] > self.__cards[opp_pos] else -1) * (pot / 2)
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            return 1 if self.__bets[pos] > self.__bets[opp_pos] else -1

    def before_results(self):
        pass

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence
