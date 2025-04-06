#include "board.cpp"

struct Entry {
    uint64_t key: 56; // use 56-bit keys
    uint8_t val;      // use 8-bit values
              // overall sizeof(Entry) = 8 bytes
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