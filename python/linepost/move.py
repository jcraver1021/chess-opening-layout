import re

move_regex = re.compile(r'^((?:(?:[a-h]x)?[a-h][1-8](?:(?:\=)?[NBRQ])?|(?:[NBRQK]x?[a-h1-8]?[a-h][1-8])){1}[+#]?)(\?\?|\?|!|!\?|\?!|!!)?$')

# (?:X) represents a non capturing group
# coord: [a-h][1-8]
# pawn: (?:[a-h]x)?[a-h][1-8](?:(?:\=)?[NBRQ])?
# piece: (?:[NBRQK]x?[a-h1-8]?[a-h][1-8])
# check: [+#]?
# combination (capturable): ((?:(?:[a-h]x)?[a-h][1-8](?:(?:\=)?[NBRQ])?|(?:[NBRQK]x?[a-h1-8]?[a-h][1-8])){1}[+#]?)
# evaluation (capturable): (\?\?|\?|!|!\?|\?!|!!)?
# final: ((?:(?:[a-h]x)?[a-h][1-8](?:(?:\=)?[NBRQ])?|(?:[NBRQK]x?[a-h1-8]?[a-h][1-8])){1}[+#]?)(\?\?|\?|!|!\?|\?!|!!)?

def is_chess_move(token):
    return move_regex.match(token) is not None

def tokenize_line(line):
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
    def fromString(cls, last_position, move_string):
        # split and find the remarks, etc.
        pass