import sys
from board import Board
from solver import Solver

ROWS = 6
COLS = 1

def get_best_move(data):
    print(f"data: {data}")
    
    # Khởi tạo Board và Solver
    game_board = Board()
    solver = Solver(Board)
    
    # Áp dụng lịch sử nước đi
    moves_played = game_board.play_sequence(data)
    if moves_played != len(data):
        print(f"Chỉ đánh được {moves_played}/{len(data)} nước")
    
    # In trạng thái bàn cờ để debug
    print("Trạng thái bàn cờ hiện tại:")
    game_board.print_board()
    
    # Tìm nước đi tốt nhất
    col = -1
    max_score = -1000
    
    for i in range(COLS):
        # Kiểm tra xem có thể đánh vào cột này không
        if not game_board.can_play(i):
            print(f"Cột {i} đã đầy, không thể đánh")
            continue
            
        # Tạo một bàn cờ mới và thử nước đi
        test_board = Board()
        # Copy thông tin từ game_board
        test_board.current_position = game_board.current_position.copy() if hasattr(game_board.current_position, 'copy') else game_board.current_position
        test_board.mask = game_board.mask.copy() if hasattr(game_board.mask, 'copy') else game_board.mask
        test_board.moved_step = game_board.moved_step
        
        # Thực hiện nước đi
        try:
            test_board.play_col(i)
            # Đánh giá nước đi
            score = -solver.solve(test_board)  # Negate vì xem xét từ góc nhìn đối thủ
            print(f"Đánh giá cột {i}: điểm = {score}")
            
            # Cập nhật nước đi tốt nhất
            if score > max_score:
                max_score = score
                col = i
        except Exception as e:
            print(f"Lỗi khi đánh giá cột {i}: {str(e)}")
    
    print(f"Cột tốt nhất: {col} với điểm {max_score}")
    return col

def print_board(board):
    """In bàn cờ ra màn hình"""
    print()
    for r in range(ROWS):
        for c in range(COLS):
            print(f"| {board[r][c]} ", end='')
        print("|")
    print("-----------------------------")
    for c in range(COLS):
        print(f"  {c} ", end='')
    print("\n")

def check_win(board, last_player, last_col):
    """
    Kiểm tra chiến thắng sau nước đi cuối cùng
    
    Args:
        board: Mảng 2D biểu diễn bàn cờ
        last_player: Người chơi vừa đi ('X' hoặc 'O')
        last_col: Cột vừa đánh
    
    Returns:
        bool: True nếu người chơi last_player thắng, False nếu không
    """
    # Tìm hàng của quân vừa đặt
    last_row = 0
    for r in range(ROWS-1, -1, -1):
        if board[r][last_col] == last_player:
            last_row = r
            break
    
    # Kiểm tra 4 hướng: ngang, dọc, chéo xuống, chéo lên
    directions = [
        [(0, 1), (0, -1)],  # Ngang
        [(1, 0), (-1, 0)],  # Dọc
        [(1, 1), (-1, -1)], # Chéo xuống
        [(-1, 1), (1, -1)]  # Chéo lên
    ]
    
    for dir_pair in directions:
        count = 1  # Quân vừa đặt
        for dr, dc in dir_pair:
            r, c = last_row, last_col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == last_player:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Kiểm tra bàn cờ đã đầy chưa"""
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    """Hàm chính để chạy trò chơi"""
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    moved = ""  # Lịch sử nước đi
    current_player = 'O'  

    while True:
        print_board(board)

        if current_player == 'O':  # Lượt của AI
            best_col = get_best_move(moved)
            print(f"AI move: {best_col}")
            moved += str(best_col + 1)  # 1-based trong lịch sử nước đi

            # Cập nhật bàn cờ hiển thị
            row = -1
            for r in reversed(range(ROWS)):
                if board[r][best_col] == ' ':
                    board[r][best_col] = current_player
                    row = r
                    break
            
            # Kiểm tra chiến thắng
            if check_win(board, current_player, best_col):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
        else:  # Lượt của người chơi
            try:
                col = int(input(f"Player {current_player}, enter column (0-{COLS - 1}): "))
                if not (0 <= col < COLS):
                    print("Invalid column. Try again.")
                    continue

                # Kiểm tra xem cột có đầy không
                if board[0][col] != ' ':
                    print("Column full. Try again.")
                    continue

                moved += str(col + 1)  # 1-based trong lịch sử nước đi
                
                # Cập nhật bàn cờ hiển thị
                row = -1
                for r in reversed(range(ROWS)):
                    if board[r][col] == ' ':
                        board[r][col] = current_player
                        row = r
                        break
                
                # Kiểm tra chiến thắng
                if check_win(board, current_player, col):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    break
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue
        
        # Kiểm tra hòa
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Chuyển lượt
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()