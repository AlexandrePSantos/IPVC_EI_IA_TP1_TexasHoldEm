from games.game_simulator import GameSimulator

from games.texasholdem.players.human import HumanTexasPlayer
from games.texasholdem.players.random import RandomTexasPlayer
from games.texasholdem.players.always_call import AlwaysCallTexasHoldEmPlayer
from games.texasholdem.players.always_raise import AlwaysRaiseTexasHoldEmPlayer
from games.texasholdem.players.always_pass import AlwaysPassTexasHoldEmPlayer
from games.texasholdem.players.cfr_easy import CFREasyTexasPlayer
from games.texasholdem.players.cfr_hard import CFRHardTexasPlayer
from games.texasholdem.simulator import TexasSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(iterations):
        print(f"Game nº{i + 1}")
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def player_type():
    print("1 - Human")
    print("2 - Always Call")
    print("3 - Always Raise")
    print("4 - Always Pass")
    print("5 - Random")
    print("6 - CFR Easy")
    print("7 - CFR Hard")


def main():
    player1, player2, name1, name2 = 0, 0, "", ""
    print("ESTG IA Games Simulator")

    """ ITERATIONS """
    num_iterations = int(input("Number of iterations: "))

    """ PLAYERS / DIFFICULTIES """
    player_type()
    p1 = int(input("Chose player 1: "))
    if p1 == 1:
        player1, name1 = HumanTexasPlayer, "Human"
    elif p1 == 2:
        player1, name1 = AlwaysCallTexasHoldEmPlayer, "Always Call"
    elif p1 == 3:
        player1, name1 = AlwaysRaiseTexasHoldEmPlayer, "Always Raise"
    elif p1 == 4:
        player1, name1 = AlwaysPassTexasHoldEmPlayer, "Always Pass"
    elif p1 == 5:
        player1, name1 = RandomTexasPlayer, "Random"
    elif p1 == 6:
        player1, name1 = CFREasyTexasPlayer, "CFR Easy"
    elif p1 == 7:
        player1, name1 = CFRHardTexasPlayer, "CFR Hard"

    p2 = int(input("Chose player 2: "))
    if p2 == 1:
        player2, name2 = HumanTexasPlayer, "Human"
    elif p2 == 2:
        player2, name2 = AlwaysCallTexasHoldEmPlayer, "Always Call"
    elif p2 == 3:
        player2, name2 = AlwaysRaiseTexasHoldEmPlayer, "Always Raise"
    elif p2 == 4:
        player2, name2 = AlwaysPassTexasHoldEmPlayer, "Always Pass"
    elif p2 == 5:
        player2, name2 = RandomTexasPlayer, "Random"
    elif p2 == 6:
        player2, name2 = CFREasyTexasPlayer, "CFR Easy"
    elif p2 == 7:
        player2, name2 = CFRHardTexasPlayer, "CFR Hard"

    """ SIMULATIONS """
    tex_simulations = [{"name": "Texas Hold'Em", "player1": player1(name1 + " 1"), "player2": player2(name2 + " 2")}]
    for sim in tex_simulations:
        run_simulation(sim["name"], TexasSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
