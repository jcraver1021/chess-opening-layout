import re

COORDINATE_PATTERN = f'[a-h][1-8]'
PROMOTION_PATTERN = r'(?:\=)?[NBRQ]'
PAWN_PATTERN = f'(?:[a-h]x)?{COORDINATE_PATTERN}(?:{PROMOTION_PATTERN})?'
PIECE_PATTERN = f'(?:[NBRQK][a-h1-8]?x?{COORDINATE_PATTERN})'
CHECK_PATTERN = '[+#]'
ONCE_PATTERN = '{1}'
MOVE_PATTERN = f'(?:{PAWN_PATTERN}|{PIECE_PATTERN}){ONCE_PATTERN}{CHECK_PATTERN}?'
EVALUATION_PATTERN = '\?\?|\?|\?!|!\?|!|!!'
MOVE_REGEX = re.compile(f'^(?P<move>{MOVE_PATTERN})(?P<eval>{EVALUATION_PATTERN})?$')

class _Token:
    def __init__(self, s):
        self.match = MOVE_REGEX.match(s)
    
    def is_chess_move(self):
        return self.match is not None

def tokenize_line_by_move(line):
    # try to tokenize it and join together stuff that's not a move
    # like, you can have space characters and such
    # so the start of a move is unambiguously a chess move, starting with the valid letters
    # yield the things maybe
    pass

class Move:
    def __init__(self, position, label, evaluation=None, remarks=None, next_moves=None):
        self.position = position
        self.label = label
        self.evaluation = evaluation
        if remarks:
            self.remarks = remarks
        else:
            self.remarks = []
        if next_moves:
            self.next_moves = next_moves
        else:
            self.next_moves = []
    
    @classmethod
    def from_string(cls, last_position, move_string, evaluation):
        # split and find the remarks, etc.
        # nope, token is split by this point, so join the remarks, make the move, etc.
        # TODO move to line class
        pass