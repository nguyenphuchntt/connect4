import subprocess

ROWS = 6
COLS = 7

def getCol(data):
    print(f"data:{data}")
    col = -1
    max_score = 1000
    for i in range(COLS):
        process = subprocess.Popen(
            ["./c4solver"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if data.count(str(i + 1)) >= ROWS:
            continue
        output, error = process.communicate(input=(data + str(i + 1)))
        try:
            if (int(output) < max_score):
                max_score = int(output)
                col = i
        except Exception:
            return i
    return col

import sys

def print_board(board):
    print()
    for r in range(ROWS):
        for c in range(COLS):
            print(f"| {board[r][c]} ", end='')
        print("|")
    for c in range(COLS):
        print(f"  {c} ", end='')
    print("\n")


def main():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    moved = ""
    current_player = 'O'

    while True:
        print_board(board)

        if current_player == 'O':
            best_col = getCol(moved)
            print(f"AI move: {best_col}")
            moved += str(best_col + 1)  # move history: 1-based

            for r in reversed(range(ROWS)):
                if board[r][best_col] == ' ':
                    board[r][best_col] = current_player
                    break
        else:
            try:
                col = int(input(f"Player {current_player}, enter column (0-{COLS - 1}): "))
                if not (0 <= col < COLS):
                    print("Invalid column. Try again.")
                    continue

                # check if column is full
                if board[0][col] != ' ':
                    print("Column full. Try again.")
                    continue

                moved += str(col + 1)
                for r in reversed(range(ROWS)):
                    if board[r][col] == ' ':
                        board[r][col] = current_player
                        break
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    main()
