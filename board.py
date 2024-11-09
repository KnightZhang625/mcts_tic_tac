# coding:utf-8

import random
from typing import Set

PlayerPiece = {
    "Human": True,
    "AI": False,
}

class Node:
    def __init__(self,
                 board = (None, ) * 9,
                 turn = "Human",
                 winner = None,
                 is_terminal = False,
                 is_fully_expanded = False):

        self.board = board
        self.turn = turn
        self.winner = winner
        self.is_terminal = is_terminal
        self.is_fully_expanded = is_fully_expanded

        self.num_visit = 0
        self.value = 0
        self.parent = None
        self.children = {}
    
    def __hash__(self):
        return hash((self.board, self.turn, self.winner, self.is_terminal))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        # Only compare immutable fields
        return (
            self.board == other.board
            and self.turn == other.turn
            and self.winner == other.winner
            and self.is_terminal == other.is_terminal
        )

    @property
    def reward(self):
        if not self.is_terminal:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner is None:
            return 0.5  # Board is a tie
        if self.turn == self.winner:
            return 1.0
        # 不存在 self.turn != self.winner, 因为:
        # 假设这一步棋Human走的, 胜者绝不会是AI, 否则的话AI之前就赢了

def find_children(node: Node) -> Set[Node]:
    if node.is_terminal:
        return set()
    next_player = "AI" if node.turn == "Human" else "Human"
    return {
        make_move(node.board, next_player, i) for i, v in enumerate(node.board) if v is None
    }

def find_random_child(node: Node) -> Node:
    if node.is_terminal:
        raise RuntimeError(f"Cannot be here")
    empty_spots = [i for i, v in enumerate(node.board) if v is None]
    next_player = "AI" if node.turn == "Human" else "Human"
    return make_move(node.board, next_player, random.choice(empty_spots))

def make_move(board: tuple, player: str, idx: int) -> Node:
    new_board = board[:idx] + (PlayerPiece[player], ) + board[idx+1:]
    winner = find_winner(new_board)
    is_terminal = (winner is not None) or not any(v is None for v in new_board)
    return Node(board=new_board, turn=player, winner=winner, is_terminal=is_terminal)

def find_winner(board):
        """
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
            0 1 2
            3 4 5
            6 7 8
        """
        def _row_col_diagnol():
            for row in range(0, 9, 3):  # (0,1,2),(3,4,5),(6,7,8)
                yield (row, row+1, row+2)
            for col in range(3):
                yield (col, col+3, col+6)
            yield (0, 4, 8)
            yield (2, 4, 6)
        
        for i1, i2, i3 in _row_col_diagnol():
            v1, v2, v3 = board[i1], board[i2], board[i3]
            if False is v1 is v2 is v3:
                return "AI"
            if True is v1 is v2 is v3:
                return "Human"
        return None

def to_pretty_string(node: Node):
    to_char = lambda v: ("X" if v is True else ("O" if v is False else " "))
    rows = [
        [to_char(node.board[3 * row + col]) for col in range(3)] for row in range(3)
    ]
    return (
        "\n  1 2 3\n"
        + "\n".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))
        + "\n"
    )

node = Node()