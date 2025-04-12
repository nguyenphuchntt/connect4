import numpy as np
# https://claude.ai/chat/96d24bca-3a27-417b-a9b8-a2f90585fb80

# * A class storing a Connect 4 Board.
# * Functions are relative to the current player to play.
# * Board containing aligment are not supported by this class.
# *
# * A binary bitboard representationis used.
# * Each column is encoded on HEIGH+1 bits.
# * 
# * Example of bit order to encode for a 7x6 board
# * .  .  .  .  .  .  .
# * 5 12 19 26 33 40 47
# * 4 11 18 25 32 39 46
# * 3 10 17 24 31 38 45
# * 2  9 16 23 30 37 44
# * 1  8 15 22 29 36 43
# * 0  7 14 21 28 35 42 
# * 
# * Board is stored as
# * - a bitboard "mask" with 1 on any color stones
# * - a bitboard "current_player" with 1 on stones of current player
# *
# * "current_player" bitboard can be transformed into a compact and non ambiguous key
# * by adding an extra bit on top of the last non empty cell of each column.
# * This allow to identify all the empty cells whithout needing "mask" bitboard
# *
# * current_player "x" = 1, opponent "o" = 0
# * board     Board  mask      key       bottom
# *           0000000   0000000   0000000   0000000
# * .......   0000000   0000000   0001000   0000000
# * ...o...   0000000   0001000   0010000   0000000
# * ..xx...   0011000   0011000   0011000   0000000
# * ..ox...   0001000   0011000   0001100   0000000
# * ..oox..   0000100   0011100   0000110   0000000
# * ..oxxo.   0001100   0011110   1101101   1111111
# *
# * current_player "o" = 1, opponent "x" = 0
# * board     Board  mask      key       bottom
# *           0000000   0000000   0001000   0000000
# * ...x...   0000000   0001000   0000000   0000000
# * ...o...   0001000   0001000   0011000   0000000
# * ..xx...   0000000   0011000   0000000   0000000
# * ..ox...   0010000   0011000   0010100   0000000
# * ..oox..   0011000   0011100   0011010   0000000
# * ..oxxo.   0010010   0011110   1110011   1111111
# *
# * key is an unique representation of a board key = Board + mask + bottom
# * in practice, as bottom is constant, key = Board + mask is also a 
# * non-ambigous representation of the Board.

# Sau khi đã định nghĩa lớp đầy đủ


