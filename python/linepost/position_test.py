import chess
import pytest
import linepost.position as lppos


def split_tokens(line, position=None):
    if position is None:
        position = lppos.Position(chess.Board())
    for token in line.split():
        position = position.make_move(token)
    return position


@pytest.mark.parametrize("move,evaluation,remarks", [
    ("e4", None, []),
    ("Nc3", "?!", ["Why, tho?"]),
    ("b4", "!!", ["Hi, lularobs!", "bishop bait!"]),
])
def test_move(move, evaluation, remarks):
    pos = lppos.Position(chess.Board())
    next_pos = pos.make_move(move, evaluation, remarks)
    assert len(pos.moves) == 1
    assert pos.moves[0].label == move
    assert pos.moves[0].evaluation == evaluation
    assert pos.moves[0].remarks == remarks
    assert pos.moves[0].from_position == pos
    assert pos.moves[0].to_position == next_pos


@pytest.mark.parametrize("move", [
    ("e5"),
    ("Ke2"),
    ("O-O"),
])
def test_invalid_move(move):
    pos = lppos.Position(chess.Board())
    with pytest.raises(ValueError):
        _ = pos.make_move(move)


@pytest.mark.parametrize("line,branch1,branch2", [
    ("e4", "e5", "c5"),
    ("e4 c6 d4 d5", "Nc3 dxe4", "e5 c5"),
])
def test_merge(line, branch1, branch2):
    parent1 = split_tokens(line)
    _ = split_tokens(branch1, parent1)
    parent2 = split_tokens(line)
    _ = split_tokens(branch2, parent2)
    parent1.merge(parent2)
    assert len(parent1.moves) == 2


@pytest.mark.parametrize("line1,line2", [
    ("e4", "d4"),
    ("e4", "e4 e5"),
])
def test_invalid_merge(line1, line2):
    pos1 = split_tokens(line1)
    pos2 = split_tokens(line2)

    with pytest.raises(ValueError):
        pos1.merge(pos2)

    with pytest.raises(ValueError):
        pos2.merge(pos1)
