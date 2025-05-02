import numpy as np
from typing import Dict, Optional, Tuple, NamedTuple

class Board:
    "Constant values"
    WIDTH = 7
    HEIGHT = 6
    MIN_SCORE = -(WIDTH * HEIGHT) // 2 + 3
    MAX_SCORE = (WIDTH * HEIGHT + 1) // 2 - 3

    def __init__(self):
        "Constructor: init default values"
        self.current_position = np.int64(0)  # current player
        self.mask = np.int64(0)              # both player
        self.moved_step = 0                  # step moved

    @staticmethod
    def bottom(width, height):
        "Create a bit-mask with only 1s in the bottom row"
        result = np.int64(0)
        for col in range(width):
            result |= np.int64(1 << (col * (height + 1)))
        return result
    
    bottom_mask = bottom(WIDTH, HEIGHT) # A bottom bit-mask
    board_mask = bottom_mask * ((1 << HEIGHT) - 1) # A full board mask

    def copy(self):
        "Create a copy of the current board"
        new_board = Board()
        new_board.current_position = self.current_position 
        new_board.mask = self.mask  
        new_board.moved_step = self.moved_step  
        return new_board

    def play(self, move):
        "Play a move by a bit-mask move"
        self.current_position ^= self.mask # Switch player
        self.mask |= move # Make a move
        self.moved_step += 1 # Increase step

    # def play_sequence(self, seq):
    #     "Play using a sequence of input numbers"
    #     for i in range(len(seq)):
    #         column = ord(seq[i]) - ord('1')
    #         if column < 0 or column >= Board.WIDTH or not self.can_play(column) or self.is_winning_move(column):
    #             return i  # used to compare to the len of seq -> fail
    #         self.play_col(column)
    #     return len(seq) # success

    def can_win_next(self):
        "Check if the current player can win on the next move"
        return bool(self.winning_position() & self.possible())

    def nb_moves(self):
        "Step moved"
        return self.moved_step

    def key(self):
        "Unique key of the board -> return a bit-mask"
        return self.current_position + self.mask

    def possible_non_losing_moves(self):
        "Return a bit-mask that has bit 1 where do not lead to a loss on the next turn"
        possible_mask = self.possible() # Possible move at this turn
        opponent_win = self.opponent_winning_position() # # Possible winning moves of the opponent
        forced_moves = possible_mask & opponent_win  # The moves that player must take 
        if forced_moves:
            # If number of forced_moves > 1 -> lose
            if forced_moves & (forced_moves - 1):
                return np.int64(0)  # Lose
            else:
            # You must take this move
                possible_mask = forced_moves
        
        # Eliminate moves that allow the opponent to win
        return possible_mask & ~(opponent_win >> 1)

    def can_play(self, column):
        "Check if a column can played by checking the top position"
        return (self.mask & Board.top_mask_col(column)) == 0

    def play_col(self, column):
        "Play at the column"
        self.play((self.mask + Board.bottom_mask_col(column)) & Board.column_mask(column))

    def is_winning_move(self, column):
        "Check if player play at this column, this player win"
        return bool(self.winning_position() & self.possible() & Board.column_mask(column))

    def winning_position(self):
        "Return a bit-mask that has bit 1 at all position can lead to a winning of current player"
        return Board.compute_winning_position(self.current_position, self.mask)

    def opponent_winning_position(self):
        "Return a bit-mask that has bit 1 at all position can lead to a winning of opponent player"
        return Board.compute_winning_position(self.current_position ^ self.mask, self.mask)

    def possible(self):
        "Return a bit-mask that has bit 1 at valid moves of current player"
        return (self.mask + Board.bottom_mask) & Board.board_mask

    @staticmethod
    def pop_count(m):
        "Count the number of bit 1"
        return bin(m).count('1')

    @staticmethod
    def compute_winning_position(board, mask):
        "Calculate the winning position of current player by bitwise"
        # .xxx and x.xx -> check if x is bit 1 ?
        
        # vertical
        r = (board << 1) & (board << 2) & (board << 3)

        # horizontal .xxx and x.xx
        p = (board << (Board.HEIGHT + 1)) & (board << 2 * (Board.HEIGHT + 1)) 
        r |= p & (board << 3 * (Board.HEIGHT + 1))
        r |= p & (board >> (Board.HEIGHT + 1))
        p = (board >> (Board.HEIGHT + 1)) & (board >> 2 * (Board.HEIGHT + 1))
        r |= p & (board << (Board.HEIGHT + 1))
        r |= p & (board >> 3 * (Board.HEIGHT + 1))

        # left diagonal
        p = (board << Board.HEIGHT) & (board << 2 * Board.HEIGHT)
        r |= p & (board << 3 * Board.HEIGHT)
        r |= p & (board >> Board.HEIGHT)
        p = (board >> Board.HEIGHT) & (board >> 2 * Board.HEIGHT)
        r |= p & (board << Board.HEIGHT)
        r |= p & (board >> 3 * Board.HEIGHT)

        # right diagonal
        p = (board << (Board.HEIGHT + 2)) & (board << 2 * (Board.HEIGHT + 2))
        r |= p & (board << 3 * (Board.HEIGHT + 2))
        r |= p & (board >> (Board.HEIGHT + 2))
        p = (board >> (Board.HEIGHT + 2)) & (board >> 2 * (Board.HEIGHT + 2))
        r |= p & (board << (Board.HEIGHT + 2))
        r |= p & (board >> 3 * (Board.HEIGHT + 2))

        return r & (Board.board_mask ^ mask)
    
    @staticmethod
    def top_mask_col(column):
        "Return a bit-mask that has bit 1 at the top of the column"
        return np.int64(1 << ((Board.HEIGHT - 1) + column * (Board.HEIGHT + 1)))

    @staticmethod
    def bottom_mask_col(column):
        "Return a bit-mask that has bit 1 at the bottom of the column"
        return np.int64(1 << (column * (Board.HEIGHT + 1)))

    @staticmethod
    def column_mask(column):
        "Return a bit-mask that has bit 1 at all position of the column"
        return np.int64((1 << Board.HEIGHT) - 1) << (column * (Board.HEIGHT + 1))

    def print_board(self):
        "print board"
        player_1_pos = np.int64(0)
        player_2_pos = np.int64(0)

        if (self.moved_step % 2) == 0:
            player_1_pos = self.current_position
            player_2_pos = self.current_position ^ self.mask
        else:
            player_1_pos = self.current_position ^ self.mask 
            player_2_pos = self.current_position

        p1_symbol = 'X' 
        p2_symbol = 'O' 

        print("\n  1 2 3 4 5 6 7")
        print(" ---------------")

        for row in range(self.HEIGHT - 1, -1, -1):
            print("|", end=" ")
            for col in range(self.WIDTH):
                pos = np.int64(1 << (row + col * (self.HEIGHT + 1)))

                if not (pos & self.mask): 
                    print(".", end=" ")
                elif pos & player_1_pos:
                    print(p1_symbol, end=" ")
                elif pos & player_2_pos:
                    print(p2_symbol, end=" ")
            print("|") 
        print(" ---------------")

    def has_won(self, player_position):
        "Check if a player has won"
        H = self.HEIGHT
        H1 = H + 1
        
        # Vertical
        y = player_position & (player_position >> 1)
        if y & (y >> 2): return True

        # "Horizontal"
        y = player_position & (player_position >> H1)
        if y & (y >> (2 * H1)): return True

        # Diagonal
        y = player_position & (player_position >> H)
        if y & (y >> (2 * H)): return True

        # Diagonal
        y = player_position & (player_position >> (H + 2))
        if y & (y >> (2 * (H + 2))): return True

        return False 
     
    # def check_winning(self) -> Tuple[Optional[int], Optional[int]]:
    #     "Return true if current board is a terminal non-draw node"
    #     max_win_score = (self.WIDTH * self.HEIGHT + 1 - self.nb_moves()) // 2
    #     min_loss_score = -max_win_score
    #     possible = self.possible()

    #     if self.nb_moves() >= self.WIDTH * self.HEIGHT: 
    #         return 0, None
    #     if possible == 0: 
    #         return 0, None

    #     winning_moves = self.winning_position() & possible
    #     if winning_moves:
    #         win_move = winning_moves & -winning_moves # Lấy nước thắng đầu tiên
    #         return max_win_score, win_move
        
    #     return None, None
