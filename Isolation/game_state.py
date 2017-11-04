ROWS = 2
COLUMNS = 3


class GameState:
    def __init__(self):
        """At a minimum, the board state needs to keep track
        of which cells are open and closed; which player has
        initiative (whose turn it is to move); and where each player
        is on the board.
        (Note: Remember to block off the lower right corner when you create a new board!)
        """
        # represent the board as a list of length 9 = r*c
        self.open_cells = [x for x in range((ROWS * COLUMNS) - 1)]
        self.closed_cells = [(ROWS * COLUMNS) - 1]
        self.player_turn = 1
        self.player_positions = []
        pass

    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        pass

    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        pass