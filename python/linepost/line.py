import chess
from linepost.move import Move, Token

SPLIT_CHAR = '|'
# TODO: add a character for alt-lines
# These will be parsed as alternate remarks
# Rename both constants so it's clear what they're for.

class Line:
    def __init__(self, line, starting_position=None):
        self._line_raw = line
        # Replace split with space + split so that we don't have to split tokens further
        self._tokens = [Token(token_str) for token_str in line.replace(SPLIT_CHAR, f' {SPLIT_CHAR}').split()]
        if starting_position is None:
            starting_position = chess.Board()
        self.start = starting_position
        self.moves = [move for move in self._construct_moves()]
    
    def _construct_moves(self):
        last_chess_token = Token('start')
        remarks = []
        remark = []
        position = self.start
        # Add None at the end so we can serve the final chess move.
        for token in self._tokens + [None]:
            print(f'remark: {remark}')
            print(f'remarks: {remarks}')
            if token is None or token.is_chess_move():
                if remark:
                    remarks.append(' '.join(remark))
                yield Move(position, last_chess_token.get_move(), last_chess_token.get_evaluation(), remarks)
                if token is not None:
                    remarks = []
                    remark = []
                    position = position.copy()
                    position.push_san(token.get_move())
                    last_chess_token = token
            else:
                token_str = str(token)
                if token_str.startswith(SPLIT_CHAR):
                    if remark:
                        remarks.append(' '.join(remark))
                        remark = []
                    token_str = token_str[1:]
                remark.append(token_str)
