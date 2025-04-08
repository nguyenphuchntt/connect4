#ifndef TRANS_HEADER2_H
#define TRANS_HEADER2_H

#include "board.h"
#include <bits/stdc++.h>

/**
 * NOTE: improve by Chinese remainder theorem
 * Thuật toán này giúp giải phương trình đồng dư -> chứng minh được cần tối thiếu bao nhiêu entries để không xảy ra collision trong hash table
 */

// get median
constexpr uint64_t med(uint64_t min, uint64_t max) {
    return (min + max) / 2;
}

// a number has a divisor between in (a, b)
constexpr bool has_factor(uint64_t n, uint64_t min, uint64_t max) {
    return min * min > n ? false : 
        min + 1 >= max ? n % min == 0 :
           has_factor(n, min, med(min, max)) || has_factor(n, med(min, max), max);
}

// return next prime number greater or equal to n.
constexpr uint64_t next_prime(uint64_t n) {
    return has_factor(n, 2, n) ? next_prime(n + 1) : n;
}

constexpr unsigned int log2(unsigned int n) {
    return n <= 1 ? 0 : log2(n / 2) + 1;
}

/**
 * Abstrac interface for the Transposition Table get function
 */
template<class key_t, class value_t>
class TableGetter {
    private:
        virtual void* getKeys() = 0;
        virtual void* getValues() = 0;
        virtual size_t getSize() = 0;
        virtual int getKeySize() = 0;
        virtual int getValueSize() = 0;

    public:
        virtual value_t get(key_t key) const = 0;
        virtual ~TableGetter() {};

        friend class OpeningBook;
};

// hash table to caching
// keySize = 7 * 7 = 49
// valueSize = 7
// logSize = 23
class TranspositionTable {
private:
    // size of the transition table. Have to be odd, at best -> prime number
    static const size_t size = next_prime(1 << 23);

    uint32_t *K; // array to store key; 26
    uint8_t *V; // array to store value; 7

    size_t index(uint64_t key) const {
        return key % size;
    }
public:

    TranspositionTable() {
        K = new uint32_t[size];
        V = new uint8_t[size];
        reset();
    }

    ~TranspositionTable() {
        delete[] K;
        delete[] V;
    }

    void reset() { // fill everything with 0, because 0 value means missing data
        memset(K, 0, size * sizeof(uint32_t));
        memset(V, 0, size * sizeof(uint8_t));
    }


    //Store a value for a given key
    void put(uint32_t key, uint8_t value) {
        size_t pos = index(key);
        K[pos] = key;
        V[pos] = value;
    }

    // Get the value of a key
    uint8_t get(uint32_t key) const {
        size_t pos = index(key);  // compute the index position
        if(K[pos] == (uint32_t)key) {
            return V[pos];   // and return value if key matches
        } else {
            return 0;               // or 0 if missing entry
        }
    }


};

#endif