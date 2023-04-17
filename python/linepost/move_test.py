from parameterized import parameterized
import linepost.move as move

# TODO: Generate these for more complete coverage

@parameterized([
    ('e4', True),
    ('c6', True),
    ('e0', False),
    ('e9', False),
    ('cxd5', True),
    ('cxd9', False),
    ('hxg5', True),
    ('hxi5', False),
    ('ixh5', False),
    ('e1=N', True),
    ('f8=B+', True),
    ('gx8=R', True),
    ('ax1=Q+', True),
    ('b8N', True),
    ('cx8B', True),
    ('d8R', True),
    ('e8Q', True),
    ('a8=K', False),
    ('a8=K', False),
    ('+', False),
    ('#', False),
    ('a1+', True),
    ('a8#', True),
    ('Ne7', True),
    ('Bf4', True),
    ('Re1', True),
    ('Qh5', True),
    ('Nbd2', True),
    ('N4d2', True),
    ('Nc4d2', False),
    ('Nc4d2', False),
    ('Rxb1', True),
    ('Raxb1', True),
    ('R3xb2', True),
    ('Rb3xb2', False),
    ('Raxb1=Q', False),
    ('Raxb1#', True),
])
def test_is_chess_move(token, want_bool):
    got_bool = move.is_chess_move(token)
    assert want_bool == got_bool
