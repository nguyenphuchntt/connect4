import board
import helper
import config
import pruning
import math


my_board = board.Board()
state = my_board.create_new_board()
helper.show(state)


while (True):
    # Player
    print(f"\nPlayer's turn.")
    valid_moves = my_board.get_valid_action(state) + 1
    print(f"Valid moves: {valid_moves}")
    action = int(input("Choose a column (1-7): ")) - 1
    while action not in valid_moves - 1:
        print("⚠️ Invalid move. Try again.")
        action = int(input("Choose a column (1–7): "))
    
    state = my_board.step(state, action, config.RED_PLAYER)[0]
    helper.show(state)
    
    if my_board.evaluate(state) == 1:
        print("🎉 Player wins!")
        break
        
    # Minimax AI
    print(f"\nAI's turn.")
    ai_action = pruning.minimax(state, 5, -math.inf, math.inf, True)[0]
    state = my_board.step(state, ai_action, config.BLUE_PLAYER)[0]
    helper.show(state)
    print(ai_action)

    if my_board.evaluate(state) == -1:
        print("🎉 AI wins!")
        break
    
    if my_board.is_terminal_node(state):
        print("Draw")
        break 

