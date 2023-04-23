from games.game_simulator import GameSimulator

from games.texasholdem.players.human import HumanTexasPlayer
from games.texasholdem.players.random import RandomTexasPlayer
from games.texasholdem.simulator import TexasSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 1

    """
    PLAYERS_AND_DIFFICULTIES
    """
    # --TexasHoldEm--
    tex_simulations = [
        # {
        #     "name": "Texas HoldEm - Human VS Human",
        #     "player1": HumanTexasPlayer("Human"),
        #     "player2": HumanTexasPlayer("Human")
        # }
        {
            "name": "Texas HoldEm - Human VS Random",
            "player1": HumanTexasPlayer("Human"),
            "player2": RandomTexasPlayer("Random")
        }
        # {
        #     "name": "Texas HoldEm - Random VS Random",
        #     "player1": RandomTexasPlayer("Random"),
        #     "player2": RandomTexasPlayer("Random")
        # }
    ]

    """
    SIMULATIONS
    """
    # --TexasHoldEm--
    for sim in tex_simulations:
        run_simulation(sim["name"], TexasSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
