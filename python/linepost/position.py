"""Position and Move are the nodes and edges of the repertoire graph.
"""

import chess

from typing import List, Optional


class Game:
    """The repertoire graph.

    Attributes:
        fens: A mapping of FEN strings to Position objects.
    """

    def __init__(self) -> None:
        self.fens = {}

    def get_position(self, board: chess.Board) -> 'Position':
        """Returns the Position corresponding to a given board.

        If the Position has not been seen in this Game, this method will create
        a new Position object and store it in the Game before returning it.

        Args:
            board: The board corresponding to the desired Position.
        Returns:
            The Position for this board.
        """
        fen = board.fen()
        if fen in self.fens:
            return self.fens[fen]
        position = Position(self, board)
        self.fens[fen] = position
        return position


class Position:
    """The board state and all next moves in the repertoire graph.

    Attributes:
        game: The game graph to which this position is tied.
        board: The board state at this position.
        moves: A list of moves from this position.
    """

    def __init__(self, game: Game, board: chess.Board) -> None:
        """Stores the board and creates an empty list of next moves.

        Args:
            game: The game graph to which this position is tied.
            board: The board state at this position.
        """
        self.game = game
        self.board = board
        self.moves = {}

    def make_move(self,
                  move: str,
                  evaluation: Optional[str] = None,
                  remarks: Optional[List[str]] = None) -> 'Position':
        """Adds a move from this position.

        Stores the move on this position, which links to the new Position
        created by this move, and returns that new Position.

        Args:
            move: The algebraic notation of the move.
            evaluation: Commentary on the move (e.g. !, ?).
            remarks: A list of remarks on the move or position.
        Returns:
            The Position holding the new board state.
        Raise:
            ValueError if the move is illegal from this position.
        """
        try:
            next_board = self.board.copy()
            next_board.push_san(move)
            next_position = self.game.get_position(next_board)
            next_move = Move(self, next_position, move, evaluation, remarks)
            if repr(next_move) in self.moves:
                self.moves[repr(next_move)].merge(next_move)
            else:
                self.moves[repr(next_move)] = next_move
            return next_position
        except chess.IllegalMoveError as exc:
            raise ValueError(
                f'Move {move} is illegal from board {self.board.fen()}'
            ) from exc


class Move:
    """The transition from one Position to another.

    Attributes:
        from_position: The Position before this move is made.
        to_position: The Position after this move is made.
        label: The algebraic notation of the move.
        evaluation: Commentary on the move (e.g. !, ?).
        remarks: A set of remarks on the move or position.
    """

    def __init__(self,
                 from_position: Position,
                 to_position: Position,
                 label: str,
                 evaluation: Optional[str] = None,
                 remarks: Optional[List[str]] = None) -> None:
        self.from_position = from_position
        self.to_position = to_position
        self.label = label
        if evaluation is not None:
            self.evaluation = evaluation
        else:
            self.evaluation = ''
        self._key = self._create_key()
        self._s = self._create_str()
        self.remarks = set()
        if remarks:
            self.remarks = self.remarks.union(remarks)

    def _create_key(self) -> str:
        """Creates the hash key corresponding to this move."""
        return '.'.join([
            self.from_position.board.fen(),
            self.to_position.board.fen(), self.label,
            str(self.evaluation)
        ])

    def _create_str(self) -> str:
        """Creates the string representation of this move."""
        return f'{self.label}{self.evaluation}'

    def __repr__(self) -> str:
        return self._key

    def __str__(self) -> str:
        return self._s

    def merge(self, other: 'Move') -> None:
        """Merges the remarks from another Move object.

        Args:
            other: Another Move.
        Raises:
            ValueError if the representations of the two moves differ.
        """
        if repr(self) != repr(other):
            raise ValueError(f'Moves {self} and {other}')

        self.remarks = self.remarks.union(other.remarks)