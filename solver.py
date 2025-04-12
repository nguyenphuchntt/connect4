import numpy as np
from typing import Dict, Optional
from board import Board
from MoveSorter import MoveSorter
from TranspositionTable import TranspositionTable
from OpeningBook import OpeningBook


# NOTE: Giải thích alpha beta window: 
# alpha (giá trị tốt nhất của người chơi MAX - AI)
# beta (giá trị tốt nhất của người chơi MIN - đối thủ) -> lưu ý là đối thủ muốn giá trị beta này có giá trị nhỏ nhất
# do đó khi AI tìm được nước đi tốt hơn beta, nó dừng lại ngay lập tức, nếu đối thủ tìm thấy nước đi yếu hơn alpha, nó cũng dừng lại

class Solver:
    "Giải Connect 4 sử dụng thuật toán negamax với alpha-beta pruning"
    INVALID_MOVE = -1000
    
    def __init__(self, board_class):
        """
        Khởi tạo bộ giải
        """
        self.Board = board_class  # Lưu trữ tham chiếu đến lớp Board
        self.book = OpeningBook(board_class.WIDTH, board_class.HEIGHT)
        self.node_count = 0
        
        # Khởi tạo thứ tự xem xét cột, bắt đầu từ cột giữa
        self.column_order = []
        for i in range(board_class.WIDTH):
            self.column_order.append(board_class.WIDTH // 2 + (1 - 2 * (i % 2)) * (i + 1) // 2)
            
        self.TABLE_SIZE = 24  # Lưu trữ 2^TABLE_SIZE phần tử trong transpositiontbale
        self.trans_table = TranspositionTable(self.TABLE_SIZE)
    

    def negamax(self, board, alpha, beta):
        "Triển khai thuật toán negamax với alpha-beta pruning. Return: Điểm của vị trí hiện tại"
        assert alpha < beta
        assert not board.can_win_next()
        
        self.node_count += 1
        
        possible = board.possible_non_losing_moves()
        if possible == 0:
            return (-1) * (self.Board.WIDTH * self.Board.HEIGHT - board.nb_moves()) // 2 # Thua
            
        if board.nb_moves() >= self.Board.WIDTH * self.Board.HEIGHT - 2:
            return 0  # Hòa
            
        min_score = (-1) * (self.Board.WIDTH * self.Board.HEIGHT - board.nb_moves()) // 2
        
        if alpha < min_score:
            alpha = min_score
            if alpha >= beta:
                return alpha  # Prune
                
        max_score = (self.Board.WIDTH * self.Board.HEIGHT - 1 - board.nb_moves()) // 2
        
        if beta > max_score:
            beta = max_score    # there is no need to keep beta above our max possible score.
            if alpha >= beta:
                return beta  # Prune
                
        key = board.key()
        value = self.trans_table.get(key)
        
        if value:
            if value > self.Board.MAX_SCORE - self.Board.MIN_SCORE + 1:
                # Chúng ta có một giới hạn dưới
                min_score = value + 2 * self.Board.MIN_SCORE - self.Board.MAX_SCORE - 2
                if alpha < min_score:
                    alpha = min_score
                    if alpha >= beta:
                        return alpha
            else:
                # Chúng ta có một giới hạn trên
                max_score = value + self.Board.MIN_SCORE - 1
                if beta > max_score:
                    beta = max_score
                    if alpha >= beta:
                        return beta
                        
        book_value = self.book.get(board)
        if book_value:
            return book_value + self.Board.MIN_SCORE - 1
            
        moves = MoveSorter(self.Board.WIDTH)
        
        for i in range(self.Board.WIDTH - 1, -1, -1):
            col = self.column_order[i]
            move = possible & self.Board.column_mask(col)
            if move:
                moves.add(move, board.move_score(move))
                
        next_move = moves.getNext()
        while next_move:
            board_copy = Board()  # Tạo bản sao của bàn cờ
            board_copy.play(next_move)
            score = (-1) * self.negamax(board_copy, -beta, -alpha)
            
            if score >= beta:
                self.trans_table.put(key, score + self.Board.MAX_SCORE - 2 * self.Board.MIN_SCORE + 2)
                return score
                
            if score > alpha:
                alpha = score
                
            next_move = moves.getNext()
            
        self.trans_table.put(key, alpha - self.Board.MIN_SCORE + 1)
        return alpha
        

    def solve(self, board):
        "Giải bàn cờ hiện tại sử dụng zero window search. Returns: Điểm tốt nhất có thể đạt được"
        # Giả sử bạn có phạm vi điểm từ -5 đến +5 
        # Bạn thử cửa sổ [0, 1] (med = 0)
        # Nếu kết quả <= 0, bạn biết điểm thực nằm trong khoảng [-5, 0]
        # Nếu kết quả > 0, bạn biết điểm thực nằm trong khoảng [1, 5]
        # Bạn tiếp tục thu hẹp, có thể thử [-2, -1], rồi [2, 3], v.v...
        if board.can_win_next():
            return (self.Board.WIDTH * self.Board.HEIGHT + 1 - board.nb_moves()) // 2
            
        min_score = (-1) * ((self.Board.WIDTH * self.Board.HEIGHT - board.nb_moves()) // 2)
        max_score = (self.Board.WIDTH * self.Board.HEIGHT + 1 - board.nb_moves()) // 2
        
        while min_score < max_score:
            med = min_score + (max_score - min_score) // 2
            
            if med <= 0 and min_score // 2 < med:
                med = min_score // 2
            elif med >= 0 and max_score // 2 > med:
                med = max_score // 2  # Điều chỉnh để tránh vòng lặp vô tận
                
            r = self.negamax(board, med, med + 1)
            
            if r <= med:
                max_score = r
            else:
                min_score = r
                
        return min_score
        

    def get_node_count(self):
        return self.node_count
        
    def reset(self):
        self.node_count = 0
        self.trans_table.reset()
        
    def load_book(self, book_file):
        self.book.load(book_file)