class Board:
    WIDTH = 7
    HEIGHT = 6
    MIN_SCORE = -(WIDTH * HEIGHT) // 2 + 3
    MAX_SCORE = (WIDTH * HEIGHT + 1) // 2 - 3


    def __init__(self):
        "Khởi tạo bàn cờ Connect 4 trống"
        self.current_position = np.int64(0)  # vị trí của người chơi hiện tại
        self.mask = np.int64(0)              # mặt nạ chung (cả hai người chơi)
        self.moved_step = 0                  # số nước đã đi

    @staticmethod
    def bottom(width, height):
        "Tạo bit mask với hàng dưới cùng chứa chỉ các bit 1"
        result = np.int64(0)
        for col in range(width):
            result |= np.int64(1 << (col * (height + 1)))
        return result
    
    @staticmethod
    def top_mask_col(column):
        "Trả về bit mask với 1 bit tại ô trên cùng của cột"
        return np.int64(1 << ((Board.HEIGHT - 1) + column * (Board.HEIGHT + 1)))

    @staticmethod
    def bottom_mask_col(column):
        "Trả về bit mask với 1 bit tại ô dưới cùng của cột"
        return np.int64(1 << (column * (Board.HEIGHT + 1)))

    @staticmethod
    def column_mask(column):
        "Trả về bit mask với các bit 1 trên toàn bộ cột"
        return np.int64((1 << Board.HEIGHT) - 1) << (column * (Board.HEIGHT + 1))

    def copy(self):
        "Tạo bản sao hoàn chỉnh của bàn cờ hiện tại"
        new_board = Board()
        new_board.current_position = self.current_position 
        new_board.mask = self.mask  
        new_board.moved_step = self.moved_step  
        return new_board

    def play(self, move):
        "Thực hiện một nước đi"
        self.current_position ^= self.mask  # Đảo người chơi hiện tại bằng phép XOR với mask
        self.mask |= move                   # Thêm nước đi vào mask
        self.moved_step += 1


    def play_sequence(self, seq):
        "Thực hiện chơi với một chuỗi seq số được nhập vào"
        for i in range(len(seq)):
            column = ord(seq[i]) - ord('1')
            if column < 0 or column >= Board.WIDTH or not self.can_play(column) or self.is_winning_move(column):
                if not self.can_play(column):
                    print("cant play")
                if self.is_winning_move(column):
                    print("winning move")
                return i  # trả về số nước đã đi
            self.play_col(column)
        return len(seq)

    def can_win_next(self):
        "Kiểm tra nếu người chơi hiện tại có thể thắng trong nước tiếp theo"
        return bool(self.winning_position() & self.possible())

    def nb_moves(self):
        "Trả về số nước đã đi"
        return self.moved_step

    def key(self):
        "Tạo key trạng thái bàn cờ"
        return self.current_position + self.mask

    def key3(self):
        "Tạo khóa duy nhất theo cơ số 3"
        key_forward = np.int64(0)
        for i in range(Board.WIDTH):
            self._partial_key3(key_forward, i)  # tính khóa theo thứ tự tăng dần của cột

        key_reverse = np.int64(0)
        for i in range(Board.WIDTH - 1, -1, -1):
            self._partial_key3(key_reverse, i)  # tính khóa theo thứ tự giảm dần của cột

        # lấy khóa nhỏ hơn và chia cho 3
        return min(key_forward, key_reverse) // 3

    def _partial_key3(self, key, col):
        "Tính phần khóa cơ số 3 cho một cột"
        pos = np.int64(1 << (col * (Board.HEIGHT + 1)))
        while pos & self.mask:
            key *= 3
            if pos & self.current_position:
                key += 1
            else:
                key += 2
            pos <<= 1
        key *= 3

    def possible_non_losing_moves(self):
        "Trả về các nước đi không dẫn đến thua trong lượt sau đó"
        assert not self.can_win_next()
        possible_mask = self.possible()
        opponent_win = self.opponent_winning_position()
        forced_moves = possible_mask & opponent_win # Nước bắt buộc đi để đối thủ không thắng
        
        if forced_moves:
            # Kiểm tra xem có nhiều hơn 1 nước đi bắt buộc không (nước đôi)
            if forced_moves & (forced_moves - 1):
                return np.int64(0)  # thua 
            else:
                possible_mask = forced_moves  # phải đi nước này
        
        # Loại bỏ các nước đi tạo điều kiện cho đối thủ thắng
        return possible_mask & ~(opponent_win >> 1)

    def move_score(self, move):
        "Tính score cho một nước đi = số vị trí thắng"
        return Board.pop_count(Board.compute_winning_position(self.current_position | move, self.mask))

    def can_play(self, column):
        "Kiểm tra cột có thể chơi được không"
        # Ô trên cùng chưa được sử dụng, có thể chơi
        return (self.mask & Board.top_mask_col(column)) == 0

    def play_col(self, column):
        "Thực hiện nước đi tại một cột"
        self.play((self.mask + Board.bottom_mask_col(column)) & Board.column_mask(column))

    def is_winning_move(self, column):
        "Kiểm tra nước đi có dẫn đến thắng không"
        return bool(self.winning_position() & self.possible() & Board.column_mask(column))

    def winning_position(self):
        "Tính vị trí thắng cho người chơi hiện tại"
        return Board.compute_winning_position(self.current_position, self.mask)

    def opponent_winning_position(self):
        "Tính vị trí thắng cho đối thủ"
        return Board.compute_winning_position(self.current_position ^ self.mask, self.mask)

    def possible(self):
        "Tính toán các nước đi hợp lệ"
        return (self.mask + Board.bottom_mask) & Board.board_mask

    @staticmethod
    def pop_count(m):
        "Đếm số bit 1 trong một số."
        return bin(m).count('1')

    @staticmethod
    def compute_winning_position(board, mask):
        "Tính toán tất cả vị trí thắng có thể"
        # Kiểm tra chiến thắng theo chiều dọc
        r = (board << 1) & (board << 2) & (board << 3)

        # Kiểm tra chiến thắng theo chiều ngang
        p = (board << (Board.HEIGHT + 1)) & (board << 2 * (Board.HEIGHT + 1))
        r |= p & (board << 3 * (Board.HEIGHT + 1))
        r |= p & (board >> (Board.HEIGHT + 1))
        p = (board >> (Board.HEIGHT + 1)) & (board >> 2 * (Board.HEIGHT + 1))
        r |= p & (board << (Board.HEIGHT + 1))
        r |= p & (board >> 3 * (Board.HEIGHT + 1))

        # Kiểm tra chiến thắng theo đường chéo 1 (từ trái dưới lên phải trên)
        p = (board << Board.HEIGHT) & (board << 2 * Board.HEIGHT)
        r |= p & (board << 3 * Board.HEIGHT)
        r |= p & (board >> Board.HEIGHT)
        p = (board >> Board.HEIGHT) & (board >> 2 * Board.HEIGHT)
        r |= p & (board << Board.HEIGHT)
        r |= p & (board >> 3 * Board.HEIGHT)

        # Kiểm tra chiến thắng theo đường chéo 2 (từ trái trên xuống phải dưới)
        p = (board << (Board.HEIGHT + 2)) & (board << 2 * (Board.HEIGHT + 2))
        r |= p & (board << 3 * (Board.HEIGHT + 2))
        r |= p & (board >> (Board.HEIGHT + 2))
        p = (board >> (Board.HEIGHT + 2)) & (board >> 2 * (Board.HEIGHT + 2))
        r |= p & (board << (Board.HEIGHT + 2))
        r |= p & (board >> 3 * (Board.HEIGHT + 2))

        # Chỉ giữ lại các vị trí trống trên bàn cờ
        return r & (Board.board_mask ^ mask)

    def print_board(self):
        """
        In bàn cờ ra màn hình để dễ dàng quan sát
        Sử dụng 'X' cho người chơi hiện tại, 'O' cho đối thủ và '.' cho ô trống
        """
        print("\n  1 2 3 4 5 6 7")  # In số cột
        print(" ---------------")
        
        for row in range(Board.HEIGHT - 1, -1, -1):
            print("|", end=" ")
            for col in range(Board.WIDTH):
                pos = np.int64(1 << (row + col * (Board.HEIGHT + 1)))
                if not (pos & self.mask):
                    print(".", end=" ")
                elif pos & self.current_position:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print("|")
        print(" ---------------")

    bottom_mask = bottom(WIDTH, HEIGHT)
    board_mask = bottom_mask * ((1 << HEIGHT) - 1)




# Ví dụ sử dụng
if __name__ == "__main__":
    board = Board()
    print("Khởi tạo bàn cờ Connect 4")
    board.print_board()
    
    # Thực hiện chuỗi nước đi
    moves = "44534"  # Đi các cột 1, 2, 3, 4
    result = board.play_sequence(moves)
    print(f"\nĐã thực hiện {result} nước đi")
    board.print_board()
    
    # Kiểm tra nếu có thể thắng trong nước tiếp theo
    if board.can_win_next():
        print("\nNgười chơi hiện tại có thể thắng trong nước tiếp theo!")
    
    # Hiển thị số nước đã đi
    print(f"Số nước đã đi: {board.nb_moves()}")