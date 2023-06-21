"""Position and Move are the nodes and edges of the repertoire graph.
"""

import chess

from typing import List, Optional


class Position:
    """The board state and all next moves in the repertoire graph.

    Attributes:
        board: The board state at this position.
        moves: A list of moves from this position.
    """

    def __init__(self, board: chess.Board) -> None:
        """Stores the board and creates an empty list of next moves.

        Args:
            board: The board state at this position.
        """
        self.board = board
        # TODO: Index moves by move or end FEN to enable merging evaluations.
        self.moves = []

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
            A new Position holding the new board state.
        Raise:
            ValueError if the move is illegal from this position.
        """
        try:
            next_board = self.board.copy()
            next_board.push_san(move)
            next_position = Position(next_board)
            self.moves.append(
                Move(self, next_position, move, evaluation, remarks))
            return next_position
        except chess.IllegalMoveError as exc:
            raise ValueError(
                f'Move {move} is illegal from board {self.board.fen()}'
            ) from exc

    def merge(self, other: 'Position') -> None:
        """Merges another Position's moves with this Position.

        Stores the other Position's moves in this Position but does not mutate
        the other Position.
        The other Position should be discarded.

        Args:
            other: The other Position.
        Raise:
            ValueError the other Position's FEN string does not match this one's.
        """
        fen1, fen2 = self.board.fen(), other.board.fen()
        if fen1 != fen2:
            raise ValueError(
                f'Cannot merge differing positions {fen1} and {fen2}')

        self.moves.extend(other.moves)


class Move:
    """The transition from one Position to another.

    Attributes:
        from_position: The Position before this move is make.
        to_position: The Position after this move is make.
        label: The algebraic notation of the move.
        evaluation: Commentary on the move (e.g. !, ?).
        remarks: A list of remarks on the move or position.
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
        self.evaluation = evaluation
        if remarks:
            self.remarks = remarks
        else:
            self.remarks = []

    # TODO: Add method for merging two moves.
