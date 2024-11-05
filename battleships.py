

import pandas as pd

p1_board = [[" "] * 10] * 10
p2_board = [[" "] * 10] * 10
p1_view_board = [[" "] * 10] * 10
p2_view_board = [[" "] * 10] * 10

small_ship = 2
medium_ship = 3
large_ship = 4
acc = 5
won = False


def start_p1():
    print("Player 1, place your ships")

    print("Enter the coordinates for the small ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(small_ship):
            p1_board[x][y + i] = "S"
    else:
        for i in range(small_ship):
            p1_board[x + i][y] = "S"

    print("Enter the coordinates for the medium ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(medium_ship):
            p1_board[x][y + i] = "M"
    else:
        for i in range(medium_ship):
            p1_board[x + i][y] = "M"

    print("Enter the coordinates for the large ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(large_ship):
            p1_board[x][y + i] = "L"
    else:
        for i in range(large_ship):
            p1_board[x + i][y] = "L"

    print("Enter the coordinates for the air craft carrier")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(acc):
            p1_board[x][y + i] = "ACC"
    else:
        for i in range(acc):
            p1_board[x + i][y] = "ACC"


def start_p2():
    print("Player 2, place your ships")

    print("Enter the coordinates for the small ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(small_ship):
            p1_board[x][y + i] = "S"
    else:
        for i in range(small_ship):
            p1_board[x + i][y] = "S"

    print("Enter the coordinates for the medium ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(medium_ship):
            p1_board[x][y + i] = "M"
    else:
        for i in range(medium_ship):
            p1_board[x + i][y] = "M"

    print("Enter the coordinates for the large ship")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(large_ship):
            p1_board[x][y + i] = "L"
    else:
        for i in range(large_ship):
            p1_board[x + i][y] = "L"

    print("Enter the coordinates for the air craft carrier")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1
    print("Enter the orientation")
    print("1. Vertical")
    print("2. Horizontal")
    orientation = int(input())

    if orientation == 1:
        for i in range(acc):
            p1_board[x][y + i] = "ACC"
    else:
        for i in range(acc):
            p1_board[x + i][y] = "ACC"


def play_p1():
    print("Player 1, enter the coordinates to attack")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1

    if p2_board[x][y] == "S":
        print("You hit the small ship")
        p2_board[x][y] = "X"
        p1_view_board[x][y] = "X"
    elif p2_board[x][y] == "M":
        print("You hit the medium ship")
        p2_board[x][y] = "X"
        p1_view_board[x][y] = "X"
    elif p2_board[x][y] == "L":
        print("You hit the large ship")
        p2_board[x][y] = "X"
        p1_view_board[x][y] = "X"
    elif p2_board[x][y] == "ACC":
        print("You hit the air craft carrier")
        p2_board[x][y] = "X"
        p1_view_board[x][y] = "X"
    else:
        print("You missed")
        p1_view_board[x][y] = "~"

    print("Player 1's board")
    print(p1_board)
    print("Player 1's view board")
    print(p1_view_board)

    for i in p2_board:
        if (
            p2_board[i] == "S"
            or p2_board[i] == "M"
            or p2_board[i] == "L"
            or p2_board[i] == "ACC"
        ):
            won = False
        else:
            won = True
    """
    if won == True:
        print("Player 1 has won")
    else:
        play_p2()  
    """


def play_p2():
    print("Player 2, enter the coordinates to attack")
    print("Enter the x coordinate")
    x = int(input())
    x = -1
    print("Enter the y coordinate")
    y = int(input())
    y = -1

    if p1_board[x][y] == "S":
        print("You hit the small ship")
        p1_board[x][y] = "X"
        p2_view_board[x][y] = "X"
    elif p1_board[x][y] == "M":
        print("You hit the medium ship")
        p1_board[x][y] = "X"
        p2_view_board[x][y] = "X"
    elif p1_board[x][y] == "L":
        print("You hit the large ship")
        p1_board[x][y] = "X"
        p2_view_board[x][y] = "X"
    elif p1_board[x][y] == "ACC":
        print("You hit the air craft carrier")
        p1_board[x][y] = "X"
        p2_view_board[x][y] = "X"
    else:
        print("You missed")
        p2_view_board[x][y] = "~"

    for i in p1_board:
        if (
            p1_board[i] == "S"
            or p1_board[i] == "M"
            or p1_board[i] == "L"
            or p1_board[i] == "ACC"
        ):
            won = False
        else:
            won = True
    """
    if won == True:
        print("Player 2 has won")
    else:
        play_p1()  
    """

    print("Player 2's board")
    print(p2_board)
    print("Player 2's view board")
    print(p2_view_board)


def main():
    start_p1()
    start_p2()
    while True:
        play_p1()
        play_p2()

        if won == True:
            print("Player 2 has won")
        else:
            play_p1()


main()
