"""Repertoire holds the game graph and all ingested lines.
"""

import chess

from linepost.position import Game
from linepost.line import Line


class Repertoire:
    """The game graph and all lines which constructed it.

    Attributes:
        game: The Game graph.
        lines: All Line objects which constructed the game graph.
    """

    def __init__(self) -> None:
        self.game = Game()
        self.lines = []

    def add_line(self, line: str) -> None:
        """Ingests a line, adding new positions and moves to the Game graph.
        """
        self.lines.append(Line(line, self.game))
