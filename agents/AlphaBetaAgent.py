from logic.Logic import heuristic_count, check_win
from copy import copy, deepcopy
import random, math

class Agent:
    def __init__(self):
        self.is_learning = False
        self.H_VALS = {
                1: 0,
                2: 5,
                3: 20,
                4: 50,
                5: 1000,
                'capture': 10
                }

    def get_move(self, pid, board):
        if len(board.empty_adjacent) == 0:
            move = (math.floor(random.random()*18), math.floor(random.random()*18))
            return move
        else:
            a = self.pentemax(board, 2)[0]
            return a

    def value_state(self, board, pid):
        other_pid = 2 if pid == 1 else 1
        state_val = 0
        for (r,c) in board.occupied:
            curr_raw = heuristic_count(board, r, c, pid)
            for key in curr_raw.keys():
                count = curr_raw[key]
                if key in self.H_VALS.keys():
                    state_val += self.H_VALS[key]
                else:
                    if count in self.H_VALS.keys():
                        state_val += self.H_VALS[count]
                    else:
                        state_val += 1000 # not in dict, must be greater than 5
        return state_val 

    def pentemax(self, board, recursion, alpha=-float('inf'), beta=float('inf')):
        val1 = self.value_state(deepcopy(board), 1)
        val2 = self.value_state(deepcopy(board), 2)
        pid = 1 if val1 > val2 else 2
        max_val = -1
        best_move = (-1, -1)

        if recursion == 0:
            for (r, c) in board.empty_adjacent:
                new_board = deepcopy(board).play(pid, r, c)
                new_val = self.value_state(new_board, pid)
                if new_val > max_val:
                    max_val = new_val
                    best_move = (r, c)
                alpha = max(alpha, max_val)
                if alpha >= beta:
                    break  # Beta cut-off
            return (best_move, max_val)

        else:
            for (r, c) in board.empty_adjacent:
                new_board = deepcopy(board).play(pid, r, c)
                new_val = self.value_state(new_board, pid)

                pentemax_max_val = -1
                if new_val > max_val:
                    pentemax_max_val_curr = self.pentemax(new_board, recursion - 1, alpha, beta)[1] * recursion
                    if pentemax_max_val_curr > pentemax_max_val:
                        max_val = new_val
                        best_move = (r, c)

                alpha = max(alpha, max_val)
                if alpha >= beta:
                    break  # Beta cut-off
            return (best_move, max_val)