import config
import numpy as np
from scipy.signal import convolve2d

class Board:
    def __init__(self):
        self.rows = config.BOARD_ROWS
        self.columns = config.BOARD_COLUMNS
        
    def create_new_board(self):

        "Create a board."
        return self.reset()
        
    def reset(self):
        "Reset the board."
        return np.zeros([self.rows, self.columns], dtype=np.int8)
        
    def get_valid_action(self, state):
        "Return an array containing the indices of valid actions."
        return (state[0] == 0).astype(np.uint8)
        
    def get_next_state(self, state, action, player=config.RED_PLAYER):
        "Return a state after execute an action."
        row = np.max(np.where(state[:, action] == 0)[0]) 
        new_state = state.copy()
        new_state[row, action] = player  # Place player's move
        return new_state
    
    def evaluate(self, state):
        "Evaluate the current state. Return 1 for RED win, -1 for BlUE win and 0 otherwise."
        # Create a filter kernel for checking horizontal and vertical
        filter_kernel = np.ones((1, 4), dtype=int)
        
        # Horizontal
        horizontal_check = convolve2d(state, filter_kernel, mode='valid')
        
        # Vertical
        vertical_check = convolve2d(state, filter_kernel.T, mode='valid')
        
        # Create a filter kernel for checking diagonal 
        diagonal_filter_kernel = np.eye(4, dtype=int)
        
        # Diagonal
        main_diagonal_check = convolve2d(state, diagonal_filter_kernel, mode='valid')
        anti_diagonal_check = convolve2d(state, np.fliplr(diagonal_filter_kernel), mode='valid')
        
        # Check for RED win
        result = [horizontal_check, vertical_check, main_diagonal_check, anti_diagonal_check]
        if any(np.any(check == 4) for check in result):
            return 1
        elif any(np.any(check == -4) for check in result):
            return -1
        return 0


    def step(self, state, action, player=config.RED_PLAYER):
        "Call self.get_next_state() and self.evaluate() to return next state and done flag."

        # Get next state and its score
        next_state = self.get_next_state(state, action, player)
        if next_state is None:
            return None, None, None
        
        game_result = self.evaluate(state)
        
        flag = False
        if game_result != 0 or np.sum(abs(next_state)) == (self.columns * self.rows):
            flag = True
        
        return next_state, game_result, flag
        
    def flip(self, state):
        return  -state
    
    def is_terminal_node(self, state):
        "Return True if the current state is the end state."
        return self.evaluate(state) in [-1, 1] or sum(self.get_valid_action(state)) == 0

    
    def get_encoded_state(self, state):
        "Encode the state into 3 layer."
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)
        
        return encoded_state
    
    
    
    
    
    
    
    
    
    
    
    
    