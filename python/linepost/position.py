# Position and Move are the nodes and edges of the game graph.


class Position:

    def __init__(self, board):
        self.board = board
        self.moves = []

    def make_move(self, move, evaluation=None, remarks=None):
        next_board = self.board.copy()
        next_board.push_san(move)
        self.moves.append(
            Move(self.board, next_board, move, evaluation, remarks))
        return Position(next_board)

    def merge(self, other):
        if self.board.fen() != other.board.fen():
            raise ValueError('Cannot merge differing positions')

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
