
class MoveSorter:
    "Sort the moves by score, similar to a priority queue, to select the move with the best value."
    
    def __init__(self, board_width):
        "Constructor: init default values"
        self.size = 0
        self.board_width = board_width
        self.entries = [{'move': 0, 'score': 0} for _ in range(board_width)]
    
    def add(self, move, score):
        "Add a move and its score value"
        move = int(move)
        pos = self.size
        self.size += 1
        
        "Add by insertion sort"
        while pos > 0 and self.entries[pos-1]['score'] > score:
            self.entries[pos] = self.entries[pos-1].copy()
            pos -= 1
        
        self.entries[pos] = {'move': move, 'score': score}

    def getNext(self):
        "Return the next move (with the highest score) or return 0 if no moves are left."
        if self.size > 0:
            self.size -= 1
            return self.entries[self.size]['move']
        else:
            return 0
    
    def reset(self):
        "Reset the queue"
        self.size = 0