import numpy as np
import config


def show(state):
    for row in state:
        print(" ".join(f"{num:4}" for num in row))

def get_input(x):
    try: 
        input = int(x) - 1
    except ValueError:
        print("Invalid input! Try again")
        return None

    if (input >= config.BOARD_COLUMNS or input < 0):
        print("Invalid input! Try again")
        return None
    print(input)
    return input
