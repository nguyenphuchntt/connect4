#ifndef SOLVER_H
#define SOLVER_H

#include "board.h"
#include "TranspositionTable.h"
#include "OpeningBook.h"

class Solver {
private:
    OpeningBook book{Board::WIDTH, Board::HEIGHT}; // opening book

    unsigned long long nodeCount;

    int columnOrder[Board::WIDTH];

    static constexpr int TABLE_SIZE = 24; // store 2^TABLE_SIZE elements in the transpositiontbale

    TranspositionTable < uint_t < Board::WIDTH*(Board::HEIGHT + 1) - TABLE_SIZE >, Board::position_t, uint8_t, TABLE_SIZE > transTable;
    int negamax(const Board &board, int alpha, int beta);

public:
    static const int INVALID_MOVE = -1000;


    int solve(const Board& board);

    unsigned long long getNodeCount() {
        return nodeCount;
    }

    void reset() {
        nodeCount = 0;
        transTable.reset();
    }

    void loadBook(std::string book_file) {
        book.load(book_file);
    }

    Solver();

};

#endif