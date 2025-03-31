import config
import board
import numpy as np
import math
import random

my_board = board.Board()

def evaluate_window(window, piece):
    "The score for each case of window slide."
    score = 0
    opp_piece = config.RED_PLAYER
    if piece == config.RED_PLAYER:
        opp_piece = config.BLUE_PLAYER

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(config.EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(config.EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(config.EMPTY) == 1:
        score -= 4

    return score


def score_position(state, piece):
    "Sliding window to calculate the score of the current state."
    score = 0

    ## Score center column (The center column is critical to all non-vertical wins)
    center_array = [int(i) for i in list(state[:, config.BOARD_COLUMNS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(config.BOARD_ROWS):
        row_array = [int(i) for i in list(state[r,:])]
        for c in range(config.BOARD_COLUMNS-3):
            window = row_array[c:c+config.WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(config.BOARD_COLUMNS):
        col_array = [int(i) for i in list(state[:,c])]
        for r in range(config.BOARD_ROWS-3):
            window = col_array[r:r+config.WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score diagonal
    for r in range(config.BOARD_ROWS-3):
        for c in range(config.BOARD_COLUMNS-3):
            window = [state[r+i][c+i] for i in range(config.WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(config.BOARD_ROWS-3):
        for c in range(config.BOARD_COLUMNS-3):
            window = [state[r+3-i][c+i] for i in range(config.WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score



def minimax(state, depth, alpha, beta, maximizingPlayer):
    "Minimax pruning algorithm"
    valid_locations = my_board.get_valid_action(state)
    is_terminal = my_board.is_terminal_node(state)
    if depth == 0 or is_terminal:
        if is_terminal:
            if my_board.evaluate(state) == -1:
                return (None, 100000000000000)
            elif my_board.evaluate(state) == 1:
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(state, config.BLUE_PLAYER))
        
    # Maximizing for AI
    if maximizingPlayer:
        value = -math.inf
        action = random.choice(valid_locations)
        for act in valid_locations:
            temp_state = my_board.step(state, act, config.BLUE_PLAYER)[0]
            new_score = minimax(temp_state, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                action = act
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return action, value

    # Minimizing for player
    else: 
        value = math.inf
        action = random.choice(valid_locations)
        for act in valid_locations:
            temp_state = my_board.step(state, act, config.RED_PLAYER)[0]
            new_score = minimax(temp_state, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                action = act
            beta = min(beta, value)
            if alpha >= beta:
                break
        return action, value