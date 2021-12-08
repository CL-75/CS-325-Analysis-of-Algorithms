# Casey Levy
# CS 325 - Portfolio Project
# Minesweeper

import pygame as pg
from pygame.locals import *
import random

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
M_GRAY = (100, 100, 100)
D_GRAY = (75, 75, 75)
DARK_RED = (170, 1, 20)
RED = (225, 0, 0)
DARK_BLUE = (0, 0, 120)
TURQ = (0, 153, 153)
WHITE = (250, 250, 250)
GREEN = (0, 125, 0)
BLUE = (51, 51, 255)
YELLOW = (242, 242, 109)
BACKGROUND = (211, 211, 211)

TEXT = [M_GRAY, BLACK, DARK_RED, RED, GREEN, TURQ, BLUE, DARK_BLUE]
CELL_PROX = [(0,1), (1,1), (1,0), (1,-1), (0, -1), (-1,-1), (-1,0), (-1,1)]
DIFFICULTY = [
    # Easy Difficulty
    (6, 8),
    # Med Difficulty
    (14, 35),
    # Hard Difficulty
    (22, 95)
]


# Class to display the menu
class GameMenu:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Minesweeper")
        self.screen = pg.display.set_mode((600, 650))
        self.instructions = GameButton(200, 20, 200, 100, "MINESWEEPER", BACKGROUND)
        self.game_easy = GameButton(200, 130, 200, 100, "Easy")
        self.game_med = GameButton(200, 240, 200, 100, "Medium")
        self.game_hard = GameButton(200, 350, 200, 100, "Hard")
        self.game_buttons = [self.game_easy, self.game_med, self.game_hard]


    def run_menu(self):
        game_run = True

        while game_run:
            for i in pg.event.get():
                position = pg.mouse.get_pos()
                if i.type == QUIT:
                    game_run = False
                if i.type == pg.MOUSEBUTTONDOWN:
                    if self.game_easy.mouse_over(position):
                        self.begin_game(0)
                    elif self.game_med.mouse_over(position):
                        self.begin_game(1)
                    elif self.game_hard.mouse_over(position):
                        self.begin_game(2)

                if i.type == pg.MOUSEMOTION:
                    for j in self.game_buttons:
                        if j.mouse_over(position):
                            j.color = BLUE
                        else:
                            j.color = BLACK
            self.reset_board()

    def reset_board(self):
        self.screen = pg.display.set_mode((600, 650))
        self.screen.fill(BACKGROUND)
        pg.display.set_caption("Minesweeper")
        self.instructions.make_button(self.screen)
        self.instructions.game_text_colored = D_GRAY
        self.game_easy.make_button(self.screen)
        self.game_med.make_button(self.screen)
        self.game_hard.make_button(self.screen)
        pg.display.update()

    def begin_game(self, game_difficulty):
        game = MineGame(game_difficulty)
        game.game_play()


