import pandas as pd
import sys
        
game = [[" ","|"," ","|"," "], 
        ["--", "--", "--", "--", "--"],
        [" ","|", " ","|"," "],
        ["--", "--", "--", "--", "--"],
        [" ","|"," ","|"," "]]

def print_game():
    df = pd.DataFrame(game)
    print(df)
        

       
def check_winner():
    if game[0][0] == game[0][2] == game[0][4] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][0] == game[2][0] == game[4][0] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][0] == game[2][2] == game[4][4] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][2] == game[2][2] == game[4][2] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][4] == game[2][4] == game[4][4] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[2][0] == game[2][2] == game[2][4] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[4][0] == game[4][2] == game[4][4] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][4] == game[2][2] == game[4][0] == "X":
        print_game()
        print("Player 1 wins")
        return True
    if game[0][0] == game[0][2] == game[0][4] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[0][0] == game[2][0] == game[4][0] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[0][0] == game[2][2] == game[4][4] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[0][2] == game[2][2] == game[4][2] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[0][4] == game[2][4] == game[4][4] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[2][0] == game[2][2] == game[2][4] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[4][0] == game[4][2] == game[4][4] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if game[0][4] == game[2][2] == game[4][0] == "O":
        print_game()
        print("Player 2 wins")
        return True
    if not (game[0][0] and game[0][2] and game[0][4] and game[2][0] and game[2][2] and game[2][4] and game[4][0] and game[4][2] and game[4][4]) == " ":
        print_game()
        print("It's a tie")
        
def end_game():
    if check_winner() == True:
        print("Game Over")
        sys.exit()
    
def turn():
    print_game()
    print("------------------------------------------")
    print("Player 1, it's your turn")
    row = int(input("Enter the row: "))
    column = int(input("Enter the column: "))
    if game[row][column] == " ":
        game[row][column] = "X"
        check_winner()
        end_game()
    else:  
        print("That spot is already taken")
        turn()
    print("------------------------------------------")
    print_game()
    print("------------------------------------------")
    print ("Player 2, it's your turn")
    row = int(input("Enter the row: "))
    column = int(input("Enter the column: "))
    if game[row][column] == " ":
        game[row][column] = "O"
        check_winner()
        end_game()
    else:
        print("That spot is already taken or invalid")
        turn()
    print("------------------------------------------")
    print_game()
    print("------------------------------------------")
    


    
def main():
    while True:
        turn()
        
        


        
        
main()


#024