import random

map = [[0 for _ in range(12)] for _ in range(12)]
comp_guess = [random.randint(0, 11), random.randint(0, 11)]


def play():
    guess = 0
    while guess < 5:
        print("Enter your guess")
        x = int(input("Enter the x coordinate: "))
        y = int(input("Enter the y coordinate: "))
        if x == comp_guess[0] and y == comp_guess[1]:
            print("You found the treasure!")
            break
        else:
            print("Try again")
            print("----------------------")
            x_diff = x - comp_guess[0]
            y_diff = y - comp_guess[1]
            if x_diff < 0:
                x_diff *= -1
            if y_diff < 0:
                y_diff *= -1
            print(f"Distance from the treasure: {x_diff + y_diff}")
            guess += 1


play()
