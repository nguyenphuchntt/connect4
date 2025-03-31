import board
import helper
import config
import alphabeta
import math
import time


my_board = board.Board()
state = my_board.create_new_board()
helper.show(state)


while (True):
    # Player
    print(f"\nPlayer's turn.")
    valid_moves = my_board.get_valid_action(state)
    print("Valid moves", [i for i in range(7) if valid_moves[i] == 1])
    action = int(input("Choose a valid column: "))
    while action >= 7 or valid_moves[action] == 0:
        print("⚠️ Invalid move. Try again.")
        action = int(input("Choose a valid column : "))
    
    state = my_board.get_next_state(state, action, config.RED_PLAYER)
    helper.show(state)
    
    if my_board.evaluate(state) == 1:
        print("🎉 Player wins!")
        break
        
    # Minimax AI
    start_time = time.time()
    print(f"\nAI's turn.")
    ai_action = alphabeta.minimax(state, 7, -math.inf, math.inf, True)[0]
    state = my_board.get_next_state(state, ai_action, config.BLUE_PLAYER)
    helper.show(state)
    print(ai_action)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.4f} seconds")

    if my_board.evaluate(state) == -1:
        print("🎉 AI wins!")
        break
    
    if my_board.is_terminal_node(state):
        print("Draw")
        break 

