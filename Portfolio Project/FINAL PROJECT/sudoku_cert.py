# Casey Levy
# CS 325 - Portfolio Project
# Sudoku

# Code inspired/referenced from the following:
# https://www.youtube.com/watch?v=eqUwSA0xI-s&feature=emb_logo
# https://www.geeksforgeeks.org/sudoku-backtracking-7/
# https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
# https://www.youtube.com/watch?v=auK3PSZoidc

import itertools

# Verifying moves made by the user if they're "legal" or not
def verify_move(arr, num, game_box):
    for x in range(9):
        if arr[game_box[0]][x] == num and game_box[1] != x:
            return False
    for x in range(len(arr)):
        if arr[x][game_box[1]] == num and game_box[0] != x:
            return False

    r = game_box[1]//3
    c = game_box[0]//3

    for x in range(c * 3, c * 3+3):
        for y in range(r * 3, r * 3+3):
            if arr[x][y] == num and (x,y) != game_box:
                return False
    return True


def check_box_empty(arr):
    for x in range(len(arr)):
        for y in range(len(arr[0])):
            if arr[x][y] == 0:
                return (x,y)

    return None


def display_board(arr):
    for r in arr:
        print(r)

# Method to solve the board if the user selects the "Solve!" button
# https://www.geeksforgeeks.org/sudoku-backtracking-7/
def solve_game(arr):
    solve_arr = arr
    empty = check_box_empty(solve_arr)

    if not empty:
        return solve_arr
    else:
        r, c = empty

    for x in range(1, 10):
        if verify_move(solve_arr, x, (r,c)):
            solve_arr[r][c] = x

            if solve_game(solve_arr):
                return solve_arr
            solve_arr[r][c] = 0

    return False

# Method to check a solution once the user thinks they have one/all boxes are filled
# https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
# https://www.geeksforgeeks.org/sudoku-backtracking-7/
def check_solution(game_board):
    row = [r for r in game_board if not check_row(r)]
    g_board = list(zip(*game_board))

    for x in g_board:
        if 0 in x:
            return False
    
    col = [c for c in game_board if not check_row(c)]
    g_boxes = []

    for x in range(1,9,3):
        for y in range(1,9,3):
            g_box = list(itertools.chain(r[y:y + 3]for r in g_board[x:x + 3]))
            g_boxes.append(g_box)

    solve_box = [b for b in g_boxes if not check_row(b)]

    return not row or not col or not solve_game

# Helper function for check_solution() method
# https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
def check_row(r):
    return (len(r) == 9 and sum(r) == sum(set(r)))

if __name__ == "__main__":
    game_board = [[0 for x in range(9) ] for y in range(9)]
    game_board = [[0, 5, 0, 0, 9, 0, 6, 0, 0], [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 5, 2, 0, 6, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 4],
                 [5, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 1, 0, 0, 8, 0],
                  [9, 0, 0, 8, 6, 3, 0, 0, 5], [3, 0, 6, 5, 0, 8, 4, 0, 0]]

    display_board(game_board)
    print(check_solution(game_board))
    print("----------------------------")

    if solve_game(game_board):
        solve_game(game_board)
        display_board(game_board)
        print(check_solution(game_board))
    
    else:
        print("Not a Possible Solution")