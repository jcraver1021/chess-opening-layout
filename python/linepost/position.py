import linepost.move as lpmove


class Position:
    def __init__(self, board):
        self.board = board
        self.moves = []

    def make_move(self, move, evaluation=None, remarks=None):
        next_board = self.board.copy()
        next_board.push_san(move)
        self.moves.append(lpmove.Move(self.board, next_board,
                                      move, evaluation, remarks))
        return Position(next_board)

    def merge(self, other):
        if self.board.fen() != other.board.fen():
            raise ValueError('Cannot merge differing positions')

        self.moves.extend(other.moves)
