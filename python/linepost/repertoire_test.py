from parameterized import parameterized
import linepost.repertoire as repertoire

@parameterized([
    ('e4', 'e4', []),
    ('Ke2??', 'Ke2', []),
    ('Qh4;rude;wtf', 'Qh4', ['rude', 'wtf']),
])
def test_parse_move(input_move, expected_label, expected_remarks):
    move, _, remarks = repertoire.parse_move(input_move)
    assert expected_label == move
    assert expected_remarks == remarks