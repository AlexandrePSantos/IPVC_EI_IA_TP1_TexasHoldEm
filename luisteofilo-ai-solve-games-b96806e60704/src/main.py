from games.game_simulator import GameSimulator

"""
from games.connect4.players.greedy import GreedyConnect4Player
from games.connect4.players.minimax import MinimaxConnect4Player
from games.connect4.players.random import RandomConnect4Player
from games.connect4.simulator import Connect4Simulator
"""
"""
from games.poker.players.always_bet import AlwaysBetKuhnPokerPlayer
from games.poker.players.always_bet_king import AlwaysBetKingKuhnPokerPlayer
from games.poker.players.always_pass import AlwaysPassKuhnPokerPlayer
from games.poker.players.cfr import CFRKuhnPokerPlayer
from games.poker.players.random import RandomKuhnPokerPlayer
from games.poker.simulator import KuhnPokerSimulator
"""
"""
from games.tictactoe.players.human import HumanTicTacToePlayer
from games.tictactoe.players.random import RandomTicTacToePlayer
from games.tictactoe.players.greedy import GreedyTicTacToePlayerOffensive
from games.tictactoe.players.greedy import GreedyTicTacToePlayerDefensive
from games.tictactoe.players.minimax import MinimaxTicTacToePlayer
from games.tictactoe.simulator import TicTacToeSimulator
"""
"""
from games.texasholdem.players.always_bet import AlwaysBetKuhnPokerPlayer
from games.texasholdem.players.always_bet_king import AlwaysBetKingKuhnPokerPlayer
from games.texasholdem.players.always_pass import AlwaysPassKuhnPokerPlayer
from games.texasholdem.players.cfr import CFRKuhnPokerPlayer
from games.texasholdem.players.random import RandomKuhnPokerPlayer
from games.texasholdem.simulator import KuhnPokerSimulator
"""


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 1000

    """
    PLAYERS_AND_DIFFICULTIES
    """
    # --Connect4--
    """    
    c4_simulations = [
        # uncomment to play as human
        # {
        #    "name": "Connect4 - Human VS Random",
        #    "player1": HumanConnect4Player("Human"),
        #    "player2": RandomConnect4Player("Random")
        # },
        {
            "name": "Connect4 - Random VS Random",
            "player1": RandomConnect4Player("Random 1"),
            "player2": RandomConnect4Player("Random 2")
        },
        {
            "name": "Connect4 - Greedy VS Random",
            "player1": GreedyConnect4Player("Greedy"),
            "player2": RandomConnect4Player("Random")
        },
        {
            "name": "Minimax VS Random",
            "player1": MinimaxConnect4Player("Minimax"),
            "player2": RandomConnect4Player("Random")
        },
        {
            "name": "Minimax VS Greedy",
            "player1": MinimaxConnect4Player("Minimax"),
            "player2": GreedyConnect4Player("Greedy")
        }
    ]
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

    # --TicTacToe--
    """
    tictac_simulations = [
        {
            "name": "TicTacToe - Human VS Human",
            "player1": HumanTicTacToePlayer("Human"),
            "player2": HumanTicTacToePlayer("Human")
        },
        {
            "name": "TicTacToe - Human VS Random",
            "player1": HumanTicTacToePlayer("Human"),
            "player2": RandomTicTacToePlayer("Random")
        },
        {
            "name": "TicTacToe - Human VS Greedy",
            "player1": HumanTicTacToePlayer("Human"),
            "player2": GreedyTicTacToePlayer("Greedy")
        },
        {
            "name": "TicTacToe - Human VS Minimax",
            "player1": HumanTicTacToePlayer("Human"),
            "player2": MinimaxTicTacToePlayer("Minimax")
        },
        {
            "name": "TicTacToe - Random VS Random",
            "player1": RandomTicTacToePlayer("Random 1"),
            "player2": RandomTicTacToePlayer("Random 2")
        },
        {
            "name": "TicTacToe - Greedy VS Random",
            "player1": GreedyTicTacToePlayerOffensive("Greedy"),
            "player2": RandomTicTacToePlayer("Random")
        },
        {
            "name": "TicTacToe - Greedy VS Random",
            "player1": GreedyTicTacToePlayerDefensive("Greedy"),
            "player2": RandomTicTacToePlayer("Random")
        },
        {
            "name": "TicTacToe - Greedy VS Greedy",
            "player1": GreedyTicTacToePlayerOffensive("Greedy"),
            "player2": GreedyTicTacToePlayerDefensive("Greedy")
        }
        {
            "name": "TicTacToe - Minimax VS Random",
            "player1": MinimaxTicTacToePlayer("Minimax"),
            "player2": RandomTicTacToePlayer("Random")
        },
        {
            "name": "TicTacToe - Minimax VS Minimax",
            "player1": MinimaxTicTacToePlayer("Minimax"),
            "player2": MinimaxTicTacToePlayer("Minimax")
        },
        {
            "name": "TicTacToe - Minimax VS Greedy",
            "player1": MinimaxTicTacToePlayer("Minimax"),
            "player2": GreedyTicTacToePlayer("Greedy")
        }
    ]
    """

    # --TexasHoldEm--
    """
    tex_simulations = [
        {
            "name": "Texas HoldEm - Human VS Human",
            "player1": HumanTicTacToePlayer("Human"),
            "player2": HumanTicTacToePlayer("Human")
        }
    ]
    """

    """
    SIMULATIONS
    """
    # --Connect4--
    """ 
    for sim in c4_simulations:
        run_simulation(sim["name"], Connect4Simulator(sim["player1"], sim["player2"]), num_iterations)
    """
    # --KhunPoker--
    """
    for sim in poker_simulations:
        run_simulation(sim["name"], KuhnPokerSimulator(sim["player1"], sim["player2"]), num_iterations)
    """
    # --TicTacToe--
    """    
    for sim in tictac_simulations:
        run_simulation(sim["name"], TicTacToeSimulator(sim["player1"], sim["player2"]), num_iterations)
    """
    # --TexasHoldEm--
    """    
    for sim in tex_simulations:
        run_simulation(sim["name"], TexasHoldEmSimulator(sim["player1"], sim["player2"]), num_iterations)
    """


if __name__ == "__main__":
    main()
