import pytest
from linepost.line import Line, Token
from linepost.position import Game


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
    token = Token(string)
    got_bool = token.is_chess_move()
    assert want_bool == got_bool


@pytest.mark.parametrize("string,want_move,want_eval", [
    ('great move', None, None),
    ('Nf3', 'Nf3', None),
    ('Nf3!!', 'Nf3', '!!'),
])
def test_tokens(string, want_move, want_eval):
    token = Token(string)
    assert want_move == token.get_move()
    assert want_eval == token.get_evaluation()


@pytest.mark.parametrize(
    "string,want_labels,want_evals_by_index,want_pos_remarks_by_index,want_move_remarks_by_index",  # noqa: E501
    [
        ('e4 e5 Nf3', ['e4', 'e5', 'Nf3'], {}, {}, {}),
        ('e4 e5 Nf3 Nc6', ['e4', 'e5', 'Nf3', 'Nc6'], {}, {}, {}),
        ('', [], {}, {}, {}),
        ('e4', ['e4'], {}, {}, {}),
        ('e4 p"Best by test" p"Black has many responses"', ['e4'], {}, {
            1: {'Black has many responses', 'Best by test'},
        }, {}),
        (
            'd4 m"I better not see another London" d5 Bf4?! m"really?!" m"goddammit" p"I am rooting for Black now"',  # noqa: E501
            ['d4', 'd5', 'Bf4'],
            {
                3: '?!'
            },
            {
                3: {'I am rooting for Black now'},
            },
            {
                1: {'I better not see another London'},
                3: {'really?!', 'goddammit'}
            }),
    ])
def test_lines(string, want_labels, want_evals_by_index,
               want_pos_remarks_by_index, want_move_remarks_by_index):
    game = Game()
    line = Line(string, game)
    assert len(want_labels) + 1 == len(line.line)
    for i, position in enumerate(line.line):
        if i < len(line.line) - 1:
            assert position.remarks == want_pos_remarks_by_index.get(i, set())
            move = None
            for move_key in position.moves:
                move = position.moves[move_key]
                break
            assert move.label == want_labels[i]
            assert move.evaluation == want_evals_by_index.get(i + 1, '')
            assert move.remarks == want_move_remarks_by_index.get(i + 1, set())
        else:
            assert len(position.moves) == 0


@pytest.mark.parametrize("string", [
    "e5",
    "e4 Bc5",
    "e4 e5 O-O O-O",
])
def test_invalid_lines(string):
    game = Game()
    with pytest.raises(ValueError):
        _ = Line(string, game)


@pytest.mark.parametrize("string", [
    'e4 c"comment"',
    'e4 d5 k"die"',
])
def test_invalid_comments(string):
    game = Game()
    with pytest.raises(ValueError):
        _ = Line(string, game)
