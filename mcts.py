from board import Board
import numpy as np
import config
import math
import torch

board = Board()  

class Node:
    def __init__(self, board: Board, state, parent=None, action_taken=None, prior=0, visit_count=0):
        self.board = board
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        self.children = []

        self.visit_count = visit_count
        self.value_sum = 0

    def is_fully_expanded(self):
        "Retrurn true if the node cannot be expanded anymore."
        return len(self.children) > 0

    def select(self):
        "Consider the ucb rate of each children node to get the one with the best ucb rate."
        best_child = None
        best_ucb = -np.inf
        for child in self.children:
            ucb = self.get_ucb(child)
            if (ucb > best_ucb):
                best_ucb = ucb
                best_child = child
        return best_child
    
    def get_ucb(self, child):
        "Calculate the ucb value. This function is a bit different compare with normal MCTs ucb."
        if child.visit_count == 0:
            q_sa = 0
        else:
            q_sa = 1 - ((child.value_sum/child.visit_count) + 1 ) / 2
        
        return q_sa + config.C_PUCT*(math.sqrt(self.visit_count)/(child.visit_count +1))*child.prior
        

    def expand(self, policy):
        "No more expanding each child. All children is now expanded at the same time using policy."
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()
                child_state = self.board.get_next_state(child_state, action, config.RED_PLAYER)
                child_state = self.board.flip(child_state)
                child = Node(self.board, child_state, self, action, prob)
                self.children.append(child)

        return child
    

    def backpropagate(self, value):
        "Backpropation step."
        self.value_sum += value
        self.visit_count += 1

        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)

class MCTS:
    "MCTs basically has 4 moves: Tree traversal, Node expansion, Rollout (random simulation) and Backpropagation"
    def __init__(self, board:Board, model):
        self.board = board
        self.model = model

    @torch.no_grad
    def search(self, state):
        root = Node(self.board, state, visit_count=1)
        
        policy, _ = self.model(
            torch.tensor(self.board.get_encoded_state(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        
        # Adding dirichlet noise to the old policy at first
        # Basically we want to explore more, move in some directions we maybe haven't checked before, 
        # just make sure we don't miss on any possible promising action
        # as at the begining our model doesn't know that much about the game 
        policy = (1-config.DIRICHLET_EPSILON) * policy + config.DIRICHLET_EPSILON \
                * np.random.dirichlet([config.DIRICHLET_ALPHA]) * config.ACTION_SIZE
        valid_moves = self.board.get_valid_action(state)
        policy *= valid_moves
        policy /= np.sum(policy)

        # We expand but dont backpropagate immedately, so our root node will have childre
        # but visit_count of root node still 0. That's mean when we select in the for loop, 
        # the get_ucb function make no sense. That's why we set visit_count = 1 at first.
        root.expand(policy)

        for _ in range(config.N_SEARCHES):
            # Selection
            node = root
            while node.is_fully_expanded():
                node = node.select()

            value = self.board.evaluate(node.state)
            is_terminal = self.board.is_terminal_node(node.state)

            if not is_terminal:
                policy, value = self.model(
                    # Convert the encoded 3 layer data into tensor and add Batch dimension
                    torch.tensor(self.board.get_encoded_state(node.state), device=self.model.device).unsqueeze(0)
                )
                # We got policy head, normalized it by using softmax
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.board.get_valid_action(node.state)
                policy *= valid_moves
                policy /= np.sum(policy)
            
                value = value.item()

                node = node.expand(policy)
           
            # Backup
            node.backpropagate(value)

        # An array of action probability will be returned
        action_probs = np.zeros(config.ACTION_SIZE)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs