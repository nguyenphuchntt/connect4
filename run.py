import board
import helper
import config

# test
my_board = board.Board()
state = my_board.create_new_board()
helper.show(state)

player = config.RED_PLAYER
while (True):
    my_input = helper.get_input(input())
    if my_input is None:
        break
    
    state = my_board.step(state, my_input, player)[0]
    if state is None:
        break
    
    helper.show(state)
    if (my_board.evaluate(state) != 0):
        break
    
    if player == config.RED_PLAYER:
        player = config.BLUE_PLAYER
    else:
        player = config.RED_PLAYER    