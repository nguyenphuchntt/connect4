#ifndef BOARD_H
#define BOARD_H

#include <bits/stdc++.h>

constexpr static uint64_t bottom(int width, int height) {
    // return a bitmask with a row full of 1 at the bottom
    return width == 0 ? 0 : bottom(width-1, height) | 1LL << (width-1)*(height+1);
}

class Board {

    friend class Solver;
    public:
        static const int WIDTH = 7;
        static const int HEIGHT = 6;
        static const int MIN_SCORE = -(WIDTH*HEIGHT)/2 + 3;
        static const int MAX_SCORE = (WIDTH*HEIGHT+1)/2 - 3;

        using position_t = typename std::conditional < WIDTH * (HEIGHT + 1) <= 64, uint64_t, __int128>::type;

        static_assert(WIDTH < 10, "Board's width must be less than 10");
        static_assert(WIDTH*(HEIGHT+1) <= 64, "Board does not fit in 64bits bitboard");
        /** 
         * A class storing a Connect 4 Board.
         * Functions are relative to the current player to play.
         * Board containing aligment are not supported by this class.
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
         * Board is stored as
         * - a bitboard "mask" with 1 on any color stones
         * - a bitboard "current_player" with 1 on stones of current player
         *
         * "current_player" bitboard can be transformed into a compact and non ambiguous key
         * by adding an extra bit on top of the last non empty cell of each column.
         * This allow to identify all the empty cells whithout needing "mask" bitboard
         *
         * current_player "x" = 1, opponent "o" = 0
         * board     Board  mask      key       bottom
         *           0000000   0000000   0000000   0000000
         * .......   0000000   0000000   0001000   0000000
         * ...o...   0000000   0001000   0010000   0000000
         * ..xx...   0011000   0011000   0011000   0000000
         * ..ox...   0001000   0011000   0001100   0000000
         * ..oox..   0000100   0011100   0000110   0000000
         * ..oxxo.   0001100   0011110   1101101   1111111
         *
         * current_player "o" = 1, opponent "x" = 0
         * board     Board  mask      key       bottom
         *           0000000   0000000   0001000   0000000
         * ...x...   0000000   0001000   0000000   0000000
         * ...o...   0001000   0001000   0011000   0000000
         * ..xx...   0000000   0011000   0000000   0000000
         * ..ox...   0010000   0011000   0010100   0000000
         * ..oox..   0011000   0011100   0011010   0000000
         * ..oxxo.   0010010   0011110   1110011   1111111
         *
         * key is an unique representation of a board key = Board + mask + bottom
         * in practice, as bottom is constant, key = Board + mask is also a 
         * non-ambigous representation of the Board.
         */

        /**
         * Play a playable column
         */
        void play(uint64_t move) {
            current_position ^= mask;
            mask |= move;
            movedStep++;
        }

        /**
         * Use for initialize a non-empty board
         */
        unsigned int play(std::string seq) {
            for(unsigned int i = 0; i < seq.size(); i++) {
                int column = seq[i] - '1';
                if(column < 0 || column >= Board::WIDTH || !canPlay(column) || isWinningMove(column)) return i; // invalid move
                playCol(column);
              }
              return seq.size();
        }

        bool canWinNext() const {
            return winning_position() & possible();
        }

        int nbMoves() const {
            return movedStep;
        }

        uint64_t key() const {
            return current_position + mask;
        }

        uint64_t key3() const {
            uint64_t key_forward = 0;
            for(int i = 0; i < Board::WIDTH; i++) partialKey3(key_forward, i);  // compute key in increasing order of columns
        
            uint64_t key_reverse = 0;
            for(int i = Board::WIDTH; i--;) partialKey3(key_reverse, i);  // compute key in decreasing order of columns
        
            return key_forward < key_reverse ? key_forward / 3 : key_reverse / 3; // take the smallest key and divide per 3 as the last base3 digit is always 0
          }

