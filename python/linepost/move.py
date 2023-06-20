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
MOVE_REGEX = re.compile(f'^(?P<{MOVE_LABEL}>{MOVE_PATTERN})(?P<{EVAL_LABEL}>{EVALUATION_PATTERN})?$')  # noqa: E501


class Token:
    """Token is the textual representation of a chess move, or a comment
    thereupon.

    TODO: Consider moving Token to the Line class.
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


class Move:
    """Move represents the transition from one position to another.
    """

    def __init__(self, from_position, to_position, label,
                 evaluation=None, remarks=None):
        self.from_position = from_position
        self.to_position = to_position
        self.label = label
        self.evaluation = evaluation
        if remarks:
            self.remarks = remarks
        else:
            self.remarks = []
