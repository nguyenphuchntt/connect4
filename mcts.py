from board import Board
import numpy as np
import config
import math

board = Board()  

class Node:
    def __init__(self, board: Board, args, state, parent=None, action_taken=None):
        self.board = board
        self.state = state
        self.args = args
        self.parent = parent
        self.action_taken = action_taken

        self.children = []
        self.expandable_moves = board.get_valid_action(state)

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self):
        return np.sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf
        for child in self.children:
            ucb = self.get_ucb(child)
            if (ucb > best_ucb):
                best_ucb = ucb
                best_child = child
        return best_child
    
    def get_ucb(self, child):
        if (child.visit_count == 0):
            return np.inf
        else:
            q_sa = 1 - ((child.value_sum/child.visit_count) + 1 ) / 2
        
        return q_sa + self.args['C']*math.sqrt(math.log(self.visit_count)/child.visit_count)
        

    def expand(self):
        "Get the next state and flip"
        action = np.random.choice(np.where(self.expandable_moves == 1)[0])
        self.expandable_moves[action] = 0
        child_state = self.state.copy()
        child_state = self.board.get_next_state(child_state, action, config.RED_PLAYER)
        child_state = self.board.flip(child_state)
        child = Node(self.board, self.args, child_state, self, action)
        self.children.append(child)
        return child
    
    def simulate(self):
        value = self.board.evaluate(self.state)
        is_terminal = self.board.is_terminal_node(self.state)

        if (is_terminal):
            return value
        
        rollout_state = self.state.copy()
        rollout_player = 1
        while True:
            valid_moves = self.board.get_valid_action(rollout_state)
            action = np.random.choice(np.where(valid_moves == 1)[0])
            rollout_state = self.board.get_next_state(rollout_state, action, rollout_player)
            value = self.board.evaluate(rollout_state)
            is_terminal = self.board.is_terminal_node(rollout_state)
            if is_terminal:
                return value
            
            rollout_player = -rollout_player

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)

class MCTS:
    def __init__(self, board:Board, args):
        self.board = board
        self.args = args

    def search(self, state):
        root = Node(self.board, self.args, state)
        #define root
        for search in range(self.args['num_searches']):
            #selection
            node = root
            while node.is_fully_expanded():
                node = node.select()
            value = self.board.evaluate(node.state)
            is_terminal = self.board.is_terminal_node(node.state)

            if not is_terminal:
                #expansion
                node = node.expand()
                #simulation or let it through network
                value = node.simulate()
            #backup
            node.backpropagate(value)
        action_probs = np.zeros(config.BOARD_COLUMNS)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs