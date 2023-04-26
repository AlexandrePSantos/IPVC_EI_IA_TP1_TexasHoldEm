from games.game_simulator import GameSimulator

from games.texasholdem.players.human import HumanTexasPlayer
from games.texasholdem.players.random import RandomTexasPlayer
from games.texasholdem.players.always_bet import AlwaysBetTexasHoldEmPlayer
from games.texasholdem.players.always_pass import AlwaysPassTexasHoldEmPlayer
from games.texasholdem.simulator import TexasSimulator

from games.poker.players.random import RandomKuhnPokerPlayer
from games.poker.simulator import KuhnPokerSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(iterations):
        simulator.change_player_positions()
        simulator.run_simulation()
        # print(f"Iteration {i + 1}: Completed")

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 10

    """
    PLAYERS_AND_DIFFICULTIES
    """
    poker_simulations = [
        {
            "name": "Kuhn Poker - Random VS Random",
            "player1": RandomKuhnPokerPlayer("Random 1"),
            "player2": RandomKuhnPokerPlayer("Random 2")
        }
    ]
    # --TexasHoldEm--
    tex_simulations = [
        # {
        #     "name": "Texas HoldEm - Human VS Human",
        #     "player1": HumanTexasPlayer("Human"),
        #     "player2": HumanTexasPlayer("Human")
        # }
        # {
        #     "name": "Texas HoldEm - Human VS Random",
        #     "player1": HumanTexasPlayer("Human"),
        #     "player2": RandomTexasPlayer("Random")
        # }
        {
            "name": "Texas HoldEm - Random VS Random",
            "player1": RandomTexasPlayer("Random1"),
            "player2": RandomTexasPlayer("Random2")
        }
    ]

    """
    SIMULATIONS
    """
    # for sim in poker_simulations:
    #     run_simulation(sim["name"], KuhnPokerSimulator(sim["player1"], sim["player2"]), num_iterations)

    # --TexasHoldEm--
    for sim in tex_simulations:
        run_simulation(sim["name"], TexasSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
