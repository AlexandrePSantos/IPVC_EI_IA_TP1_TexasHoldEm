from games.game_simulator import GameSimulator

from games.texasholdem.players.human import HumanTexasPlayer
from games.texasholdem.players.random import RandomTexasPlayer
from games.texasholdem.players.always_bet import AlwaysBetTexasHoldEmPlayer
from games.texasholdem.players.always_pass import AlwaysPassTexasHoldEmPlayer
from games.texasholdem.players.algoeasy import AlgoEasy
from games.texasholdem.players.algohard import AlgoHard
from games.texasholdem.simulator import TexasSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(iterations):
        print(f"Iteration {i + 1}")
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def player_type():
    print("1 - Human")
    print("2 - Always Bet")
    print("3 - Always Pass")
    print("4 - Random")
    print("5 - MonteCarlo Low Difficulty")
    print("6 - MonteCarlo High Difficulty")


def main():
    player1, player2, name1, name2 = 0, 0, "", ""
    print("ESTG IA Games Simulator")

    """
    ITERATIONS
    """
    num_iterations = int(input("Number of iterations: "))

    """
    PLAYERS / DIFFICULTIES 
    """
    player_type()
    p1 = int(input("Insert the type for player 1: "))
    if p1 == 1:
        player1, name1 = HumanTexasPlayer, "Human"
    elif p1 == 2:
        player1, name1 = AlwaysBetTexasHoldEmPlayer, "Always Bet"
    elif p1 == 3:
        player1, name1 = AlwaysPassTexasHoldEmPlayer, "Always Pass"
    elif p1 == 4:
        player1, name1 = RandomTexasPlayer, "Random"

    p2 = int(input("Insert the type for player 2: "))
    if p2 == 1:
        player2 = HumanTexasPlayer
        name2 = "Human"
    elif p2 == 2:
        player2 = AlwaysBetTexasHoldEmPlayer
        name2 = "Always Bet"
    elif p2 == 3:
        player2 = AlwaysPassTexasHoldEmPlayer
        name2 = "Always Pass"
    elif p2 == 4:
        player2 = RandomTexasPlayer
        name2 = "Random"

    """
    SIMULATIONS
    """
    tex_simulations = [
        {
            "name": "Texas Hold'Em",
            "player1": player1(name1 + " 1"),
            "player2": player2(name2 + " 2")
        }]

    for sim in tex_simulations:
        run_simulation(sim["name"], TexasSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
