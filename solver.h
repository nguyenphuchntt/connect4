#ifndef SOLVER_H
#define SOLVER_H

#include "board.h"
#include "TranspositionTable.h"

class Solver {
private:
    unsigned long long nodeCount;

    int columnOrder[Board::WIDTH];

    TranspositionTable<Board::WIDTH * (Board::HEIGHT + 1),
                    7,
                    23> transTable;
    int negamax(const Board &board, int alpha, int beta);

public:
    int solve(const Board& board);
    unsigned long long getNodeCount() {
        return nodeCount;
    }

    void reset() {
        nodeCount = 0;
        transTable.reset();
    }

    Solver();

};

#endif