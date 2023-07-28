import chess
import pytest
from linepost.position import Game, Position


@pytest.mark.parametrize("move_label,evaluation,remarks", [
    ("e4", "", set()),
    ("Nc3", "?!", {"Why, tho?"}),
    ("b4", "!!", {"Hi, lularobs!", "bishop bait!"}),
])
def test_move(move_label, evaluation, remarks):
    game = Game()
    pos = Position(game, chess.Board())
    next_pos = pos.make_move(move_label, evaluation, remarks)
    assert len(pos.moves) == 1
    move = None
    for move_key in pos.moves:
        move = pos.moves[move_key]
        break
    assert move.label == move_label
    assert move.evaluation == evaluation
    assert move.remarks == remarks
    assert move.from_position == pos
    assert move.to_position == next_pos


@pytest.mark.parametrize("move", [
    ("e5"),
    ("Ke2"),
    ("O-O"),
])
def test_invalid_move(move):
    game = Game()
    pos = Position(game, chess.Board())
    with pytest.raises(ValueError):
        _ = pos.make_move(move)


def test_invalid_move_merge():
    game = Game()
    pos = Position(game, chess.Board())
    pos1 = pos.make_move("e4")
    pos2 = pos.make_move("d4")
    moves = list(pos.moves.values())
    with pytest.raises(ValueError):
        moves[0].merge(moves[1])
