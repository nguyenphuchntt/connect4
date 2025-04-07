#ifndef TRANS_HEADER_H
#define TRANS_HEADER_H

#include "board.h"
#include <bits/stdc++.h>

struct Entry {
    uint64_t key: 56; // use 56-bit keys
    uint8_t val;      // use 8-bit values
              // overall sizeof(Entry) = 8 bytes
};

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
class TranspositionTable {
public:

    std::vector<Entry> entries;

    unsigned int index(uint64_t key) const {
        return key % entries.size();
    }

    TranspositionTable () {}

    TranspositionTable(unsigned int size): entries(size) {
    }

    /*
    * Empty the Transition Table.
    */
    void reset() { // fill everything with 0, because 0 value means missing data
        memset(&entries[0], 0, entries.size() * sizeof(Entry));
    }

    /**
     * Store a value for a given key
     * @param key: 56-bit key
     * @param value: non-null 8-bit value. null (0) value are used to encode missing data.
     */
    void put(uint64_t key, uint8_t val) {
        unsigned int i = index(key); // compute the index position
        entries[i].key = key;              // and overide any existing value.
        entries[i].val = val;       
    }


    /** 
     * Get the value of a key
     * @param key
     * @return 8-bit value associated with the key if present, 0 otherwise.
     */
    uint8_t get(uint64_t key) const {
        unsigned int i = index(key);  // compute the index position
        if(entries[i].key == key) {
            return entries[i].val;   // and return value if key matches
        } else {
            return 0;               // or 0 if missing entry
        }
    }


};

#endif