import board
import helper
import time
import numpy as np
import alphabeta
from mcts import MCTS
import math


my_board = board.Board()
state = my_board.create_new_board()
helper.show(state)

args = {
    'C': 1.41,
    'num_searches':1200
}

mcts = MCTS(my_board, args)

player = 1

remaining = 42
while (True):
    remaining = remaining - 1
    # Player
    if player == 1:
        print(f"\nPlayer's turn.")
        valid_moves = my_board.get_valid_action(state)
        print("Valid moves", [i+1 for i in range(7) if valid_moves[i] == 1])
        action = int(input("Choose a column: ")) - 1
        while action >= len(valid_moves) or action < 0 or valid_moves[action] == 0:
            print("⚠️ Invalid move. Try again.")
            action = int(input("Choose a column: ")) - 1
    else:         
        print(f"\nAI's turn.")
        start_time = time.time()
        if (remaining < 30):
            action = alphabeta.minimax(state, 7, -math.inf, math.inf, True)[0]
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution Time: {execution_time:.4f} seconds in minimax")
        else:
            neutral_state = -state
            mcts_probs = mcts.search(state=neutral_state)
            action = np.argmax(mcts_probs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution Time: {execution_time:.4f} seconds in MCTS")

    state = my_board.get_next_state(state, action, player)
    helper.show(state)
    print(player, "play: ", action + 1)
    value = my_board.evaluate(state)
    is_terminal = my_board.is_terminal_node(state)

    if is_terminal:
        print(state)
        if value == 1:
            print("Player win")
        elif value == -1:
            print("AI win")
        else: 
            print("draw")
        break
        

    player = -player 
