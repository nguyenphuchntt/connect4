#ifndef BOARD_H
#define BOARD_H


#include <bits/stdc++.h>

static const int WIDTH = 7;
static const int HEIGHT = 6;
static const int MIN_SCORE = - (WIDTH * HEIGHT) / 2 + 3;
static const int MAX_SCORE = (WIDTH * HEIGHT + 1) / 2 - 3;

constexpr static uint64_t bottom(int width, int height) {
    // return a bitmask with a row full of 1 at the bottom
    return width == 0 ? 0 : bottom(width - 1, height) | 1LL << (width - 1) * (height + 1);
}

class Board {
    /** 
     * A class storing a Connect 4 position.
     * Functions are relative to the current player to play.
     * Position containing aligment are not supported by this class.
     *
     * A binary bitboard representationis used.
     * Each column is encoded on HEIGH+1 bits.
     * 
     * Example of bit order to encode for a 7x6 board
     * .  .  .  .  .  .  .
     * 5 12 19 26 33 40 47
     * 4 11 18 25 32 39 46
     * 3 10 17 24 31 38 45
     * 2  9 16 23 30 37 44
     * 1  8 15 22 29 36 43
     * 0  7 14 21 28 35 42 
     * 
     * Position is stored as
     * - a bitboard "mask" with 1 on any color stones
     * - a bitboard "current_player" with 1 on stones of current player
     *
     * "current_player" bitboard can be transformed into a compact and non ambiguous key
     * by adding an extra bit on top of the last non empty cell of each column.
     * This allow to identify all the empty cells whithout needing "mask" bitboard
     *
     * current_player "x" = 1, opponent "o" = 0
     * board     position  mask      key       bottom
     *           0000000   0000000   0000000   0000000
     * .......   0000000   0000000   0001000   0000000
     * ...o...   0000000   0001000   0010000   0000000
     * ..xx...   0011000   0011000   0011000   0000000
     * ..ox...   0001000   0011000   0001100   0000000
     * ..oox..   0000100   0011100   0000110   0000000
     * ..oxxo.   0001100   0011110   1101101   1111111
     *
     * current_player "o" = 1, opponent "x" = 0
     * board     position  mask      key       bottom
     *           0000000   0000000   0001000   0000000
     * ...x...   0000000   0001000   0000000   0000000
     * ...o...   0001000   0001000   0011000   0000000
     * ..xx...   0000000   0011000   0000000   0000000
     * ..ox...   0010000   0011000   0010100   0000000
     * ..oox..   0011000   0011100   0011010   0000000
     * ..oxxo.   0010010   0011110   1110011   1111111
     *
     * key is an unique representation of a board key = position + mask + bottom
     * in practice, as bottom is constant, key = position + mask is also a 
     * non-ambigous representation of the position.
     */

    public:

    Board() : current_position{0}, mask{0}, movedStep{0} {
    }

    uint64_t key() const {
        return current_position + mask;
    }

    unsigned int getMovedStep() const {
        return movedStep;
    }

    /**
     * Indicates whether a column is playable
     */
    bool canPlay(int column) const {
        return (mask & top_mask_col(column)) == 0;
    }

