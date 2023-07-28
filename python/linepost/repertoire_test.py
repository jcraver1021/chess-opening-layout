import pytest
from linepost.repertoire import Repertoire


@pytest.mark.parametrize("lines", [
    [
        'e4 e5 Nf3',
        'e4 c5 Nf3',
    ],
    [
        'e4 e5 Nf3',
        '',
        'e4 c5 Nf3',
    ],
    [
        'e4 e5 Nf3',
        '    ',
        'e4 c5 Nf3',
    ],
    [
        'e4 e5 Nf3',
        '# Some people hate it, but you can play the Alapin if you want',
        'e4 c5 c3',
    ],
])
def test_lines(lines):
    _ = Repertoire.from_lines(lines)
