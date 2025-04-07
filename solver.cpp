#include "transpositionTable.h"
#include "board.h"
#include "MoveSorter.h"
/**
 * NOTE: Giải thích alpha beta window: 
 * 
 * alpha (giá trị tốt nhất của người chơi MAX - AI)
 * beta (giá trị tốt nhất của người chơi MIN - đối thủ) -> lưu ý là đối thủ muốn giá trị beta này có giá trị nhỏ nhất
 * do đó khi AI tìm được nước đi tốt hơn beta, nó dừng lại ngay lập tức, nếu đối thủ tìm thấy nước đi yếu hơn alpha, nó cũng dừng lại
 */

class Solver {
private:
    TranspositionTable transTable;

    unsigned long long nodeCount;

    int columnOrder[WIDTH]; // column exploration order

    int negamax(const Board& board, int alpha, int beta) {
        assert(alpha < beta);
        assert(!board.canWinNext());

        nodeCount++;

        uint64_t next = board.possibleNonLosingMoves();
        if (next == 0) {
            return - (WIDTH * HEIGHT - board.getMovedStep()) / 2;
        }
        if (board.getMovedStep() >= WIDTH * HEIGHT - 2) {
            return 0; // draw
        }
        
        int min = - (WIDTH * HEIGHT - 2 - board.getMovedStep()) / 2; // minimum score

        if (alpha < min) {
            alpha = min;
            if (alpha >= beta) return alpha; //prune
        }

        int max = (WIDTH * HEIGHT - 1 - board.getMovedStep()) / 2; // maximum score

        if(beta > max) {
            beta = max;                     // there is no need to keep beta above our max possible score.
            if(alpha >= beta) return beta;  // prune the exploration if the [alpha;beta] window is empty.
        }

        const uint64_t key = board.key();
        if (int value = transTable.get(key)) {
            if (value > MAX_SCORE - MIN_SCORE + 1) {
                // we have an lower bound
                min = value + 2 * MIN_SCORE - MAX_SCORE - 2;
                if (alpha < min) {
                    alpha = min;
                    if (alpha >= beta) return alpha;
                }
            } else { // we have an upper bound
                if (beta > max) {
                    beta = max;
                    if (alpha >= beta) return beta;
                }
            }
        }

        MoveSorter moves;

        for (int i = WIDTH; i--;) {
            // xét từ cột
            if (uint64_t move = next & Board::column_mask(columnOrder[i])) {
                // Ghép next với một cột toàn 1 -> xem cột đó có possible move không
                // nếu có -> add
                moves.add(move, board.moveScore(move));
            }
        }

        while (uint64_t next = moves.getNext()) {
            Board board_2(board);
            board_2.play(next);               // It's opponent turn in P2 position after current player plays x column.
            int score = -negamax(board_2, -beta, -alpha); // If current player plays col x, his score will be the opposite of opponent's score after playing col x
            if(score >= beta) {
                transTable.put(key, score + MAX_SCORE - 2 * MIN_SCORE + 2); // save the lower bound
                return score;  // prune the exploration if we find a possible move better than what we were looking for.
            }
            if(score > alpha) alpha = score; // reduce the [alpha;beta] window for next exploration, as we only 
                                                // need to search for a position that is better than the best so far.
        }

        transTable.put(board.key(), alpha - MIN_SCORE + 1); // save the upper bound of the position
        return alpha;
    }



public:

    void reset() {
        nodeCount = 0;
        transTable.reset();
    }

    Solver() : nodeCount{0}, transTable(8388593) { // 64MB cache
        for(int i = 0; i < WIDTH; i++){
            columnOrder[i] = WIDTH/2 + (1-2*(i%2))*(i+1)/2; // initialize the column exploration order, starting with center columns
        } 
    }

    int getBestMove(const Board& board) {
        // implement zero window search ... no tim gia tri chinh xac cua score bang cach gan giong cay nhi phan
        if (board.canWinNext()) {
            return (WIDTH * HEIGHT+  1 - board.getMovedStep()) /2;
        }

        int min = - (WIDTH * HEIGHT - board.getMovedStep()) / 2;
        int max = (WIDTH * HEIGHT+1 - board.getMovedStep())/2;
        while (min < max) {
            // iteratively narrow the min-max exploration window
            int med = min + (max - min) / 2; // trung binh cong
            if (med <= 0 && min / 2 < med) med = min / 2;
            else if (med >= 0 && max / 2 > med) med = max / 2; // dieu chinh de tranh lap vo han
            int r = negamax(board, med, med + 1);
            if (r <= med) {
                max = r;
            } else {
                min = r;
            }
        }
        return min;
    }

    unsigned long long getNodeCount() {
        return nodeCount;
    }

};