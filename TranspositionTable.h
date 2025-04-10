#ifndef TRANSPOSITION_TABLE_H
#define TRANSPOSITION_TABLE_H

#include <cstring>
#include <cassert>
#include <type_traits>
#include <bits/stdc++.h>

constexpr uint64_t med(uint64_t min, uint64_t max) {
  return (min + max) / 2;
}
/*
 * tells if an integer n has a a divisor between min (inclusive) and max (exclusive)
 */
constexpr bool has_factor(uint64_t n, uint64_t min, uint64_t max) {
  return min * min > n ? false :
    min + 1 >= max ? n % min == 0 :
    has_factor(n, min, med(min, max)) || has_factor(n, med(min, max), max);
}

// return next prime number greater or equal to n.
// n must be >= 2
constexpr uint64_t next_prime(uint64_t n) {
  return has_factor(n, 2, n) ? next_prime(n + 1) : n;
}

template<unsigned int key_size, unsigned int value_size, unsigned int log_size>
class TranspositionTable {
  private:
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
  key_t *Key;
  value_t *Value;

  size_t index(uint64_t key) const {
    return key%size;
  }

  public:
  
  TranspositionTable() {
    Key = new key_t[size];
    Value = new value_t[size];
    reset();
  }
  
  ~TranspositionTable() {
    delete[] Key;
    delete[] Value;
  }

  // fill everything with 0, because 0 value means
  void reset() {
    memset(Key, 0, size * sizeof(key_t));
    memset(Value, 0, size * sizeof(value_t));
  }

  // store
  void put(uint64_t key, value_t value) {
    size_t pos = index(key);
    Key[pos] = key;
    Value[pos] = value;
  }

  // get
  value_t get(uint64_t key) const {
    size_t pos = index(key);
    if(Key[pos] == (key_t)key) {
      return Value[pos];
    }
    else return 0;
  }

};

#endif
