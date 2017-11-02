"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_minmax(self):
        # create an isolation board (by default 7x7)
        player1 = game_agent.MinimaxPlayer()
        player2 = game_agent.MinimaxPlayer()
        game = isolation.Board(player1, player2)

        # place player 1 on the board at row 2, column 3, then place player 2 on
        # the board at row 0, column 5; display the resulting board state.  Note
        # that the .apply_move() method changes the calling object in-place.
        game.apply_move((2, 3))
        game.apply_move((0, 5))
        print(game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert (player1 == game.active_player)

        # get a list of the legal moves available to the active player
        print(game.get_legal_moves())

        # get a successor of the current state by making a copy of the board and
        # applying a move. Notice that this does NOT change the calling object
        # (unlike .apply_move()).
        new_game = game.forecast_move((1, 1))
        assert (new_game.to_string() != game.to_string())
        print("\nOld state:\n{}".format(game.to_string()))
        print("\nNew state:\n{}".format(new_game.to_string()))

        # play the remainder of the game automatically -- outcome can be "illegal
        # move", "timeout", or "forfeit"
        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

    def test_alphabeta(self):
        # create an isolation board (by default 7x7)
        player1 = game_agent.AlphaBetaPlayer()
        player2 = game_agent.AlphaBetaPlayer()
        game = isolation.Board(player1, player2)

        # place player 1 on the board at row 2, column 3, then place player 2 on
        # the board at row 0, column 5; display the resulting board state.  Note
        # that the .apply_move() method changes the calling object in-place.
        game.apply_move((2,3))
        game.apply_move((0,5))
        print(game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert (player1 == game.active_player)

        # get a list of the legal moves available to the active player
        print(game.get_legal_moves())

        # get a successor of the current state by making a copy of the board and
        # applying a move. Notice that this does NOT change the calling object
        # (unlike .apply_move()).
        new_game = game.forecast_move((1, 1))
        assert (new_game.to_string() != game.to_string())
        print("\nOld state:\n{}".format(game.to_string()))
        print("\nNew state:\n{}".format(new_game.to_string()))

        # play the remainder of the game automatically -- outcome can be "illegal
        # move", "timeout", or "forfeit"
        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

if __name__ == '__main__':
    unittest.main()
