
import os, math
from logic.Logic import heuristic_count
PCOL = ['\033[92m','\033[91m']
ENDC = '\033[0m'

class Printer:
    def __init__(self):
        try:
            size = os.get_terminal_size()
            self.print_enabled = True
            self.rows = size.lines
            self.columns = min([size.columns, 50])
        except OSError:
            self.print_enabled = False
            self.rows = 1
            self.columns = 50
            
    def printable_title(self, text):
        text = ' ' + text.strip(' ') + ' '
        border_float = (self.columns - len(text))/2
        left_border = int(math.ceil(border_float))
        right_border = int(math.floor(border_float))
        return (('-'*left_border) + text + ('-'* right_border))


    def printable_option(self, text):
        return (' '*5 + text)

    def print_heading(self, text):
        if not self.print_enabled:
            return
        print() # print an empty line before all prints
        print_text = self.printable_title(text)
        print(print_text)

    def print_sep(self):
        if not self.print_enabled:
            return
        print('-' * self.columns)
        print()

    def print_option(self, text):
        if not self.print_enabled:
            return
        print_text = self.printable_option(text)
        print(print_text)

    def board_printer(self, game_board):
        self.print_heading('Game Board')
        self.print_sep()
        print('  ' + ' __'*19)
        topstr = '  '  +  ('|  '*19) + '|'
        botstr = '  ' + ('|__'*19) + '|'
        rowidx = 0
        for row in game_board.grid:
            rowidx += 1
            colidx = 0
            curr_str = (' ' + str(rowidx) if rowidx < 10 else str(rowidx)) + '|'
            for column in row:
                colidx += 1
                curr_str += ''
                curr_str = curr_str + ((' ' + str(colidx) if colidx < 10 else str(colidx))  if column == 0 else PCOL[column-1] + 'P' + str(column)) + ENDC + '|'
            #print(topstr)
            print(curr_str)
            print(botstr)

    def print_captures(self, game_board, player=None):
        if player:
            print('Player ' + str(player) + ' has ' + str(game_board.captures[player]) + '.')
        else:
            for i in game_board.captures:
                print('Player ' + str(i) + ' has ' + str(game_board.captures[i]) + '.')

    def print_heuristic(self, game_board, r, c, player):
        print(str(heuristic_count(game_board, r, c, player)))


