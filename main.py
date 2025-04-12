
"""
This file is part of Connect4 Game Solver <http://connect4.gamesolver.org>
Copyright (C) 2017-2019 Pascal Pons <contact@gamesolver.org>

Connect4 Game Solver is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Connect4 Game Solver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Connect4 Game Solver. If not, see <http://www.gnu.org/licenses/>.
"""

from solver import Solver
from board import Board


def main():
    """
    Main function.
    Reads Connect 4 positions, line by line, from standard input
    and writes one line per Board to standard output containing:
    - score of the Board

    Any invalid Board (invalid sequence of move, or already won game)
    will generate an error message to standard error and an empty line to standard output.
    """
    solver = Solver(Board)
    
    try:
        line = input()
        p = Board()
        if p.play_sequence(line) != len(line):
            print("invalid")
        else:
            score = solver.solve(p)
            print(score)
    except EOFError:
        pass


if __name__ == "__main__":
    main()