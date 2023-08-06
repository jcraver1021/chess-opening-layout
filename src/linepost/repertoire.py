"""Repertoire holds the game graph and all ingested lines.
"""

import chess

from linepost.position import Game
from linepost.line import Line
from typing import Iterable, Optional


class Repertoire:
    """The game graph and all lines which constructed it.

    Attributes:
        game: The Game graph.
        lines: All Line objects which constructed the game graph.
    """

    @classmethod
    def from_lines(cls,
                   line_source: Iterable[str],
                   rep: Optional['Repertoire'] = None) -> 'Repertoire':
        """From a list of lines, create a repertoire.

        Optionally, add these lines to an existing repertoire.

        Args:
            line_source: A list of lines (e.g. from a file).
            rep: The repertoire to add the lines to. Creates one if none provided.
        Returns:
            The repertoire with the provided lines.
        """
        if rep is None:
            rep = Repertoire()
        for line in line_source:
            line = line.strip()
            if line and not line.startswith('#'):
                rep.add_line(line)
        return rep

    @classmethod
    def from_file(cls,
                  filename: str,
                  rep: Optional['Repertoire'] = None) -> 'Repertoire':
        """Create a repertoire from lines in a text file.

        Optionally, add these lines to an existing repertoire.

        Args:
            filename: The name of the file with the lines.
            rep: The repertoire to add the lines to. Creates one if none provided.
        Returns:
            The repertoire with the provided lines.
        """
        with open(filename) as file:
            return Repertoire.from_lines(file.readlines())

    def __init__(self) -> None:
        self.game = Game()
        self.lines = []

    def add_line(self, line: str) -> None:
        """Ingests a line, adding new positions and moves to the Game graph.
        """
        self.lines.append(Line(line, self.game))
