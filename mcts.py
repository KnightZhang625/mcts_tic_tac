# coding:utf-8

import math
import random

from board import Node
from board import find_children, find_random_child

class MCTS:
    def __init__(self, cur_node: Node):
        self.root = cur_node
        self.weight = 1
    
    def rollout(self):
        # select a unexplored node
        node = self.select_node(self.root)
        # simulate: 没事走两步
        reward = self.simulate(node)
        # backpropogate
        self.backpropogate(node, reward)
    
    def select_node(self, node: Node) -> Node:
        while not node.is_terminal:
            if not node.is_fully_expanded:
                return self.expand_node(node)
            else:
                node = self.select_best_child(node)
        return node
            
    def expand_node(self, node: Node):
        children = find_children(node)
        for child_node in children:
            if child_node not in node.children:
                child_node.parent = node
                node.children[child_node] = None
                if len(node.children) == len(children):
                    node.is_fully_expanded = True
                return child_node

    def select_best_child(self, node: Node):
        def cal_score(node: Node):
            return node.value / node.num_visit + self.weight * math.sqrt(
                math.log(node.parent.num_visit) / node.num_visit
            )
    
        best_value = float("-inf")
        best_nodes = []
        for child_node in node.children:
            score = cal_score(child_node)
            if score > best_value:
                best_value = score
                best_nodes = [child_node]
            elif score == best_value:
                best_nodes.append(child_node)
        
        return random.choice(best_nodes)

    def simulate(self, node: Node):
        start_node_player = node.turn
        while True:
            if node.is_terminal:
                reward = node.reward
                end_node_player = node.turn

                if start_node_player == end_node_player:
                    return reward
                elif start_node_player != end_node_player:
                    return 1 - reward
            
            node = find_random_child(node)
    
    def backpropogate(self, node: Node, reward: float):
        while node != None:
            node.num_visit +=1
            node.value +=reward
            node = node.parent
            reward = 1 - reward