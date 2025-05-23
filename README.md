# Connect4 AI bot

### Members of group
    - Thái Khắc Mạnh 23021620
    - Nguyễn Văn Phúc 23021664
    - Trần Duy Thành 23021720
    - Thiều Quang Huy 23021580

As mentioned in the [report](<./Báo-cáo-BTL-Trí-tuệ-nhân-tạo.pdf>), each team member implemented their own version of the code and competed to select the final bot. Afterwards, everyone collaborated to fine-tune it for the competition. Other versions of the bot can be found in the different branches of this repository.
## Introduction
This Connect 4 AI bot employs the Minimax search algorithm, enhanced with Alpha-Beta pruning and several optimization techniques, to compute the strongest possible move for any given Connect 4 board state.<br/>
Together, these techniques enable our program to search to depths of 9–11 moves within the given time limit (about 10 seconds), meaning it can select an optimal move by looking ahead 9–10 moves.

## Algorithm and key techniques
Negamax with Alpha-Beta Pruning: Core depth-first search, simplifying Minimax by using a single recursive function.

Heuristic Evaluation: Provides estimated scores at leaf nodes when maximum depth or time limit is reached.

Iterative Deepening: Repeated searches from depth 1 upward to manage time flexibly and reuse move-ordering information.

Transposition Table: Hash table caching position evaluations to avoid redundant calculations.

Move Ordering: Orders moves by likely strength to maximize early pruning (from previous search, from transposition table, and other).

Additionally, several other techniques are employed, such as blocking the opponent’s immediate winning moves, reusing the best move found in the previous iterative deepening search, and applying center-out move ordering.

For a more detailed explanation, please read [here](<./Báo-cáo-BTL-Trí-tuệ-nhân-tạo.pdf>) and [demo video](<https://drive.google.com/file/d/1ObkfesKQAoNKdVO-beNFv3zauSsQ6Niu/view?usp=sharing>)


