import chess
import pytest
import linepost.line as lpline


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
