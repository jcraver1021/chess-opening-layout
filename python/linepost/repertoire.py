# Linepost rep

import chess
import graphviz

if False:
    graphviz.set_jupyter_format('png')

colors = {
    "??": "red",
    "?": "orange",
    "?!": "yellow",
    "!!": "cyan",
    "!": "blue"
}


def parse_move(move):
    components = move.split(';')
    label = components[0]
    color = "black"
    remarks = []
    for assessment in colors:
        if label.endswith(assessment):
            color = colors[assessment]
            label = label.replace(assessment, '')
    if len(components) >= 2:
        remarks = [remark for remark in components[1:]]
    return label, color, remarks


def label_move(move, new_turn, move_no):
    if new_turn:
        return f'{move_no}. {move}', False, move_no
    return f'..{move}', True, move_no + 1


class Repertoire:
    def __init__(self, name="Opening Repertoire"):
        self.name = name
        self.graph = graphviz.Digraph(name=name, graph_attr={'rankdir':'LR'})
        self.positions = {}  # map of FENs to chess positions
        self.edges = set()
        self.starting_position = chess.Board()
        self._add_position(self.starting_position, "Start")

    def _add_position(self, position, label, color="black"):
        fen = position.fen()
        self.graph.node(fen, label=label, color=color)
        self.positions[fen] = position

    def _connect(self, fen1, fen2):
        edge = (fen1, fen2)
        if edge not in self.edges:
          self.graph.edge(*edge)
          self.edges.add(edge)
  
    def _annotate(self, fen, remark):
        self.graph.node(remark, color="gray")
        self._connect(remark, fen)

    def add_line(self, moves):
        last_pos = None
        new_turn = True
        move_no = 1
        for move_entry in moves.split():
            if last_pos is None:
                last_pos = self.starting_position
            next_pos = last_pos.copy()
            move, color, remarks = parse_move(move_entry)
            next_pos.push_san(move)
            move, new_turn, move_no = label_move(move, new_turn, move_no)
            self._add_position(next_pos, move, color)
            self._connect(last_pos.fen(), next_pos.fen())
            for remark in remarks:
                self._annotate(next_pos.fen(), remark)
            last_pos = next_pos

    def draw(self):
        return self.graph