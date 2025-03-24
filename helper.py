import numpy as np

class helper():
    
    @staticmethod
    def print(state):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in state]))
        
    
