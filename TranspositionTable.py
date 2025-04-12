import numpy as np
from typing import TypeVar, Generic, Any

def is_prime(n: int) -> bool:
    """Kiểm tra xem một số có phải là số nguyên tố không"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n: int) -> int:
    """Tìm số nguyên tố tiếp theo lớn hơn hoặc bằng n"""
    if n <= 1:
        return 2
    prime = n
    found = False
    while not found:
        prime += 1 if prime % 2 == 0 else 2  # Chỉ kiểm tra số lẻ
        if is_prime(prime):
            found = True
    return prime

# Định nghĩa kiểu dữ liệu
KeyT = TypeVar('KeyT')
ValueT = TypeVar('ValueT')

class TableGetter(Generic[KeyT, ValueT]):
    """Abstract interface for the Transposition Table get function."""
    def get(self, key: KeyT) -> ValueT:
        raise NotImplementedError
    
    def get_keys(self):
        raise NotImplementedError
    
    def get_values(self):
        raise NotImplementedError
    
    def get_size(self) -> int:
        raise NotImplementedError
    
    def get_key_size(self) -> int:
        raise NotImplementedError
    
    def get_value_size(self) -> int:
        raise NotImplementedError


# uint_t<S> is a template type providing an unsigned int able to fit interger of S bits.
# uint_t<8> = uint8_t and uint_t<9> = uint_16t
def uint_t(S):
    """Chọn kiểu uint phù hợp dựa trên số bit S"""
    if S <= 8:
        return np.uint8
    elif S <= 16:
        return np.uint16
    elif S <= 32:
        return np.uint32
    else:
        return np.uint64
    

class TranspositionTable(TableGetter[KeyT, ValueT]):
    """
    Transposition Table là một hash table đơn giản với kích thước lưu trữ cố định.
    Trong trường hợp xung đột, chúng ta giữ mục nhập cuối cùng và ghi đè mục trước đó.
    
    Số lượng mục được lưu trữ là một lũy thừa của hai được xác định khi tạo.
    """
    
    def __init__(self, log_size: int):
        self.size = next_prime(1 << log_size)  # size of the transition table
        self.keys = [0] * self.size
        self.values = [0] * self.size
        self.reset()
        
    def reset(self):
        """Fill everything with 0."""
        self.keys = [0] * self.size
        self.values = [0] * self.size
        
    def index(self, key: int) -> int:
        """Calculate index in the table from key."""
        return key % self.size
    
    def put(self, key: int, value: ValueT):
        """Store a value with the given key."""
        pos = self.index(key)
        self.keys[pos] = key
        self.values[pos] = value
        
    def get(self, key: int) -> ValueT:
        """Get a value by key."""
        pos = self.index(key)
        if self.keys[pos] == key:
            return self.values[pos]
        else:
            return 0
    
    def get_keys(self):
        """Get all keys."""
        return self.keys
    
    def get_values(self):
        """Get all values."""
        return self.values
    
    def get_size(self) -> int:
        """Get size of the table."""
        return self.size
    
    def get_key_size(self) -> int:
        """Get key size in bytes (approximate in Python)."""
        return 8  # 64-bit integer
    
    def get_value_size(self) -> int:
        """Get value size in bytes (approximate in Python)."""
        return 1  # uint8_t in original