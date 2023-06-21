# Position and Move are the nodes and edges of the game graph.

import chess


class Position:

    def __init__(self, board):
        self.board = board
        self.moves = []

    def make_move(self, move, evaluation=None, remarks=None):
        try:
            next_board = self.board.copy()
            next_board.push_san(move)
            next_position = Position(next_board)
            self.moves.append(
                Move(self, next_position, move, evaluation, remarks))
            return next_position
        except chess.IllegalMoveError as exc:
            raise ValueError(
                f'Move {move} is illegal from board {self.board.fen()}')

    def merge(self, other):
        fen1, fen2 = self.board.fen(), other.board.fen()
        if fen1 != fen2:
            raise ValueError(
                f'Cannot merge differing positions {fen1} and {fen2}')

        self.moves.extend(other.moves)


class Move:
    """Move represents the transition from one position to another.
    """

    def __init__(self,
                 from_position,
                 to_position,
                 label,
                 evaluation=None,
                 remarks=None):
        self.from_position = from_position
        self.to_position = to_position
        self.label = label
        self.evaluation = evaluation
        if remarks:
            self.remarks = remarks
        else:
            self.remarks = []
