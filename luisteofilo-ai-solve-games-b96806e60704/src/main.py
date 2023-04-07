from games.game_simulator import GameSimulator


from games.poker.players.always_bet import AlwaysBetKuhnPokerPlayer
from games.poker.players.always_bet_king import AlwaysBetKingKuhnPokerPlayer
from games.poker.players.always_pass import AlwaysPassKuhnPokerPlayer
from games.poker.players.cfr import CFRKuhnPokerPlayer
from games.poker.players.random import RandomKuhnPokerPlayer
from games.poker.simulator import KuhnPokerSimulator

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
    # --KhunPoker--
    """
    poker_simulations = [
        # uncomment to play as human
        # {
        #    "name": "Connect4 - Human VS Random",
        #    "player1": HumanKuhnPokerPlayer("Human"),
        #    "player2": RandomKuhnPokerPlayer("Random")
        # },
        {
            "name": "Kuhn Poker - Random VS Random",
            "player1": RandomKuhnPokerPlayer("Random 1"),
            "player2": RandomKuhnPokerPlayer("Random 2")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS Random",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - AlwaysPass VS Random",
            "player1": AlwaysPassKuhnPokerPlayer("AlwaysPass"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS AlwaysPass",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS AlwaysBetKing",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
        },
        {
            "name": "Kuhn Poker - CFR VS Random",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysPass",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysBet",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysBetKuhnPokerPlayer("AlwaysBet")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysBetKing",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
        }
    ]
    """

    # --TexasHoldEm--
    tex_simulations = [
        {
            "name": "Texas HoldEm - Human VS Human",
            "player1": HumanTexasPlayer("Human"),
            "player2": HumanTexasPlayer("Human")
        }
    ]

    """
    SIMULATIONS
    """
    # --KhunPoker--
    """
    for sim in poker_simulations:
        run_simulation(sim["name"], KuhnPokerSimulator(sim["player1"], sim["player2"]), num_iterations)
    """
    # --TexasHoldEm--
    for sim in tex_simulations:
        run_simulation(sim["name"], TexasSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
