# Casey Levy
# CS 325 - Portfolio Project
# Sudoku

# Code inspired/referenced from the following:
# https://www.youtube.com/watch?v=eqUwSA0xI-s&feature=emb_logo
# https://www.geeksforgeeks.org/sudoku-backtracking-7/
# https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
# https://www.youtube.com/watch?v=auK3PSZoidc

import pygame as pg

pg.font.init()
import time
from random import sample
from sudoku_cert import solve_game, verify_move, check_solution


# Class for each box in the game
class GameBox:
    game_rows, game_cols = 9, 9

    def __init__(self, val, game_row, game_col, width, height):
        self.val = val
        self.game_row, self.game_col = game_row, game_col
        self.temp_val = 0
        self.width, self.height = width, height
        self.select = False

    # Creating a box
    def make_box(self, game_win):
        game_font = pg.font.SysFont(None, 40)
        space = self.width / 9
        r = self.game_row * space
        c = self.game_col * space

        if self.temp_val != 0 and self.val == 0:
            game_text = game_font.render(str(self.temp_val), 1, (128, 128, 128))
            game_win.blit(game_text, (c + 5, r + 5))

        elif not self.val == 0:
            game_text = game_font.render(str(self.val), 1, (0, 0, 0))
            game_win.blit(game_text,
                          (c + (space / 2 - game_text.get_width() / 2), r + (space / 2 - game_text.get_height() / 2)))

        if self.select:
            pg.draw.rect(game_win, (255, 0, 0), (c, r, space, space), 3)

    def set_value(self, value):
        self.val = value

    def set_temp_value(self, value):
        self.temp_val = value


# Class for buttons to solve, verify, and reset board
class GameButton:
    def __init__(self, colored, i, j, width, height, button_text=''):
        self.colored = colored
        self.i, self.j = i, j
        self.button_text = button_text
        self.width, self.height = width, height

    # Checking mouse position
    def mouse_over(self, position):
        if position[0] > self.i and position[0] < self.i + self.width:
            if position[1] > self.j and position[1] < self.j + self.height:
                return True

        return False

    def color(self, colored):
        self.colored = colored

    # Creating the buttons
    def make_button(self, game_win, text_outline=None):
        if text_outline:
            pg.draw.rect(game_win, text_outline, (self.i - 2, self.j - 2, self.width + 4, self.height + 4), 0)
        pg.draw.rect(game_win, self.colored, (self.i, self.j, self.width, self.height), 0)

        if self.button_text != '':
            game_font = pg.font.SysFont(None, 25)
            game_text = game_font.render(self.button_text, 1, (255, 255, 255))
            game_win.blit(game_text, (self.i + (self.width / 2 - game_text.get_width() / 2),
                                      self.j + (self.height / 2 - game_text.get_height() / 2)))


