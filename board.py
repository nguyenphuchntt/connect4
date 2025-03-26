import config
import numpy as np
import math
import random
from scipy.signal import convolve2d

class Board:
    def __init__(self):
        self.rows = config.BOARD_ROWS
        self.cols = config.BOARD_COLUMNS
        
    def create_new_board(self):
        "Create new board."
        return self.reset()
        
    def reset(self):
        "Reset the board."
        return np.zeros([self.rows, self.cols], dtype=np.int8)
        
    def get_valid_action(self, state):
        "Return a numpy array containing the indices of valid actions."
        if self.winning_state(state, config.AI_PIECE) or self.winning_state(state, config.PLAYER_PIECE):
            return np.array([])
        
        # Calculate sum in vertical
        cols = np.sum(np.abs(state), axis=0)
        return np.where(cols < self.rows)[0]
        
    
    def winning_state(self, state, piece):
        "Evaluate the current position. Returns True if this piece win"
        # Create a filter kernel for checking horizontal and vertical
        filter_kernel = np.ones((1, 4), dtype=int)
        
        # Horizontal & Vertical
        horizontal_check = convolve2d(state, filter_kernel, mode='valid')
        vertical_check = convolve2d(state, filter_kernel.T, mode='valid')
        
        # Create a filter kernel for checking diagonal 
        diagonal_filter_kernel = np.eye(4, dtype=int)
        
        # Diagonal
        main_diagonal_check = convolve2d(state, diagonal_filter_kernel, mode='valid')
        anti_diagonal_check = convolve2d(state, np.fliplr(diagonal_filter_kernel), mode='valid')
        
        # Check for RED win
        result = [horizontal_check, vertical_check, main_diagonal_check, anti_diagonal_check]
        if any(np.any(check == 4 * piece) for check in result):
            return True
        return False

    def get_next_state(self, state, action, piece):
        "Return a state after execute an action"
        # Game is over
        if self.winning_state(state, piece): return None
        
        # Board is full
        if np.sum(abs(state)) == self.rows * self.cols: return None
        
        # Invalid actions
        if action not in self.get_valid_action(state): return None
        
        # Identify the next empty row in the action's row
        row = np.where(state[:, action] == 0)[0][-1] # Go through all positions at action's column and get the last position
        
        # Execute the action
        new_state = state.copy()
        new_state[row, action] = piece
        return new_state
     
        
    def step(self, state, action, piece):
        "Play an action in a given state. Return the next_state, reward and done flag."
        # Get next state and its score
        next_state = self.get_next_state(state, action, piece)
        if next_state is None:
            return None, None, None
        return next_state
    

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = config.PLAYER_PIECE
        if piece == config.PLAYER_PIECE:
            opp_piece = config.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(config.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(config.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(config.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, state, piece):
        "Score function."
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(state[:, self.cols//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(state[r,:])]
            for c in range(self.cols-3):
                window = row_array[c:c+config.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.cols):
            col_array = [int(i) for i in list(state[:,c])]
            for r in range(self.rows-3):
                window = col_array[r:r+config.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score diagonal
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                window = [state[r+i][c+i] for i in range(config.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.rows-3):
            for c in range(self.cols-3):
                window = [state[r+3-i][c+i] for i in range(config.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score



    def is_terminal_node(self, state):
        "Return True if the current state is the end state."
        return self.winning_state(state, config.PLAYER_PIECE) or self.winning_state(state, config.AI_PIECE) or len(self.get_valid_action(state)) == 0



    def minimax(self, state, depth, alpha, beta, maximizingPlayer):
        "Minimax pruning algorithm"
        valid_locations = self.get_valid_action(state)
        is_terminal = self.is_terminal_node(state)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_state(state, config.AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_state(state, config.PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(state, config.AI_PIECE))
            
        if maximizingPlayer:
            value = -math.inf
            action = random.choice(valid_locations)
            for act in valid_locations:
                temp_state = self.step(state, act, config.AI_PIECE)
                new_score = self.minimax(temp_state, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    action = act
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return action, value

        else: 
            value = math.inf
            action = random.choice(valid_locations)
            for act in valid_locations:
                temp_state = self.step(state, act, config.PLAYER_PIECE)
                new_score = self.minimax(temp_state, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    action = act
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return action, value
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    