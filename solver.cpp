#include "./board.cpp"

/**
 * NOTE: Giải thích alpha beta window: 
 * 
 * alpha (giá trị tốt nhất của người chơi MAX - AI)
 * beta (giá trị tốt nhất của người chơi MIN - đối thủ) -> lưu ý là đối thủ muốn giá trị beta này có giá trị nhỏ nhất
 * do đó khi AI tìm được nước đi tốt hơn beta, nó dừng lại ngay lập tức, nếu đối thủ tìm thấy nước đi yếu hơn alpha, nó cũng dừng lại
 */

class Solver {
private:
    unsigned long long nodeCount;

    int columnOrder[WIDTH]; // column exploration order

    int negamax(const Board& board, int alpha, int beta) {
        nodeCount++;

        if (board.getMovedStep() == WIDTH * HEIGHT) { // draw game
            return 0;
        }

        for(int x = 0; x < WIDTH; x++) { // check if can win at the next move
            if(board.canPlay(x) && board.isWinningMove(x)) 
            return (WIDTH * HEIGHT +  1 - board.getMovedStep()) / 2;
        }

        int max = (WIDTH * HEIGHT - 1 - board.getMovedStep()) / 2; // maximum score is score of winning at this state

        if(beta > max) {
            beta = max;                     // there is no need to keep beta above our max possible score.
            if(alpha >= beta) return beta;  // prune the exploration if the [alpha;beta] window is empty.
        }

        int bestScore = - WIDTH* HEIGHT;

        for(int x = 0; x < WIDTH; x++) {
            // compute the score of all possible next move and keep the best one
            if (board.canPlay(columnOrder[x])) { // play by order
                Board board_2(board);
                board_2.play(columnOrder[x]);               // It's opponent turn in P2 position after current player plays x column.
                int score = -negamax(board_2, -alpha, -beta); // If current player plays col x, his score will be the opposite of opponent's score after playing col x
                if(score >= beta) return score;  // prune the exploration if we find a possible move better than what we were looking for.
                if(score > alpha) alpha = score; // reduce the [alpha;beta] window for next exploration, as we only 
                                                    // need to search for a position that is better than the best so far.
            }
        }
      return alpha;
    }

public:

    Solver() : nodeCount(0) {
        for(int i = 0; i < WIDTH; i++){
            columnOrder[i] = WIDTH/2 + (1-2*(i%2))*(i+1)/2; // initialize the column exploration order, starting with center columns
        } 
    }

    int getBestMove(const Board& board) {
        nodeCount = 0;
        return negamax(board, - WIDTH * HEIGHT/2, WIDTH * HEIGHT / 2);
    }

    unsigned long long getNodeCount() {
        return nodeCount;
    }

};