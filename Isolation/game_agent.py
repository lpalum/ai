"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


"""
Evaluation functions are going to be created as a weighted combination of
features that are dependent on the position of the players and the state 
of the game.
f1 - player open moves (changes based on the state of the game)
f2 - opponent open moves (changes based on the state of the game)
f3 - players manhattan distance to the center of the board (changes based on players position)
f4 - opponents manhattan distance to the center of the board (changes based on opponents position)
f5 - players manhattan distance from the opponent

"""

"""Calculate the heuristic value of a game state from the point of view
of the given player.


Note: this function should be called from within a Player instance as
`self.score()` -- you should not need to call this function directly.

Parameters
----------
game : `isolation.Board`
    An instance of `isolation.Board` encoding the current state of the
    game (e.g., player locations and blocked cells).

player : object
    A player instance in the current game (i.e., an object corresponding to
    one of the player objects `game.__player_1__` or `game.__player_2__`.)

Returns
-------
float
    The heuristic value of the current game state to the specified player.
"""
# Precompute dictionaries for distance to center, difference in open moves and abs calculations
rows_cols = [0, 1, 2, 3, 4, 5, 6]
the_abs = {-6: 6, -5: 5, -4: 4, -3: 3, -2: 2, -1: 1, 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
dist2center= { r:{c:abs(3-r)+abs(3-c) for c in rows_cols} for r in rows_cols }
open_move_diff = {i: {j: i - 2 * j for j in range(50)} for i in range(50)}
inv_dist2center = {r: {c: 1 / (1 + (abs(3 - r) + abs(3 - c))) for c in rows_cols} for r in rows_cols}
inv_dist2opp = {
r: {c: 1 / (r + c) if r != 0 and c != 0 else 1 / c if c != 0  else 1 / r if r != 0 else 1 for c in rows_cols} for r in
rows_cols}

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # my distance to the opponent (closer is better - keep your enemies closer)
    my, mx = game.get_player_location(player)
    oy, ox = game.get_player_location(game.get_opponent(player))
    return float(inv_dist2opp[the_abs[my - oy]][the_abs[mx - ox]])

def custom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Difference between my opponents distance to the center and my distance
    myr, myc = game.get_player_location(player)
    opr, opc = game.get_player_location(game.get_opponent(player))
    return float(dist2center[opr][opc] - dist2center[myr][myc])

def custom_score_3(game,player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my, mx = game.get_player_location(player)
    oy, ox = game.get_player_location(game.get_opponent(player))
    mom = len(game.get_legal_moves(player))
    oom = len(game.get_legal_moves(game.get_opponent(player)))

    # push opponent away from center and away from me while I have more open moves
    return float(mom - oom + dist2center[oy][ox] - dist2center[my][mx] + (the_abs[my - oy] + the_abs[mx - ox]))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def _terminal_test(game):
            """ Return True if the game is over for the active player
            and False otherwise.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # No more moves? We are finished with the game.
            if len(game.get_legal_moves()) == 0:
                return True
            else:
                return False

        # best outcome of player 2 (min) given the actions of player 1 (max)
        def _min_value(game, d):
            """ Return the value/score for a win if the game is over
            or reached the appropriate depth in the tree,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if _terminal_test(game) or d == 0:
                return self.score(game, self)

            v = float("inf")
            moves = game.get_legal_moves()
            for m in moves:
                v = min(v, _max_value(game.forecast_move(m), d - 1))
            return v

        # best outcome of player 1 (max) given the actions of player 2 (min)
        def _max_value(game, d):
            """ Return the value for a loss (-1) if the game is over
            or reached the appropriate depth in the tree,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if _terminal_test(game) or d == 0:
                return self.score(game, self)

            v = float("-inf")
            moves = game.get_legal_moves()
            for m in moves:
                v = max(v, _min_value(game.forecast_move(m), d - 1))
            return v

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # For this game governed by the depth limited minimax player strategy
        # Iterate through the legal moves maximizing player 1 (max) return
        # assume that player 1 is "on the board" when the game starts and it is
        # player 2s (min) turn.
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        return max(legal_moves, key=lambda m: _min_value(game.forecast_move(m), depth - 1))


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer expires.
            # Start with a depth of 1 and interatively increase the depth
            # until the timeout occurs and then return the best move
            # found up until that point.
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            # Handle any actions required after timeout as needed
            #print("Active: {} Depth Reached: {} Open Moves: {} Best Move {}".format(game.active_player,depth,len(game.get_legal_moves()),best_move))
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def _terminal_test(game):
            """ Return True if the game is over for the active player
            and False otherwise.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # No more moves, we are finished with the game.
            if len(game.get_legal_moves()) == 0:
                return True
            else:
                return False

        # best outcome of player 2 (min) given the actions of player 1 (max)
        def _min_value(game, d, alpha, beta):
            """ Return the value/score for a win if the game is over
            or reached the appropriate depth in the tree,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if _terminal_test(game) or d == 0:
                return self.score(game, self)

            v = float("inf")
            moves = game.get_legal_moves()
            for m in moves:
                v = min(v, _max_value(game.forecast_move(m), d - 1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # best outcome of player 1 (max) given the actions of player 2 (min)
        def _max_value(game, d, alpha, beta):
            """ Return the value/score for a loss if the game is over
            or reached the appropriate depth in the tree,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if _terminal_test(game) or d == 0:
                return self.score(game, self)

            v = float("-inf")
            moves = game.get_legal_moves()
            for m in moves:
                v = max(v, _min_value(game.forecast_move(m), d - 1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        # begin a depth limited a-b pruning game search with the best score initialized to
        # the first element of the legal moves.
        # best_score (alpha) for player 1 maximizer is intialized to -inf
        # beta is initialized to +inf at the start of the game.

        best_move = legal_moves[0]
        best_score = float("-inf")
        # interate through the legal moves starting with player 2 minimizer.  Player 1 is already
        # on the board.  We are starting at ply 1 hence the reduction in depth of 1
        for m in legal_moves:
            the_score = _min_value(game.forecast_move(m), depth - 1, best_score, beta)
            # Keep the best score and move as we iterate through the possible moves.
            if the_score > best_score:
                best_score = the_score
                best_move = m
        return best_move
