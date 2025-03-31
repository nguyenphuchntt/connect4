import numpy as np
import config


def show(state):
    for row in state:
        print(" ".join(f"{num:4}" for num in row))
