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
    valid_moves = my_board.get_valid_action(state)
    print(f"Valid moves: {valid_moves}")
    action = int(input("Choose a column (0–6): "))
    while action not in valid_moves:
        print("⚠️ Invalid move. Try again.")
        action = int(input("Choose a column (0–6): "))
    
    state = my_board.step(state, action, config.PLAYER_PIECE)
    helper.show(state)
    
    if my_board.winning_state(state, config.PLAYER_PIECE):
        print("🎉 Player wins!")
        break
        
    # Minimax AI
    print(f"\nAI's turn.")
    ai_action = pruning.minimax(state, 5, -math.inf, math.inf, True)[0]
    state = my_board.step(state, ai_action, config.AI_PIECE)
    helper.show(state)

    if my_board.winning_state(state, config.AI_PIECE):
        print("🎉 AI wins!")
        break
    
    

    if my_board.is_terminal_node(state):
        print("Draw")
        break 