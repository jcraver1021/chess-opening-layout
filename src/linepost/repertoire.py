"""Repertoire holds the game graph and all ingested lines.
"""

import chess

from linepost.position import Game
from linepost.line import Line
from linepost.visual import visualize
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
                   skip_invalid: bool = False,
                   rep: Optional['Repertoire'] = None) -> 'Repertoire':
        """From a list of lines, create a repertoire.

        Optionally, add these lines to an existing repertoire.

        Args:
            line_source: A list of lines (e.g. from a file).
            skip_invalid: Whether to skip invalid lines.
            rep: The repertoire to add the lines to. Creates one if none provided.
        Returns:
            The repertoire with the provided lines.
        Raises:
            ValueError if adding an invalid line and skip_invalid is False.
        """
        if rep is None:
            rep = Repertoire()
        for line in line_source:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    rep.add_line(line)
                except ValueError as exc:
                    if not skip_invalid:
                        raise exc
        return rep

    @classmethod
    def from_file(cls,
                  filename: str,
                  skip_invalid: bool = False,
                  rep: Optional['Repertoire'] = None) -> 'Repertoire':
        """Create a repertoire from lines in a text file.

        Optionally, add these lines to an existing repertoire.

        Args:
            filename: The name of the file with the lines.
            skip_invalid: Whether to skip invalid lines.
            rep: The repertoire to add the lines to. Creates one if none provided.
        Returns:
            The repertoire with the provided lines.
        """
        with open(filename) as file:
            return Repertoire.from_lines(file.readlines(), skip_invalid)

    def __init__(self) -> None:
        self.game = Game()
        self.lines = []

    def add_line(self, line: str) -> None:
        """Ingests a line, adding new positions and moves to the Game graph.

        Does not mutate the game state if the line is invalid.

        Args:
            line: A string representing one line in the repertoire.
        """
        # Ingest the line into a new game first in case it fails.
        _ = Line(line, Game())

        self.lines.append(Line(line, self.game))

    def visualize(self) -> 'graphviz.Digraph':
        """Returns a graphviz graph of the game.

        Returns:
            The rendered graph.
        """
        return visualize(self.game)
