import chess
import pytest
import linepost.line as lpline

@pytest.mark.parametrize("string,want_labels,want_evals_by_index,want_remarks_by_index", [
    ('e4 e5 Nf3', ['e4', 'e5', 'Nf3'], {}, {}),
    ('e4 e5 Nf3 Nc6', ['e4', 'e5', 'Nf3', 'Nc6'], {}, {}),
    ('', [], {}, {}),
    ('e4', ['e4'], {}, {}),
    ('d4|I better not see another London d5 Bf4?!|really?!|goddammit', ['d4', 'd5', 'Bf4'], {3: '?!'}, {1: ['I better not see another London'], 3: ['really?!', 'goddammit']}),
])
def test_lines(string, want_labels, want_evals_by_index, want_remarks_by_index):
    line = lpline.Line(string)
    assert len(want_labels) + 1 == len(line.moves)
    for i, move in enumerate(line.moves):
        if i > 0:
            assert move.label == want_labels[i - 1]
            assert move.evaluation == want_evals_by_index.get(i, None)
        assert move.remarks == want_remarks_by_index.get(i, [])

@pytest.mark.parametrize("string", [
    # "Ke0 e5", invalid moves don't parse currently
    "e5",
    "e4 Bc5",
    # "e4 e5 O-O O-O", castles needs to be defined
])
def test_invalid_lines(string):
    with pytest.raises(chess.IllegalMoveError):
        line = lpline.Line(string)
