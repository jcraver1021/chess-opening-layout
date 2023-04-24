import pytest
import linepost.line as lpline

@pytest.mark.parametrize("string,want_moves_length,want_remarks_by_index", [
    ('e4 e5 Nf3', 4, {}),
    ('e4 e5 Nf3 Nf6', 5, {}),
    ('', 1, {}),
    ('e4', 2, {}),
    ('d4|I better not see another London d5 Bf4|really?!|goddammit', 4, {1: ['I better not see another London'], 3: ['really?!', 'goddammit']}),
])
def test_lines(string, want_moves_length, want_remarks_by_index):
    line = lpline.Line(string)
    assert want_moves_length == len(line.moves)
    for i, move in enumerate(line.moves):
        assert move.remarks == want_remarks_by_index.get(i, [])

# TODO: Test that invalid moves result in a failure.
