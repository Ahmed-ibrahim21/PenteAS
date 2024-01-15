
import game.Board as Board
import logic.Logic as Logic
import agents.MinimaxAgent as MinimaxAgent
from copy import copy, deepcopy

class Game:
    def __init__(self, agent1=None, agent2=None):
        self.board = Board.Board()
        self.session_active = False
        self.current_turn = 1 # start with player 1
        self.has_win = False
        self.winner = -1
        self.agents = [None, agent1, agent2]
        self.past_board = None

    def start_game(self):
        self.session_active = True
        self.run_game()
        return self.winner

    def reset(self):
        self.board = Board.Board()
        self.session_active = False
        self.current_turn = 1
        self.has_win = False
        self.winner = -1

    # Game will run until it is a human's turn
    def run_game(self):
        is_run = False
        while self.agents[self.current_turn] and self.session_active and (not self.has_win):
            is_run = True
            self.play(*self.agents[self.current_turn].get_move(self.current_turn, self.board))
        return is_run

    def play(self, r, c):
        if r < 0 or r > 18 or c < 0 or c > 18:
            print("Invalid position specified!")
            print("Player " + str(self.current_turn) + "'s turn!")
            return

        if not self.board.spot_empty(r, c):
            print ("Position is occupied!")
            print("Player " + str(self.current_turn) + "'s turn!")
            return

        self.past_board = deepcopy(self.board)

        self.board.play(self.current_turn, r, c)

        self.board_verify() # Verify the current board

        if Logic.check_win(self.board, r, c, self.current_turn):
            print("Player " + str(self.current_turn) + ' wins!')
            self.winner = self.current_turn
            other_player = 1 if self.current_turn is 2 else 2
            if self.agents[other_player] and self.agents[other_player].is_learning:
                self.agents[other_player].update_heuristic_vals(self.board, self.winner, win=True)
            print("Game ended.")
            self.has_win = True
            return

        self.current_turn = 2 if self.current_turn is 1 else 1
        if not self.run_game():
            print("Player " + str(self.current_turn) + "'s turn!")

    def board_verify(self):
        removed = {1: 0, 2: 0}
        for row in range(0, 19):
            for col in range(0, 19):
                piece = self.past_board.get_piece(row, col)
                if piece != 0:
                    if self.board.get_piece == 0:
                        removed[piece] += 1
        captures_old = {1: self.past_board.get_captures(1), 2: self.past_board.get_captures(2)}
        captures_new = {1: self.board.get_captures(1), 2: self.board.get_captures(2)}
        for key, value in removed.items():
            opponent = 2 if key == 1 else 1
            if value%2 != 0:
                raise Exception("ERROR: ODD NUMBER OF PIECES REMOVED FROM THE BOARD")
            if captures_new[opponent] != captures_old[opponent] + (value/2):
                raise Exception("ERROR: INVALID KEY REMOVAL DETECTED $WAGMONEYYOLO420BLAZEIT")

                    