        // return a bitmap of all the possible next moves that do not lose in one turn.
        uint64_t possibleNonLosingMoves() const {
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

        // score a possible move = number of possible winning state
        int moveScore(uint64_t move) const {
            return popCount(compute_winning_position(current_position | move, mask));
        }

        Board() : current_position{0}, mask{0}, movedStep{0} {
        }

private:
        /**
         * NOTE: Cách tính điểm vd: -5 có nghĩa là sẽ thua sau 5 nước tính từ khi chơi full bàn cờ (42/42 quân), +5 nghĩa là chơi thắng sau 5 nước tính từ khi chơi full bàn cờ
         */
        uint64_t current_position; // lưu người chơi hiện tại
        uint64_t mask;              // lưu cho cả hai người chơi
        unsigned int movedStep;

        void partialKey3(uint64_t &key, int col) const {
            for(position_t pos = UINT64_C(1) << (col * (Board::HEIGHT + 1)); pos & mask; pos <<= 1) {
              key *= 3;
              if(pos & current_position) key += 1;
              else key += 2;
            }
            key *= 3;
          }

        /**
         * Indicates whether a column is playable
         */
        bool canPlay(int column) const {
            return (mask & top_mask_col(column)) == 0;
        }

        // play at the column
        void playCol(int column) {
            play((mask + bottom_mask_col(column)) & column_mask(column));
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

        // 
        uint64_t possible() const {
            return (mask + bottom_mask) & board_mask; // những ô đã đi rồi + 1 độ cao
        }

        // counts number of bit set to one in a 64 bits integer
        static unsigned int popCount(uint64_t m) {
            unsigned int c = 0; 
            for (c = 0; m; c++) m &= m - 1;
            return c;
        }

        // list possible winning moves
        static uint64_t compute_winning_position(uint64_t Board, uint64_t mask) {
            // vertical;
            uint64_t r = (Board << 1) & (Board << 2) & (Board << 3);

            //horizontal
            uint64_t p = (Board << (HEIGHT+1)) & (Board << 2*(HEIGHT+1));
            r |= p & (Board << 3*(HEIGHT+1));
            r |= p & (Board >> (HEIGHT+1));
            p = (Board >> (HEIGHT+1)) & (Board >> 2*(HEIGHT+1));
            r |= p & (Board << (HEIGHT+1));
            r |= p & (Board >> 3*(HEIGHT+1));

            //diagonal 1
            p = (Board << HEIGHT) & (Board << 2*HEIGHT);
            r |= p & (Board << 3*HEIGHT);
            r |= p & (Board >> HEIGHT);
            p = (Board >> HEIGHT) & (Board >> 2*HEIGHT);
            r |= p & (Board << HEIGHT);
            r |= p & (Board >> 3*HEIGHT);

            //diagonal 2
            p = (Board << (HEIGHT+2)) & (Board << 2*(HEIGHT+2));
            r |= p & (Board << 3*(HEIGHT+2));
            r |= p & (Board >> (HEIGHT+2));
            p = (Board >> (HEIGHT+2)) & (Board >> 2*(HEIGHT+2));
            r |= p & (Board << (HEIGHT+2));
            r |= p & (Board >> 3*(HEIGHT+2));

            return r & (board_mask ^ mask);
        }


        const static uint64_t bottom_mask = bottom(WIDTH, HEIGHT);
        const static uint64_t board_mask = bottom_mask * ((1LL << HEIGHT)-1);


        // return a bitmask containing a single 1 corresponding to the top cel of a given column
        static constexpr uint64_t top_mask_col(int column) {
            return UINT64_C(1) << ((HEIGHT - 1) + column*(HEIGHT+1));
        }

        // return a bitmask containing a single 1 corresponding to the bottom cell of a given column
        static constexpr uint64_t bottom_mask_col(int column) {
            return UINT64_C(1) << column*(HEIGHT+1);
        }

    public:

        // return a bitmask 1 on all the cells of a given column
        static constexpr int64_t column_mask(int column) {
            return ((UINT64_C(1) << HEIGHT) - 1) << column * (HEIGHT + 1);
        }
};

#endif