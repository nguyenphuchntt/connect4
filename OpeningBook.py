import struct
from typing import Optional
import sys

from TranspositionTable import TranspositionTable, TableGetter

class OpeningBook:
    """
    Python implementation of the Connect4 OpeningBook that was originally in C++.
    
    The opening book contains pre-calculated best moves for early game positions.
    """
    
    def __init__(self, width: int, height: int, depth: int = -1, table: Optional[TableGetter] = None):
        """
        Initialize an opening book.
        
        Parameters:
        -----------
        width : int
            Width of the board
        height : int
            Height of the board
        depth : int
            Maximum depth of stored positions
        table : TableGetter, optional
            The transposition table to use
        """
        self.T = table
        self.width = width
        self.height = height
        self.depth = depth
    
    def init_transposition_table(self, partial_key_bytes: int, log_size: int) -> Optional[TableGetter]:
        """
        Initialize a transposition table with the given parameters.
        
        Parameters:
        -----------
        partial_key_bytes : int
            Size of the partial key in bytes
        log_size : int
            Log base 2 of the table size
        
        Returns:
        --------
        TableGetter or None
            The initialized transposition table or None if initialization failed
        """
        if log_size < 21 or log_size > 27:
            print(f"Unimplemented OpeningBook size: {log_size}", file=sys.stderr)
            return None
        
        if partial_key_bytes not in [1, 2, 4]:
            print(f"Invalid internal key size: {partial_key_bytes} bytes", file=sys.stderr)
            return None
        
        return TranspositionTable(log_size)
    
    def load(self, filename: str):
        """
        Load an opening book from a file.
        
        Opening book file format:
        - 1 byte: board width
        - 1 byte: board height
        - 1 byte: max stored Board depth
        - 1 byte: key size in bits
        - 1 byte: value size in bits
        - 1 byte: log_size = log2(size). number of stored elements (size) is smallest prime number above 2^(log_size)
        - size key elements
        - size value elements
        
        Parameters:
        -----------
        filename : str
            Path to the opening book file
        """
        self.depth = -1
        self.T = None
        
        try:
            with open(filename, 'rb') as f:
                print(f"Loading opening book from file: {filename}. ", end="", file=sys.stderr)
                
                # Read header information
                _width = ord(f.read(1))
                if _width != self.width:
                    print(f"Unable to load opening book: invalid width (found: {_width}, expected: {self.width})", file=sys.stderr)
                    return
                
                _height = ord(f.read(1))
                if _height != self.height:
                    print(f"Unable to load opening book: invalid height (found: {_height}, expected: {self.height})", file=sys.stderr)
                    return
                
                _depth = ord(f.read(1))
                if _depth > self.width * self.height:
                    print(f"Unable to load opening book: invalid depth (found: {_depth})", file=sys.stderr)
                    return
                
                partial_key_bytes = ord(f.read(1))
                if partial_key_bytes > 8:
                    print(f"Unable to load opening book: invalid internal key size (found: {partial_key_bytes})", file=sys.stderr)
                    return
                
                value_bytes = ord(f.read(1))
                if value_bytes != 1:
                    print(f"Unable to load opening book: invalid value size (found: {value_bytes}, expected: 1)", file=sys.stderr)
                    return
                
                log_size = ord(f.read(1))
                if log_size > 40:
                    print(f"Unable to load opening book: invalid log2(size) (found: {log_size})", file=sys.stderr)
                    return
                
                # Initialize transposition table
                self.T = self.init_transposition_table(partial_key_bytes, log_size)
                if self.T is None:
                    print("Unable to initialize opening book", file=sys.stderr)
                    return
                
                # Read keys and values
                keys_data = f.read(self.T.get_size() * partial_key_bytes)
                values_data = f.read(self.T.get_size())
                
                if len(keys_data) != self.T.get_size() * partial_key_bytes or len(values_data) != self.T.get_size():
                    print("Unable to load data from opening book", file=sys.stderr)
                    return
                
                # Parse keys and values
                keys = self.T.get_keys()
                values = self.T.get_values()
                
                # Fill keys and values
                for i in range(self.T.get_size()):
                    if partial_key_bytes == 1:
                        keys[i] = keys_data[i]
                    elif partial_key_bytes == 2:
                        keys[i] = struct.unpack('<H', keys_data[i*2:(i+1)*2])[0]
                    elif partial_key_bytes == 4:
                        keys[i] = struct.unpack('<I', keys_data[i*4:(i+1)*4])[0]
                    values[i] = values_data[i]
                
                self.depth = _depth  # Set depth only on success
                print("done", file=sys.stderr)
                
        except FileNotFoundError:
            print(f"Unable to load opening book: {filename}", file=sys.stderr)
        except Exception as e:
            print(f"Error loading opening book: {e}", file=sys.stderr)
    
    def get(self, board) -> int:
        """
        Get the score for a board position from the opening book.
        
        Parameters:
        -----------
        board : Board
            The board position to look up
        
        Returns:
        --------
        int
            The score for the position or 0 if not found
        """
        if self.T is None or board.nb_moves() > self.depth:
            return 0
        return self.T.get(board.key3())
    
    def __del__(self):
        """Clean up resources."""
        self.T = None