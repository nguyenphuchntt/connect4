#ifndef MoveSorter_H
#define MoveSorter_H

#include <bits/stdc++.h>
#include "board.h"

/**
 * Gần giống priority queue để lấy move có giá trị tốt nhất
 */
class MoveSorter {
public: 

    void add(uint64_t move, int score) {
        // Add a move in the container with its score
        int pos = size++;
        for(; pos && entries[pos - 1].score > score; --pos) {
            entries[pos] = entries[pos - 1];
        }
        entries[pos].move = move;
        entries[pos].score = score;
    }

    uint64_t getNext() {
        // Get next move
        if (size) {
            return entries[--size].move;
        } else {
            return 0;
        }
    }

    void reset() {
        size = 0;
    }

    MoveSorter() : size{0} {

    }

private:
    // number of stored moves
    unsigned int size;

    struct {
        uint64_t move;
        int score;
    } entries[Board::WIDTH];

};

#endif