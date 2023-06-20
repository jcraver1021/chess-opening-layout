import chess
import linepost.move as lpmove
import linepost.position as lppos

SPLIT_CHAR = '|'
# TODO: add a character for alt-lines
# These will be parsed as alternate remarks
# Rename both constants so it's clear what they're for.


START_TOKEN = lpmove.Token('start')
END_TOKEN = lpmove.Token('end')


class Line:
    def __init__(self, line, starting_position=None):
        self._line_raw = line
        # Replace split with space + split to avoid later splitting.
        self._tokens = [
            lpmove.Token(token_str) for token_str in line.replace(
                SPLIT_CHAR, f' {SPLIT_CHAR}').split()
        ]
        if starting_position is None:
            starting_position = chess.Board()
        self.start = lppos.Position(starting_position)
        self.line = [self.start]
        self.line.extend(
            [position for position in self._construct_positions()])

    def _construct_positions(self):
        last_chess_token = START_TOKEN
        remarks = []
        remark = []
        position = self.start
        # Add None at the end so we can serve the final chess move.
        for token in self._tokens + [END_TOKEN]:
            if token in {START_TOKEN, END_TOKEN} or token.is_chess_move():
                if remark:
                    remarks.append(' '.join(remark))
                if last_chess_token is not START_TOKEN:
                    position = position.make_move(
                        last_chess_token.get_move(),
                        last_chess_token.get_evaluation(),
                        remarks
                    )
                    yield position
                if token is not END_TOKEN:
                    remarks = []
                    remark = []
                    last_chess_token = token
            else:
                token_str = str(token)
                if token_str.startswith(SPLIT_CHAR):
                    if remark:
                        remarks.append(' '.join(remark))
                        remark = []
                    token_str = token_str[1:]
                remark.append(token_str)
