import board
import helper
import config
import pruning
import math
import numpy as np
from mcts import MCTS


my_board = board.Board()
state = my_board.create_new_board()
helper.show(state)

args = {
    'C': 1.41,
    'num_searches':1200
}

mcts = MCTS(my_board, args)

player = 1
while (True):
    # Player
    if player == 1:

        print(f"\nPlayer's turn.")
        valid_moves = my_board.get_valid_action(state)
        # print(f"Valid moves: {valid_moves}")
        action = int(input("Choose a column (1-7): ")) - 1
        while action >= len(valid_moves) or valid_moves[action] == 0:
            print("⚠️ Invalid move. Try again.")
            action = int(input("Choose a column (1–7): ")) - 1
        
        # state = my_board.step(state, action, config.RED_PLAYER)[0]
        # helper.show(state)
    
        # if my_board.evaluate(state) == 1:
        #     print("🎉 Player wins!")
        #     break
        
    # Minimax AI
    # print(f"\nAI's turn.")
    # ai_action = pruning.minimax(state, 5, -math.inf, math.inf, True)[0]
    # state = my_board.step(state, ai_action, config.BLUE_PLAYER)[0]
    # helper.show(state)
    # print(ai_action)

    else: 
        neutral_state = -state
        mcts_probs = mcts.search(state=neutral_state)
        action = np.argmax(mcts_probs)

    state = my_board.get_next_state(state, action, player)
    helper.show(state)
    print(player, "play: ", action + 1)
    value = my_board.evaluate(state)
    is_terminal = my_board.is_terminal_node(state)

    if is_terminal:
        print(state)
        if value == 1:
            print(player, " win")
        elif value == -1:
            print(player, " win")
        else: 
            print("draw")
        break
        

    player = -player
    # if my_board.evaluate(neutral_state) == 1:
    #     print("🎉 AI wins!")
    #     break
        
    # if my_board.is_terminal_node(neutral_state):
    #     print("Draw")
    #     break 
