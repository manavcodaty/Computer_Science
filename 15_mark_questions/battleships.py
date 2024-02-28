import random

# Initialize the boards
board1 = []
board2 = []

for x in range(0, 5):
    board1.append(["O"] * 5)
    board2.append(["O"] * 5)

def print_board(board):
    for row in board:
        print(" ".join(row))
        
        
def handle_guess(board, guess_row, guess_col):
    if guess_row not in range(5) or guess_col not in range(5):
        print("Oops, that's not even in the ocean.")
    elif board[guess_row][guess_col] == "X":
        print("You guessed that one already.")
    else:
        print("You missed the battleship!")
        board[guess_row][guess_col] = "X"
    print_board(board)

# Randomly place a ship
def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board[0]) - 1)

ship_row1 = random_row(board1)
ship_col1 = random_col(board1)

ship_row2 = random_row(board2)
ship_col2 = random_col(board2)

# Game loop
for turn in range(5):
    print("Player 1 Turn", turn + 1)
    guess_row1 = int(input("Guess Row (0-4): "))
    guess_col1 = int(input("Guess Col (0-4): "))

    if guess_row1 == ship_row2 and guess_col1 == ship_col2:
        print("Congratulations Player 1! You sank Player 2's battleship!")
        break
    else:
        handle_guess(board1, guess_row1, guess_col1)

    print("Player 2 Turn", turn + 1)
    guess_row2 = int(input("Guess Row (0-4): "))
    guess_col2 = int(input("Guess Col (0-4): "))

    if guess_row2 == ship_row1 and guess_col2 == ship_col1:
        print("Congratulations Player 2! You sank Player 1's battleship!")
        break
    else:
        handle_guess(board2, guess_row2, guess_col2)

