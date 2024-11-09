# coding:utf-8

from board import Node, make_move, to_pretty_string
from mcts import MCTS

def play_game():
    node = Node()
    print(to_pretty_string(node))

    while True:
        row_col = input("enter row,col: ")
        row, col = map(int, row_col.split(","))
        index = 3 * (row - 1) + (col - 1)
        if node.board[index] is not None:
            raise RuntimeError("Invalid move")
        node = make_move(node.board, player="Human", idx=index)
        print(to_pretty_string(node))

        if node.is_terminal:
            break
        
        # You can train as you go, or only at the beginning.
        # Here, we train as we go, doing fifty rollouts each turn.
        tree = MCTS(node)

        for _ in range(500):
            tree.rollout()

        node = tree.select_best_child(node)
        print(to_pretty_string(node))
        if node.is_terminal:
            break
    
if __name__ == "__main__":
    play_game()