# Stores a single line based on algebraic notation.

import chess
import linepost.position as lppos
import re

COORDINATE_PATTERN = '[a-h][1-8]'
PROMOTION_PATTERN = r'(?:\=)?[NBRQ]'
PAWN_PATTERN = f'(?:[a-h]x)?{COORDINATE_PATTERN}(?:{PROMOTION_PATTERN})?'
PIECE_PATTERN = f'(?:[NBRQK][a-h1-8]?x?{COORDINATE_PATTERN})'
CASTLES_PATTERN = '[oO](?:-[oO]){1,2}'
CHECK_PATTERN = '[+#]'
ONCE_PATTERN = '{1}'
MOVE_PATTERN = f'(?:{PAWN_PATTERN}|{PIECE_PATTERN}|{CASTLES_PATTERN}){ONCE_PATTERN}{CHECK_PATTERN}?'  # noqa: E501
EVALUATION_PATTERN = r'\?\?|\?|\?!|!\?|!|!!'
MOVE_LABEL = 'move'
EVAL_LABEL = 'eval'
MOVE_REGEX = re.compile(
    f'^(?P<{MOVE_LABEL}>{MOVE_PATTERN})(?P<{EVAL_LABEL}>{EVALUATION_PATTERN})?$'
)  # noqa: E501


class Token:
    """Token is the textual representation of a chess move, or a comment
    thereupon.
    """

    def __init__(self, s):
        self._raw = s
        self._match = MOVE_REGEX.match(self._raw)

    def is_chess_move(self):
        return self._match is not None

    def get_move(self):
        return self._match.group(MOVE_LABEL) if self.is_chess_move() else None

    def get_evaluation(self):
        return self._match.group(EVAL_LABEL) if self.is_chess_move() else None

    def __str__(self):
        return self._raw


SPLIT_CHAR = '|'
# TODO: add a character for alt-lines
# These will be parsed as alternate remarks
# Rename both constants so it's clear what they're for.

START_TOKEN = Token('start')
END_TOKEN = Token('end')


class Line:

    def __init__(self, line, starting_position=None):
        self._line_raw = line
        # Replace split with space + split to avoid later splitting.
        self._tokens = [
            Token(token_str) for token_str in line.replace(
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
                        last_chess_token.get_evaluation(), remarks)
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
