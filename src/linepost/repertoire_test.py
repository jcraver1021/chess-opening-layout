import pytest
from linepost.repertoire import Repertoire


def test_add_invalid_no_change():
    rep = Repertoire()
    rep.add_line('e4 e5 Ke2')
    with pytest.raises(ValueError):
        rep.add_line('d4 d4')
    assert len(rep.lines) == 1
    assert len(rep.lines[0].line) == 4
    assert len(rep.game.fens) == 4
    with pytest.raises(ValueError):
        rep.add_line('c4 Be5')
    assert len(rep.lines) == 1
    assert len(rep.lines[0].line) == 4
    assert len(rep.game.fens) == 4


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
    [
        'e4 e5 Nf3\n',
        'e4 c5 Nf3\n',
    ],
    [
        'e4 e5 Nf3\n',
        '\n',
        'e4 c5 Nf3\n',
    ],
    [
        'e4 e5 Nf3\n',
        '    \n',
        'e4 c5 Nf3\n',
    ],
    [
        'e4 e5 Nf3\n',
        '# Some people hate it, but you can play the Alapin if you want\n',
        'e4 c5 c3\n',
    ],
])
def test_lines(lines):
    _ = Repertoire.from_lines(lines)