    /**
     * Play a playable column
     */
    void play(int column) {
        current_position ^= mask; // chuyển người chơi 
        mask |= mask + bottom_mask_col(column);
        // bottom_mask trả về một mask chứa giá trị 1 duy nhất tại cột đã truyền vào
        // mask + bottom_mask(col) sẽ đẩy cột được chọn lên chiều cao 1 (vì 1 + 1 = 10)
        // |= để fill lại số 0 (trong 10) thành 11
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
 
    uint64_t getMask() const {
        return mask;
    }

    uint64_t getPosition() const {
        return current_position;
    }



private:
    /**
     * NOTE: 0 means EMPTY
     * NOTE: 1 means PERSON
     * NOTE: -1 means AI
     * 
     * NOTE: Ban co nay nam ngang
     * NOTE: Cách tính điểm vd: -5 có nghĩa là sẽ thua sau 5 nước tính từ khi chơi full bàn cờ (42/42 quân), +5 nghĩa là chơi thắng sau 5 nước tính từ khi chơi full bàn cờ
     */
    uint64_t current_position; // lưu người chơi hiện tại
    uint64_t mask;              // lưu cho cả hai người chơi
    unsigned int movedStep;

    // return a bitmask containing a single 1 corresponding to the top cel of a given column
    static uint64_t top_mask_col(int col) {
        return (UINT64_C(1) << (HEIGHT - 1)) << col * (HEIGHT+1);
    }

    // return a bitmask containing a single 1 corresponding to the bottom cell of a given column
    static uint64_t bottom_mask_col(int col) {
        return UINT64_C(1) << col * (HEIGHT+1);
    }

    // return a bitmask 1 on all the cells of a given column
    static uint64_t column_mask(int col) {
        return ((UINT64_C(1) << HEIGHT)-1) << col*(HEIGHT+1);
    }
  
    // check winning condition
    static bool alignment(uint64_t pos) {
        // horizontal 
        uint64_t m = pos & (pos >> (HEIGHT+1));
        // shift sang phai 1 don vi & vi tri hien tai -> xem co 2 o lien nhau khong
        if(m & (m >> (2*(HEIGHT+1)))) return true;
        // m la ket qua cua phep tinh tren, shift tiep sang 2 don vi de xem co 4 o lien nhau khong
        // Ket qua chi can khong phai tat ca deu la bit 0 la true

        // diagonal 1
        m = pos & (pos >> HEIGHT);
        // tuong tu o tren nhung shift cheo tren
        if(m & (m >> (2*HEIGHT))) return true;

        // diagonal 2 
        m = pos & (pos >> (HEIGHT+2));
        // tuong tu o tren nhung shift cheo duoi
        if(m & (m >> (2*(HEIGHT+2)))) return true;

        // vertical;
        m = pos & (pos >> 1);
        //tuong tu o tren nhung shift theo chieu doc
        if(m & (m >> 2)) return true;

        return false;
    }

    const static uint64_t bottom_mask = bottom(WIDTH, HEIGHT);
    const static uint64_t board_mask = bottom_mask * ((1LL << HEIGHT) - 1); // full 1

    // 
    uint64_t possible() const {
        return (mask + bottom_mask) & board_mask; // những ô đã đi rồi + 1 ô trên nó full 1
    }

    /**
     * Indicates whether the current player wins by playing a given column.
     */
    bool isWinningMove(int column) const {
        return winning_position() & possible() & column_mask(column);
    }

    uint64_t winning_position() const {
        return compute_winning_position(current_position, mask);
    }

    uint64_t opponent_winning_position() const {
        return compute_winning_position(current_position ^ mask, mask);
    }

    bool canWinNext() {
        return winning_position() & possible();
    }

    uint64_t possibleNonLosingMoves() {
        assert(!canWinNext());
        uint64_t possible_mask = possible();
        uint64_t opponent_win = opponent_winning_position();
        uint64_t forced_moves = possible_mask & opponent_win;
        if (forced_moves) {
            if (forced_moves & (forced_moves - 1)) {
                // more than 1 forced move
                return 0; // lose
            } else {
                possible_mask = forced_moves;
                // have to play this move
            }
        }
        return possible_mask & ~(opponent_win >> 1);
        // tránh đánh ô ở dưới ô đối thủ sẽ thắng vì turn sau là turn của họ đánh rồi
    }

    static uint64_t compute_winning_position(uint64_t position, uint64_t mask) {
        // chieu doc
        uint64_t r = (position << 1) & (position << 2) & (position << 3);

        // chieu ngang
        uint64_t p = (position << (HEIGHT+1)) & (position << 2*(HEIGHT+1));
        r |= p & (position << 3*(HEIGHT+1));
        r |= p & (position >> (HEIGHT+1));
        p = (position >> (HEIGHT+1)) & (position >> 2*(HEIGHT+1));
        r |= p & (position << (HEIGHT+1));
        r |= p & (position >> 3*(HEIGHT+1));

        //diagonal 1
        p = (position << HEIGHT) & (position << 2*HEIGHT);
        r |= p & (position << 3*HEIGHT);
        r |= p & (position >> HEIGHT);
        p = (position >> HEIGHT) & (position >> 2*HEIGHT);
        r |= p & (position << HEIGHT);
        r |= p & (position >> 3*HEIGHT);

        //diagonal 2
        p = (position << (HEIGHT+2)) & (position << 2*(HEIGHT+2));
        r |= p & (position << 3*(HEIGHT+2));
        r |= p & (position >> (HEIGHT+2));
        p = (position >> (HEIGHT+2)) & (position >> 2*(HEIGHT+2));
        r |= p & (position << (HEIGHT+2));
        r |= p & (position >> 3*(HEIGHT+2));

        return r & (board_mask ^ mask);
        // r la cac nuoc di co the win
        // (board_mask ^ mask) la nhung nuoc chua danh
    }
};

#endif