#ifndef TRANSPOSITION_TABLE_H
#define TRANSPOSITION_TABLE_H

#include <cstring>
#include <cassert>
#include <type_traits>
#include <bits/stdc++.h>

/**
 * util functions to compute next prime at compile time
 */
constexpr uint64_t med(uint64_t min, uint64_t max) {
  return (min + max) / 2;
}
/**
 * tells if an integer n has a a divisor between min (inclusive) and max (exclusive)
 */
constexpr bool has_factor(uint64_t n, uint64_t min, uint64_t max) {
  return min * min > n ? false : // do not search for factor above sqrt(n)
         min + 1 >= max ? n % min == 0 :
         has_factor(n, min, med(min, max)) || has_factor(n, med(min, max), max);
}

  //return next prime number
constexpr uint64_t next_prime(uint64_t n) {
  return has_factor(n, 2, n) ? next_prime(n + 1) : n;
}

/**
 * Abstrac interface for the Transposition Table get function
 */
template<class key_t, class value_t>
class TableGetter {
 private:
  virtual void* getKeys() = 0;
  virtual void* getValues() = 0;
  virtual size_t
  getSize() = 0;
  virtual int getKeySize() = 0;
  virtual int getValueSize() = 0;

 public:
  virtual value_t get(key_t key) const = 0;
  virtual ~TableGetter() {};

 friend class OpeningBook;
};

// uint_t<S> is a template type providing an unsigned int able to fit interger of S bits.
// uint_t<8> = uint8_t and uint_t<9> = uint_16t
template<int S> using uint_t =
  typename std::conditional < S <= 8, uint_least8_t,
  typename std::conditional < S <= 16, uint_least16_t,
  typename std::conditional<S <= 32, uint_least32_t,
  uint_least64_t>::type>::type >::type;

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
template<class partial_key_t, class key_t, class value_t, int log_size>
class TranspositionTable : public TableGetter<key_t, value_t> {
  private:

  static const size_t size = next_prime(1 << log_size); // size of the transition table. Have to be odd to be prime with 2^sizeof(key_t)
                                                        // using a prime number reduces collisions
  void* getKeys()    override {return Key;}
  void* getValues()  override {return Value;}
  size_t getSize()   override {return size;}
  int getKeySize()   override {return sizeof(partial_key_t);}
  int getValueSize() override {return sizeof(value_t);}

  partial_key_t *Key;
  value_t *Value;

  size_t index(uint64_t key) const {
    return key%size;
  }

  public:
  
  TranspositionTable() {
    Key = new partial_key_t[size];
    Value = new value_t[size];
    reset();
  }
  
  ~TranspositionTable() {
    delete[] Key;
    delete[] Value;
  }

  // fill everything with 0, because 0 value means
  void reset() {
    memset(Key, 0, size * sizeof(partial_key_t));
    memset(Value, 0, size * sizeof(value_t));
  }

  // store
  void put(uint64_t key, value_t value) {
    size_t pos = index(key);
    Key[pos] = key;
    Value[pos] = value;
  }

  // get
  value_t get(uint64_t key) const override {
    size_t pos = index(key);
    if(Key[pos] == (partial_key_t)key) {
      return Value[pos];
    }
    else return 0;
  }

};

#endif
