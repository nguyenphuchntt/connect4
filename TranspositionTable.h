#ifndef TRANS_HEADER_H
#define TRANS_HEADER_H

#include <bits/stdc++.h>
#include "board.h"


/*
 * util functions to compute next prime at compile time
 */
constexpr uint64_t med(uint64_t min, uint64_t max) {
  return (min+max)/2;
}
/*
 * tells if an integer n has a a divisor between min (inclusive) and max (exclusive)
 */
constexpr bool has_factor(uint64_t n, uint64_t min, uint64_t max) {
  return min*min > n ? false : // do not search for factor above sqrt(n)
    min + 1 >= max ? n % min == 0 :
    has_factor(n, min, med(min,max)) || has_factor(n, med(min,max), max);
}

// return next prime number greater or equal to n.
// n must be >= 2
constexpr uint64_t next_prime(uint64_t n) {
  return has_factor(n, 2, n) ? next_prime(n+1) : n;
}

/**
 * Transposition Table is a simple hash map with fixed storage size.
 * In case of collision we keep the last entry and overide the previous one.
 * We keep only part of the key to reduce storage, but no error is possible thanks to Chinese theorem.
 *
 * The number of stored entries is a power of two that is defined at compile time.
 * We also define size of the entries and keys to allow optimization at compile time.
 * 
 * key_size:   number of bits of the key
 * value_size: number of bits of the value
 * log_size:   base 2 log of the size of the Transposition Table.
 *             The table will contain 2^log_size elements
 */
template<unsigned int key_size, unsigned int value_size, unsigned int log_size>
class TranspositionTable {
  private:

  static_assert(key_size   <= 64, "key_size is too large");
  static_assert(value_size <= 64, "value_size is too large");
  static_assert(log_size   <= 64, "log_size is too large");

  // uint_t<S> is a template type providing an unsigned int able to fit interger of S bits.
  // uint_t<8> = uint8_t and uint_t<9> = uint_16t
  template<int S> using uint_t = 
      typename std::conditional<S <= 8, uint_least8_t, 
      typename std::conditional<S <= 16, uint_least16_t,
      typename std::conditional<S <= 32, uint_least32_t, 
                                         uint_least64_t>::type >::type >::type;


  /*
   * We only store partially the key to save memory. We keep sufficient number of bits to avoid any collision
   * of same key in the same slot having the same stored trucated key.
   */
  typedef uint_t<key_size - log_size> key_t;  // integer to fit at least key_size - log_size bits
  typedef uint_t<value_size> value_t;         // integer to fit values

  static const size_t size = next_prime(1 << log_size); // size of the transition table. Have to be odd to be prime with 2^sizeof(key_t)
                                                        // using a prime number reduces collisions
  key_t *K;     // Array to store truncated version of keys;
  value_t *V;   // Array to store values;

  size_t index(uint64_t key) const {
    return key%size;
  }

  public:
  
  TranspositionTable() {
    K = new key_t[size];
    V = new value_t[size];
    reset();
  }
  
  ~TranspositionTable() {
    delete[] K;
    delete[] V;
  }

  /*
   * Empty the Transition Table.
   */
  void reset() { // fill everything with 0, because 0 value means missing data
    memset(K, 0, size*sizeof(key_t));
    memset(V, 0, size*sizeof(value_t));
  }

  /**
   * Store a value for a given key
   * @param key: must be less than key_size bits.
   * @param value: must be less than value_size bits. null (0) value is used to encode missing data
   */
  void put(uint64_t key, value_t value) {
    assert(key >> key_size == 0);
    assert(value >> value_size == 0);
    size_t pos = index(key);
    K[pos] = key; // key is possibly trucated as key_t is possibly less than key_size bits.
    V[pos] = value;
  }

  /** 
   * Get the value of a key
   * @param key: must be less than key_size bits.
   * @return value_size bits value associated with the key if present, 0 otherwise.
   */
  value_t get(uint64_t key) const {
    assert(key >> key_size == 0);
    size_t pos = index(key);
    if(K[pos] == (key_t)key) return V[pos]; // need to cast to key_t because key may be truncated due to size of key_t
    else return 0;
  }

};

#endif
