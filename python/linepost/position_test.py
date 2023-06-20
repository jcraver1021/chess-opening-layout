import chess
import pytest
import linepost.position as lppos

@pytest.mark.parametrize("line1,line2", [
    ("e4", "d4"),
    ("e4", "e4 e5"),
])
def test_invalid_lines(line1, line2):
    def split_tokens(line):
        position = lppos.Position(chess.Board())
        for token in line.split():
            position = position.make_move(token)
        return position
    
    pos1 = split_tokens(line1)
    pos2 = split_tokens(line2)
    
    with pytest.raises(ValueError):
        pos1.merge(pos2)
    
    with pytest.raises(ValueError):
        pos2.merge(pos1)