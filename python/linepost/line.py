"""Line stores a single opening line from algebraic notation.
"""

import chess
from linepost.position import Game
from linepost.position import Move
from linepost.position import Position
import re

from typing import Generator, Optional

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
)


class Token:
    """Textual representation of a chess move, evaluation, or comment.

    It can be any legal chess move, with or without evaluations (e.g. ?, !), or
    it can be part of a commentary about a move or position.
    """

    def __init__(self, s: str):
        """Initializes the token based on whether it's chess move.

        Args:
            s: The raw string.
        """
        self._raw = s
        self._match = MOVE_REGEX.match(self._raw)

    def is_chess_move(self) -> bool:
        """Whether this token represents a chess move.

        Returns:
            Whether this move matches the compiled MOVE_REGEX.
        """
        return self._match is not None

    def get_move(self) -> Optional[str]:
        """If this is a chess move, returns the move label.

        Returns:
            The move portion of the chess token.
        """
        return self._match.group(MOVE_LABEL) if self.is_chess_move() else None

    def get_evaluation(self) -> Optional[str]:
        """If this is a chess move, returns the evaluation portion.

        Returns:
            The evaluation portion of the chess token.
        """
        return self._match.group(EVAL_LABEL) if self.is_chess_move() else None

    def __str__(self):
        return self._raw


SPLIT_CHAR = '|'
# TODO: Add a character for alt-lines
# These will be parsed as alternate remarks
# Rename both constants so it's clear what they're for.
# TODO: Add designation for a non-initial starting position.

START_TOKEN = Token('start')
END_TOKEN = Token('end')


class Line:
    """A single line (no variation) of a chess opening.

    Parses the entire line, including commentary, and stores it as a list of
    list of Position objects (with Move objects as the edges). Each
    Position will have a Move link to each subsequent position.

    Attributes:
        initial_board: The chess.Board representing the initial position.
        line: The list of Position objects in the line.
    """

    def __init__(self,
                 line: str,
                 game: Game,
                 initial_board: Optional[chess.Board] = None) -> None:
        """Initializes the line

        Args:
            line: A string representing the opening line and commentary.
            initial_board: The initial state of the chess board at the beginning
                of the line (defaults to the starting position).
        Raises:
            ValueError if the line cannot be completely parsed.
        """
        self._line_raw = line
        # Replace split with space + split to avoid later splitting.
        self._tokens = [
            Token(token_str) for token_str in line.replace(
                SPLIT_CHAR, f' {SPLIT_CHAR}').split()
        ]
        self.game = game
        if initial_board is None:
            initial_board = chess.Board()
        self._start = game.get_position(initial_board)
        self.line = [self._start]
        self.line.extend(
            [position for position in self._construct_positions()])

    def _construct_positions(self) -> Generator[Position, None, None]:
        """Generates the positions based on this line.

        Returns:
            A generator yielding each Position based on this line.
        """
        last_chess_token = START_TOKEN
        remarks = []
        remark = []
        position = self._start
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