# Class for the 9x9 board
class GameBoard:
    board = [[0 for x in range(9)] for y in range(9)]

    def __init__(self, game_row, game_col, width, height):
        self.game_row, self.game_col = game_row, game_col
        self.width, self.height = 540, 540
        self.game_model = None
        self.game_base = 3
        self.select = None
        self.game_side = self.game_base * self.game_base
        self.build_board()

        self.game_boxes = [[GameBox(self.game_board[x][y], x, y, 540, 540) for x in range(game_col)] for y in
                           range(game_row)]

    # Creating the board
    def build_board(self):
        row_base = range(self.game_base)
        r = [x * self.game_base + row for x in self.shuffle_board(row_base) for row in self.shuffle_board(row_base)]
        c = [x * self.game_base + col for x in self.shuffle_board(row_base) for col in self.shuffle_board(row_base)]

        number = self.shuffle_board(range(1, self.game_base * self.game_base + 1))
        game_board = [[number[self.move_pattern(row, col)] for col in c] for row in r]  # Randomizing the board
        spaces = self.game_side * self.game_side
        empty_space = spaces * 3 // 4

        for i in sample(range(spaces), empty_space):
            game_board[i // self.game_side][i % self.game_side] = 0

        self.game_board = game_board

    def shuffle_board(self, shuffle):
        return sample(shuffle, len(shuffle))

    def move_pattern(self, row, col):
        return (self.game_base * (row % self.game_base) + row // self.game_base + col) % self.game_side

    # Player's moves
    def move(self, value):
        r, c = self.select
        if self.game_boxes[r][c].val == 0:
            self.game_boxes[r][c].set_value(value)
            self.model()

            if verify_move(self.game_model, value, (r, c)) and solve_game(self.game_model):
                return True

            else:
                self.game_boxes[r][c].set_value(0)
                self.game_boxes[r][c].set_temp_value(0)
                self.model()
                return False

    def model(self):
        self.game_model = [[self.game_boxes[x][y].val for x in range(self.game_col)] for y in range(self.game_row)]

    def solve(self):
        self.game_board = solve_game(self.game_board)

    def make(self, game_win):
        space = self.width / 9
        for x in range(self.game_row + 1):
            if x % 3 == 0 and x != 0:
                pad = 4
            else:
                pad = 1

            pg.draw.line(game_win, (0, 128, 128), (0, x * space), (self.width, x * space), pad)
            pg.draw.line(game_win, (0, 128, 128), (x * space, 0), (x * space, self.height), pad)

        for x in range(self.game_row):
            for y in range(self.game_col):
                self.game_boxes[x][y].make_box(game_win)

    def make_temp(self, value):
        r, c = self.select
        self.game_boxes[r][c].set_temp_value(value)

    def solved_board(self, game_win):
        self.game_boxes = [[GameBox(self.game_board[x][y], x, y, 540, 540) for y in range(self.game_col)] for x in
                           range(self.game_row)]
        space = self.width / 9
        for x in range(self.game_row + 1):
            if x % 3 == 0 and x != 0:
                pad = 4
            else:
                pad = 1

            pg.draw.line(game_win, (0, 0, 0), (0, x * space), (self.width, x * space), pad)
            pg.draw.line(game_win, (0, 0, 0), (x * space, 0), (x * space, self.height), pad)

        for x in range(self.game_row):
            for y in range(self.game_col):
                self.game_boxes[x][y].make_box(game_win)

    # Method to clear a box the user placed a number in
    def clear(self):
        r, c = self.select
        if self.game_boxes[r][c].val == 0:
            self.game_boxes[r][c].set_temp_value(0)

    # If box is clicked by the user
    def click_box(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            space = self.width / 9
            r = pos[0] // space
            c = pos[1] // space
            return (int(r), int(c))
        else:
            return None

    # Player selection
    def selection(self, r, c):
        for x in range(self.game_row):
            for y in range(self.game_col):
                self.game_boxes[x][y].select = False
        self.game_boxes[r][c].select = True
        self.select = (r, c)

    # Completed board
    def board_complete(self):
        for x in range(self.game_row):
            for y in range(self.game_col):
                if self.game_boxes[x][y].val == 0:
                    return False
        return True

# Setting up timer
def time_setup(sec):
    minute = sec // 60
    s = sec % 60
    game_time = " " + str(minute) + ":" + str(s)
    return game_time

# Resetting the board
def reset(game_win, solve, verify, reset_board, game_board, game_time, player_move):
    game_win.fill((255, 255, 255))
    game_font = pg.font.SysFont(None, 34)
    game_text = game_font.render(time_setup(game_time), 1, (0, 0, 0))
    game_win.blit(game_text, (450, 545))
    game_text = game_font.render(str(player_move), 1, (0, 128, 128))
    game_win.blit(game_text, (20, 545))
    solve.make_button(game_win)
    verify.make_button(game_win)
    reset_board.make_button(game_win)
    game_board.make(game_win)

# Main program method
def main():
    game_window = pg.display.set_mode((540, 600))
    pg.display.set_caption("SUDOKU")
    game_board = GameBoard(9, 9, 600, 600)
    button_reset = GameButton((255, 0, 191,), 250, 545, 60, 25, button_text="Reset")
    button_verify = GameButton((191, 0, 255), 320, 545, 60, 25, button_text="Verify")
    button_solve = GameButton((0, 128, 128), 390, 545, 60, 25, button_text="Solve!")
    key = None
    game_run = True
    game_start = time.time()
    player_move = ""
    while game_run:
        time_passed = round(time.time() - game_start)   # Game timer
        for e in pg.event.get():
            if e.type == pg.QUIT:
                game_run = False

            if e.type == pg.KEYDOWN:    # Code for user number entries
                if e.key == pg.K_1:
                    key = 1
                if e.key == pg.K_2:
                    key = 2
                if e.key == pg.K_3:
                    key = 3
                if e.key == pg.K_4:
                    key = 4
                if e.key == pg.K_5:
                    key = 5
                if e.key == pg.K_6:
                    key = 6
                if e.key == pg.K_7:
                    key = 7
                if e.key == pg.K_8:
                    key = 8
                if e.key == pg.K_9:
                    key = 9

                if e.key == pg.K_DELETE:   # If user wants to delete a number in a box
                    game_board.clear()
                    key = None

                if e.type == pg.K_RETURN:
                    x, y = game_board.select
                    if game_board.game_boxes[x][y].temp_val != 0:
                        if game_board.move(game_board.game_boxes[x][y].temp_val):
                            player_move = "Valid"
                        else:
                            player_move = "Invalid"
                        key = None

            if e.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()

            if e.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                mouse_click = game_board.click_box(pos)
                if mouse_click:
                    game_board.selection(mouse_click[0], mouse_click[1])
                    key = None
                if button_solve.mouse_over(pos):
                    game_board.solve()
                    game_board.solved_board(game_window)
                    player_move = "Board Complete! :)"

                if button_verify.mouse_over(pos):     # Verifying solutions/attempts
                    if check_solution(game_board.game_board):
                        player_move = "Solution is Valid!"
                    else:
                        player_move = "Solution is Invalid!"

                if button_reset.mouse_over(pos):
                    game_board = GameBoard(9, 9, 540, 540)
                    player_move = ""
                    game_start = time.time()

            if game_board.board_complete() and check_solution(game_board.game_board):
                player_move = "Solution is Valid!"

        if game_board.select and key != None:
            game_board.make_temp(key)

        reset(game_window, button_solve, button_verify, button_reset, game_board, time_passed, player_move)
        pg.display.update()


main()
pg.quit()
