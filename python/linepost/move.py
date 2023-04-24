import re

COORDINATE_PATTERN = f'[a-h][1-8]'
PROMOTION_PATTERN = r'(?:\=)?[NBRQ]'
PAWN_PATTERN = f'(?:[a-h]x)?{COORDINATE_PATTERN}(?:{PROMOTION_PATTERN})?'
PIECE_PATTERN = f'(?:[NBRQK][a-h1-8]?x?{COORDINATE_PATTERN})'
CASTLES_PATTERN = '[oO](?:-[oO]){1,2}'
CHECK_PATTERN = '[+#]'
ONCE_PATTERN = '{1}'
MOVE_PATTERN = f'(?:{PAWN_PATTERN}|{PIECE_PATTERN}|{CASTLES_PATTERN}){ONCE_PATTERN}{CHECK_PATTERN}?'
EVALUATION_PATTERN = r'\?\?|\?|\?!|!\?|!|!!'
MOVE_LABEL = 'move'
EVAL_LABEL = 'eval'
MOVE_REGEX = re.compile(f'^(?P<{MOVE_LABEL}>{MOVE_PATTERN})(?P<{EVAL_LABEL}>{EVALUATION_PATTERN})?$')

class Token:
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
    def __init__(self, position, label, evaluation=None, remarks=None):
        self.position = position
        self.label = label
        self.evaluation = evaluation
        if remarks:
            self.remarks = remarks
        else:
            self.remarks = []
