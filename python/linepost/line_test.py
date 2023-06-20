import chess
import pytest
import linepost.line as lpline


# TODO: Generate these for more complete coverage
@pytest.mark.parametrize("string,want_bool", [
    ('e4', True),
    ('c6', True),
    ('e0', False),
    ('e9', False),
    ('cxd5', True),
    ('cxd9', False),
    ('cx6', False),
    ('hxg5', True),
    ('hxi5', False),
    ('ixh5', False),
    ('e1=N', True),
    ('f8=B+', True),
    ('gxh8=R', True),
    ('axb1=Q+', True),
    ('b8N', True),
    ('cxd8B', True),
    ('d8R', True),
    ('e8Q', True),
    ('a8=K', False),
    ('a1K', False),
    ('+', False),
    ('#', False),
    ('a1+', True),
    ('a8#', True),
    ('Ne7', True),
    ('Bf4', True),
    ('Re1', True),
    ('Qh5', True),
    ('Ke2', True),
    ('Jh5', False),
    ('Qe0', False),
    ('Rj5', False),
    ('B4', False),
    ('Nbd2', True),
    ('N4d2', True),
    ('Nc4d2', False),
    ('N4cd2', False),
    ('Rxb1', True),
    ('Raxb1', True),
    ('R3xb2', True),
    ('Rb3xb2', False),
    ('Raxb1=Q', False),
    ('Raxb1#', True),
    ('Ke2?', True),
    ('Ke2!', True),
    ('Ke2!!', True),
    ('Bf4??', True),
    ('a4?!', True),
    ('a4!?', True),
    ('!', False),
    ('?', False),
    ('o', False),
    ('o-o', True),
    ('o-o-o', True),
    ('o-o#', True),
    ('o-o-o??', True),
    ('o-o-o-o', False),
    ('O', False),
    ('O-O', True),
    ('O-O-O', True),
    ('O-O+', True),
    ('O-O-O!!', True),
    ('O-O-O-O', False),
    ('chess move', False),
])
def test_is_chess_move(string, want_bool):
    token = lpline.Token(string)
    got_bool = token.is_chess_move()
    assert want_bool == got_bool


@pytest.mark.parametrize("string,want_move,want_eval", [
    ('great move', None, None),
    ('Nf3', 'Nf3', None),
    ('Nf3!!', 'Nf3', '!!'),
])
def test_tokens(string, want_move, want_eval):
    token = lpline.Token(string)
    assert want_move == token.get_move()
    assert want_eval == token.get_evaluation()


@pytest.mark.parametrize("string,want_labels,want_evals_by_index,want_remarks_by_index", [  # noqa: E501
    ('e4 e5 Nf3', ['e4', 'e5', 'Nf3'], {}, {}),
    ('e4 e5 Nf3 Nc6', ['e4', 'e5', 'Nf3', 'Nc6'], {}, {}),
    ('', [], {}, {}),
    ('e4', ['e4'], {}, {}),
    ('d4|I better not see another London d5 Bf4?!|really?!|goddammit', ['d4', 'd5', 'Bf4'], {3: '?!'}, {1: ['I better not see another London'], 3: ['really?!', 'goddammit']}),  # noqa: E501
])
def test_lines(string, want_labels,
               want_evals_by_index, want_remarks_by_index):
    line = lpline.Line(string)
    assert len(want_labels) + 1 == len(line.line)
    for i, position in enumerate(line.line):
        if i < len(line.line) - 1:
            move = position.moves[0]
            assert move.label == want_labels[i]
            assert move.evaluation == want_evals_by_index.get(i + 1, None)
            assert move.remarks == want_remarks_by_index.get(i + 1, [])
        else:
            assert len(position.moves) == 0


@pytest.mark.parametrize("string", [
    "e5",
    "e4 Bc5",
    "e4 e5 O-O O-O",
])
def test_invalid_lines(string):
    with pytest.raises(chess.IllegalMoveError):
        _ = lpline.Line(string)
