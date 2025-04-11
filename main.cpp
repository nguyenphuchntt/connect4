/*
 * This file is part of Connect4 Game Solver <http://connect4.gamesolver.org>
 * Copyright (C) 2017-2019 Pascal Pons <contact@gamesolver.org>
 *
 * Connect4 Game Solver is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * Connect4 Game Solver is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Connect4 Game Solver. If not, see <http://www.gnu.org/licenses/>.
 */

 #include "solver.h"
 #include <iostream>
 
 /**
  * Main function.
  * Reads Connect 4 positions, line by line, from standard input
  * and writes one line per Board to standard output containing:
  *  - score of the Board
  *  - number of nodes explored
  *  - time spent in microsecond to solve the Board.
  *
  *  Any invalid Board (invalid sequence of move, or already won game)
  *  will generate an error message to standard error and an empty line to standard output.
  */
 int main() {
    Solver solver;
    
    std::string opening_book = "7x6.book";
    solver.loadBook(opening_book);
    
    std::string line;
    std::cin >> line;
    Board P;
    if(P.play(line) != line.size()) {
    std::cout << "invalid";
    } else {
    int score = solver.solve(P);
    std::cout << score;
    }
   
 }
 