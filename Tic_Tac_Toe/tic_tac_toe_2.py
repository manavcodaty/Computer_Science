import random
import sys

import pandas as pd

arr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def print_board():
    df = pd.DataFrame(arr)
    print(df)


print_board()  # print the board at the start


def validation(row, col):
    if row > 2 or col > 2 or col < 0 or row < 0:
        print("Invalid row or column number")
        make_move()


def ai_move():
    row = random.randint(0, 2)
    col = random.randint(0, 2)
    if arr[row][col] == 0:
        arr[row][col] = "O"
        print_board()
        if check_winner():
            print("Player 2 wins!")
            sys.exit(0.5)
        make_move()
    else:
        ai_move()


def check_winner():
    for i in range(3):
        if arr[i][0] == arr[i][1] == arr[i][2] and arr[i][0] != 0:
            return True
        if arr[0][i] == arr[1][i] == arr[2][i] and arr[0][i] != 0:
            return True
    if arr[0][0] == arr[1][1] == arr[2][2] and arr[0][0] != 0:
        return True
    if arr[0][2] == arr[1][1] == arr[2][0] and arr[0][2] != 0:
        return True
    return False


def make_move():
    print("Enter row number: ")
    row = int(input())
    print("Enter column number: ")
    col = int(input())
    validation(row, col)
    if arr[row][col] == 0:
        arr[row][col] = "X"
        print_board()
        if check_winner():
            print("Player 1 wins!")
            sys.exit(0.5)
        ai_move()


make_move()
