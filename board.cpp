#include <bits/stdc++.h>

static const int WIDTH = 7;
static const int HEIGHT = 6;

static_assert(WIDTH < 10, "Board's width must be less than 10");
static_assert(WIDTH*(HEIGHT+1) <= 64, "Board does not fit in 64bits bitboard");

class Board {

private:
    /**
     * NOTE: 0 means EMPTY
     * NOTE: 1 means PERSON
     * NOTE: -1 means AI
     * 
     * NOTE: Ban co nay nam ngang
     * NOTE: Cách tính điểm vd: -5 có nghĩa là sẽ thua sau 5 nước tính từ khi chơi full bàn cờ (42/42 quân), +5 nghĩa là chơi thắng sau 5 nước tính từ khi chơi full bàn cờ
     */
    int board[WIDTH][HEIGHT];
    int height[WIDTH];
    unsigned int movedStep;

    uint64_t current_position; // lưu người chơi hiện tại
    uint64_t mask;              // lưu cho cả hai người chơi

    // return a bitmask containing a single 1 corresponding to the top cel of a given column
    static uint64_t top_mask(int col) {
        return (UINT64_C(1) << (HEIGHT - 1)) << col * (HEIGHT+1);
    }

    // return a bitmask containing a single 1 corresponding to the bottom cell of a given column
    static uint64_t bottom_mask(int col) {
        return UINT64_C(1) << col * (HEIGHT+1);
    }

public:

    Board() : board{0}, height{0}, movedStep{0} {
    }

    unsigned int getMovedStep() const {
        return movedStep;
    }

    /**
     * Indicates whether a column is playable
     */
    bool canPlay(int column) const {
        return (mask & top_mask(column)) == 0;
    }

    /**
     * Play a playable column
     */
    void play(int column) {
        current_position ^= mask; // chuyển người chơi 
        mask |= mask + bottom_mask(column);
        movedStep++;
    }

    /**
     * Use for initialize a non-empty board
     */
    unsigned int play(std::string seq) {
        for(unsigned int i = 0; i < seq.size(); i++) {
            int col = seq[i] - '1'; 
            if(col < 0 || col >= WIDTH || !canPlay(col) || isWinningMove(col)) return i; // invalid move
            play(col);
        }
        return seq.size();
    }

    /**
     * Indicates whether the current player wins by playing a given column.
     */
    bool isWinningMove(int column) const {
        int current_player = 1 + movedStep % 2;
        if(height[column] >= 3 
            && board[column][height[column]-1] == current_player 
            && board[column][height[column]-2] == current_player 
            && board[column][height[column]-3] == current_player) 
          return true;
        for (int dy = -1; dy <= 1; dy++) {    // check hàng ngang, chéo lên, chéo xuống
            int nb = 0;                       // đếm số lượng cùng màu
            for(int dx = -1; dx <= 1; dx += 2) // tương ứng với ở trên, nhưng mở rộng sang bên trái hay bên phải
                for(int x = column + dx, y = height[column] + dx * dy; x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT && board[x][y] == current_player; nb++) {
                // 
                x += dx;
                y += dx * dy;
            }
            if(nb >= 3) return true; // nếu có lớn hơn hoặc bằng 3 ô cùng màu (chưa tính ô hiện tại) thì thắng
        }
        return false;
    }



};