class GameCells:
    def __init__(self, i, j, game_level, game_cells):
        self.i, self.j = i, j
        self.length = 750//game_level[0]-5
        self.i_position = 5 + (self.length+5) * self.i
        self.j_position = 105 + (self.length+5) * self.j
        self.is_visible = False
        self.is_mine = False
        self.num = 0
        self.game_flag = False
        self.game_cells = game_cells
        self.game_level = game_level
        self.colored = M_GRAY
        self.game_text_colored = None



    def make_flag(self):
        if self.game_flag == False:
            self.game_flag = True
            return True

        else:
            self.game_flag = False
            return False


    def print_cell(self):
        self.is_visible = True
        self.colored = BACKGROUND

        if self.is_mine == True:
            self.colored = DARK_RED
            return False

        if self.num == 0:
            for x in CELL_PROX:
                bounds = [-1, self.game_level[0]]
                if self.j+x[1] not in bounds and self.i+x[0] not in bounds:
                    if self.game_cells[self.j+x[1]][self.i+x[0]].is_visible == False:
                        self.game_cells[self.j+x[1]][self.i+x[0]].print_cell()


    def mouse_over(self, position):
        if position[0] > self.i_position and position[0] < self.i_position + self.length:
            if position[1] > self.j_position and position[1] < self.j_position + self.length:
                return True
        return False


    def reset_screen(self, game_win):
        pg.draw.rect(game_win, self.colored, (self.i_position, self.j_position, self.length, self.length), 0)
        if self.num != 0 and self.is_visible == True:
            game_font = pg.font.SysFont(None, 30)
            game_text = game_font.render(str(self.num), 1, self.game_text_colored)
            game_win.blit(game_text, (self.i_position+(self.length//2-game_text.get_width()//2), self.j_position+(self.length//2-game_text.get_height()//2)))


class GameButton:
    def __init__(self, i, j, width, height, game_text = '', color = GRAY):
        self.i, self.j = i, j
        self.color = color
        self.width = width
        self.height = height
        self.font = pg.font.SysFont(None, 30)
        self.game_text = game_text
        self.game_text_colored = WHITE

    def make_button(self, game_win):
        pg.draw.rect(game_win, self.color, (self.i, self.j, self.width, self.height), 0)
        if self.game_text != '':
            game_font = pg.font.SysFont(None,30)
            game_text = game_font.render(self.game_text, 1, self.game_text_colored)
            game_win.blit(game_text, (self.i+(self.width//2-game_text.get_width()//2), self.j+(self.height//2-game_text.get_height()//2)))


    def mouse_over(self, position):
        if position[0] > self.i and position[0] < self.i+self.width:
            if position[1] > self.j and position[1] < self.j+self.height:
                return True
        return False


class MineGame:
    def __init__(self, game_difficulty):
        pg.init()
        self.screen = pg.display.set_mode((850, 1000))
        self.game_level = DIFFICULTY[game_difficulty]
        pg.display.set_caption("Minesweeper")
        self.game_flag = 0
        self.game_state = "IN_PROGRESS"
        self.font = pg.font.SysFont(None, 30)
        self.verify = GameButton(500, 20, 220, 60, "Verify Flags", M_GRAY)
        self.game_cells = []

        for i in range(self.game_level[0]):
            self.game_cells.append([])
            for j in range(self.game_level[0]):
                self.game_cells[i].append(GameCells(j, i, self.game_level, self.game_cells))

        for a in range(self.game_level[1]):
            search = True
            while search:
                j = random.randint(0, self.game_level[0]-1)
                i = random.randint(0, self.game_level[0]-1)
                if self.game_cells[i][j] == False:
                    self.game_cells[i][j].is_mine = True
                    search = False

        for cell in self.game_cells:
            for position in cell:
                for x in CELL_PROX:
                    if position.is_mine == False:
                        bounds = [-1, self.game_level[0]]
                        if position.i+x[1] not in bounds and position.j+x[0] not in bounds:
                            if self.game_cells[position.i+x[1]][position.j+x[0]] == True:
                                position.cell_number += 1
                if position.cell_number != 0:
                    position.cell_text_color = TEXT[position.cell_number-1]

        search = True
        while search:
            j = random.randint(0, self.game_level[0] - 1)
            i = random.randint(0, self.game_level[0] - 1)
            if self.game_cells[i][j].cell_number == 0 and self.game_cells[i][j].is_mine == False:
                self.game_cells[i][j].print_cell()
                search = False

    def display(self):
        if self.game_state == "IN_PROGRESS":
            game_text = self.font.render("MINES: " + str(self.game_level[1]), True, D_GRAY)
            game_text_i = game_text.get_rect().width
            game_text_j = game_text.get_rect().height

            self.screen.blit(game_text, ((150-(game_text_i//2)), (50-(game_text_j//2))))
            game_text = self.font.render("FLAGS: " + str(self.game_flag), True, D_GRAY)
            game_text_i = game_text.get_rect().width
            game_text_j = game_text.get_rect().height
            self.screen.blit(game_text, ((350-(game_text_i//2)), (50-(game_text_j//2))))
            self.verify.make_button(self.screen)

        elif self.game_state == "YOU LOST! :(":
            game_text = self.font.render("Game Over!", True, BLACK)
            game_text_i = game_text.get_rect().width
            game_text_j = game_text.get_rect().height
            self.screen.blit(game_text, ((150-(game_text_i//2)), (50-(game_text_j//2))))

        elif self.game_state == "YOU WON! :)":
            game_text = self.font.render("You're A Winner!", True, BLACK)
            game_text_i = game_text.get_rect().width
            game_text_j = game_text.get_rect().height
            self.screen.blit(game_text, ((150-(game_text_i//2)), (50-(game_text_j//2))))

    def board_cells(self):
        for i in self.game_cells:
            for j in i:
                j.reset_board()

    def game_play(self):
        game_run = True
        game_pause = False

        while game_run:
            for i in pg.event.get():
                position = pg.mouse.get_pos()
                if i.type == QUIT:
                    game_run = False
                if not game_pause:
                    if i.type == pg.MOUSEMOTION:
                        for r in self.game_cells:
                            for c in r:
                                if c.game_flag == True:
                                    c.colored = YELLOW
                                elif c.is_visible == False and c.game_flag == False:
                                    if c.mouse_over(position):
                                        c.colored = D_GRAY
                                    else:
                                        c.colored = M_GRAY

                        if self.verify.mouse_over(position):
                            self.verify.colored = D_GRAY

                        else:
                            self.verify.colored = M_GRAY

                    if i.type == pg.MOUSEBUTTONDOWN:
                        if i.game_button == 3:
                            for r in self.game_cells:
                                for c in r:
                                    if c.is_visible == False:
                                        if c.mouse_over(position):
                                            game_flag = c.set_game_flag()
                                            if game_flag == True:
                                                self.game_flag += 1
                                                c.colored = YELLOW
                                            else:
                                                self.game_flag -= 1
                                                c.colored = D_GRAY

                        if i.game_button == 1:
                            for r in self.game_cells:
                                for c in r:
                                    if c.is_visible == False:
                                        if c.mouse_over(position):
                                            game_state = c.print_cell()
                                            if game_state == False:
                                                self.game_state = "YOU LOST! :("
                                                game_pause = True

                                            if c.game_flag == True:
                                                c.game_flag = False
                                                c.colored = BACKGROUND
                                                self.game_flag -= 1

                            if self.verify.mouse_over(position):
                                is_verified = self.verify_game_flags()
                                if is_verified:
                                    print("This solution may work.")
                                else:
                                    print("This solution will not work or you have not flagged enough mines.")


            game_win = self.game_victory()
            if game_win == True:
                self.game_state = "YOU WON! :)"
                game_pause = True

            self.reset_board()


    def verify_game_flags(self):
        for r in self.game_cells:
            for c in r:
                if c.is_visible == True:
                    neighboring = 0
                    for a in CELL_PROX:
                        bounds = [-1, c.game_level[0]]
                        if c.i+a[1] not in bounds and c.j+a[0] not in bounds:
                            adj = self.game_cells[c.i+a[1]][c.j+a[0]]
                            if adj.game_flag == True:
                                neighboring += 1
                    if neighboring != c.cell_number:
                        return False

        return True


    def game_victory(self):
        if self.game_state == "YOU LOST! :(":
            return False

        hidden = 0
        for r in self.game_cells:
            for c in r:
                if c.is_visible == False:
                    hidden += 1

        if hidden == self.game_level[1]:
            return True
        return False


    def reset_board(self):
        self.screen.fill(BACKGROUND)
        self.display()
        self.board_cells()
        pg.display.update()



def main():
    print("Welcome To Minesweeper!")
    print()
    menu = GameMenu()
    menu.run_menu()


if __name__ == "__main__":
    main()
