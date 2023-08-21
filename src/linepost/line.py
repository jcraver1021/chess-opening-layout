"""Line stores a single opening line from algebraic notation.
"""

import chess
from linepost.position import Game, Move, Position
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
MOVE_EVAL_PATTERN = f'(?P<{MOVE_LABEL}>{MOVE_PATTERN})(?P<{EVAL_LABEL}>{EVALUATION_PATTERN})?'
MOVE_REGEX = re.compile(f'^{MOVE_EVAL_PATTERN}$')

POS_PREFIX = 'pP'
MOVE_PREFIX = 'mM'
PREFIX_PATTERN = f'[{POS_PREFIX}{MOVE_PREFIX}]{ONCE_PATTERN}'
PREFIX_LABEL = 'prefix'
REMARK_LABEL = 'remark'
REMARK_TOKEN_PATTERN = f'(?P<{PREFIX_LABEL}>{PREFIX_PATTERN})"(?P<{REMARK_LABEL}>[^"]*?)"'
REMARK_PATTERN = re.compile(f'^{REMARK_TOKEN_PATTERN}$')


def unlabel_pattern(pattern: str) -> str:
    return re.sub('P<.*?>', ':', pattern)


FULL_MOVE_PATTERN = f'{MOVE_EVAL_PATTERN}(\\s+{REMARK_TOKEN_PATTERN})*'
FULL_LINE_PATTERN = f'{FULL_MOVE_PATTERN}(\\s+{FULL_MOVE_PATTERN})*'
FULL_LINE_REGEX = re.compile(f'^{unlabel_pattern(FULL_LINE_PATTERN)}$')


def can_parse_line(line: str) -> bool:
    return FULL_LINE_REGEX.match(line) is not None


def parse_line(line: str) -> None:
    # todo: make this return a tuple of lists
    if not can_parse_line(line):
        raise ValueError(f'Line "{line}" cannot be parsed')


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
        self.game = game
        if initial_board is None:
            initial_board = chess.Board()
        self._start = game.get_position(initial_board)
        self.line = [self._start]
        self._extract_remarks()
        self.line.extend(
            [position for position in self._construct_positions()])

    def _extract_remarks(self) -> None:
        # TODO: Make this a standalone function with its own tests
        # TODO: Make sure the Position tests pass with the new logic
        line = self._line_raw
        self.remarks = re.findall(re.compile(f'[pPmM]".*?"'), line)
        self.position_remarks = []
        self.move_remarks = []
        for remark in self.remarks:
            if remark[0].lower() == "p":
                remark_list = self.position_remarks
                prefix = "p"
            else:
                remark_list = self.move_remarks
                prefix = "m"
            remark_index = len(remark_list)
            remark_list.append(remark[2:-1])
            line = line.replace(remark, f'{prefix}{remark_index}', 1)
        self.tokens = list(map(Token, line.split()))

    def _construct_positions(self) -> Generator[Position, None, None]:
        """Generates the positions based on this line.

        Returns:
            A generator yielding each Position based on this line.
        """
        last_chess_token = START_TOKEN
        position_remarks = []
        move_remarks = []
        position = self._start
        # Add None at the end so we can serve the final chess move.
        for token in self.tokens + [END_TOKEN]:
            if token in {START_TOKEN, END_TOKEN} or token.is_chess_move():
                if last_chess_token is not START_TOKEN:
                    position = position.make_move(
                        last_chess_token.get_move(),
                        last_chess_token.get_evaluation(), position_remarks,
                        move_remarks)
                    yield position
                if token is not END_TOKEN:
                    position_remarks = []
                    move_remarks = []
                    last_chess_token = token
            else:
                pointer = str(token)
                if len(pointer) < 1:
                    raise ValueError(
                        f'Invalid token {token} in line {self._line_raw}')
                if pointer[0] == "p":
                    position_remarks.append(self.position_remarks[int(
                        pointer[1:])])
                elif pointer[0] == "m":
                    move_remarks.append(self.move_remarks[int(pointer[1:])])
                else:
                    raise ValueError(
                        f'Invalid token {token} in line {self._line_raw}')
