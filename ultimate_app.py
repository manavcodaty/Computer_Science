#This is my ultimate app (made by Manav Codaty)
def monopoly():
    from random import randint

    class Dye(object):

        def __init__(self):
            pass

        def roll(self):
            return randint(0,6)

    class Tile(object):
        """
        Data Attributes:
            name
        """

        def __init__(self, name):
            self.name = name

        def trigger_event(self):
            print("Triggered Default Tile Event")

    class Property(Tile):
        """
        Data Attributes:
            name
            price
            base_rent
            is_utility
            is_rr
            owner
        """

        def __init__(self, name, price, base_rent, is_utility=False, 
                    is_rr=False):
            self.name = name
            self.price = price
            self.base_rent = base_rent
            self.owner=None

            if(is_utility):
                self.is_utility = True
            if(is_rr):
                self.is_rr = True

        def trigger_event(self):
            if self.owner is None:
                print("You landed on an unowned property")

                while True:
                    print("\n", "Unowned Property Menu")    
                    Game.display_menu(Game.unowned_property_menu)
                    selection = input("Select an option by typing a number: ")
                    if selection == '1':
                        # Buy Property
                        if Game.current_player.balance >= self.price:
                            Game.current_player.owned_properties.append(self)
                            Game.current_player.balance -= self.price 
                            print("Congratulations!", Game.current_player.name, 
                                "has successfully bought", self.name, 
                                "for the price of", self.price)
                            Game.current_player.display_balance()
                        else:
                            print("Your balance of", Game.current_player.balance,
                                "is insufficient to buy", self.name, "at the price of",
                                self.price)

                        break    
                    elif selection == '2':
                        # Do Not Buy Property
                        print("You chose not to buy {}.".format(self.name))
                        break
                    else:
                        print("Unknown option selected!")

        def view_property(self):
            print(self.name)    

    class Player(object):
        """
        Class Attributes:
            player_list
            max_num_players
        Data Attributes:
        name
        current_tile_index
        current_tile
        is_in_jail
        properties_owned       
        amount_of_money
        """
        player_list = []
        MAX_NUM_PLAYERS = 4

        def __init__(self, name):
            if len(Player.player_list) == Player.MAX_NUM_PLAYERS:
                print("Error: Cannot have more than", Player.MAX_NUM_PLAYERS, "players!") #DEBUG
            else:    
                self.name = name
                self.current_tile_index = 0
                self.current_tile = None # sets current tile to "GO" 
                self.is_in_jail = False
                self.num_rounds_in_jail = 0
                self.owned_properties = []
                self.balance = 1500

                Player.player_list.append(self)
                print(self.name, "has been succesfully added!") #DEBUG            

        def roll_and_move(self): # should a method from one class depend on a data attribute from another class?
            roll_1 = Game.DYE.roll()
            roll_2 = Game.DYE.roll()
            total_roll = roll_1 + roll_2
            print("You rolled a", roll_1) #DEBUG
            print("You rolled a", roll_2) #DEBUG

            # move player to new tile
            if total_roll + self.current_tile_index >= len(Game.BOARD):
                final_index = (self.current_tile_index + total_roll) - len(Game.BOARD) 
                self.current_tile_index = final_index
                self.current_tile = Game.BOARD[self.current_tile_index]
                self.balance += 200 # Pass GO
                print("You passed GO!") #DEBUG
            else:
                self.current_tile_index = self.current_tile_index + total_roll
                self.current_tile = Game.BOARD[self.current_tile_index]

            print("Your current tile is now",self.current_tile.name)    #DEBUG

            # trigger_event
            self.current_tile.trigger_event()

        def display_owned_properties(self):
            print("{}'s Properties: ".format(self.name))
            for property in self.owned_properties:
                print(property.name)

        def display_balance(self):
            print("{}'s current balance is {}".format(self.name, self.balance))

        def get_out_of_jail(self):
            pass

        """
        will put this in option function:

        def add_player():
            if len(Player.player_list) == Player.max_num_players:
                print("Error, cannot have more than",Player.max_num_players, "players")
                return
            else:
                print("You are adding a player")
                name = input('Please type the name of the player: ') # TODO: error check
                Player.player_list.append(Player(name))
                for player in Player.player_list: #DEBUG
                    print(player.name, "successfully added!") 
        """


    class Game(object):
        """ Instantiate once"""

        current_player = None
        turn_counter = 0
        DYE = Dye()
        BOARD = None   
        setup_menu = None
        player_menu = None
        unowned_property_menu = None


        def __init__(self):

            Game.BOARD = [
                Tile("GO"),
                Property("Mediterranean Avenue", 60, 2),
                Tile("Community Chest"),
                Property("Baltic Avenue",60, 8),
                Tile("Income Tax"),
                Property("Reading Railroad", 200, 50),
                Property("Oriental Avenue", 100, 6),
                Tile("Chance"),
                Property("Vermont Avenue", 100, 6),
                Property("Connecticut Avenue", 120, 8),
                Tile("Jail"),
                Property("St. Charles Place", 140, 10),
                Property("Electric Company", 150, 0, is_utility=True),
                Property("States Avenue", 140, 10),
                Property("Virginia Avenue", 160, 12),
                Property("Pennsylvania Railroad", 200, 50),
                Property("St. James Place", 180, 14),
                Tile("Community Chest"),
                Property("Tennessee Avenue", 180, 14),
                Property("New York Avenue", 200, 16),
                Tile("Free Parking"),
                Property("Kentucky Avenue", 220, 18),
                Tile("Chance"),
                Property("Indiana Avenue", 220, 18),
                Property("Illinois Avenue", 240, 20),
                Property("B. & O. Railroad", 200, 50),
                Property("Atlantic Avenue", 260, 22),
                Property("Ventnor Avenue", 260, 22),
                Property("Water Works", 150, 0, is_utility=True),
                Property("Marvin Gardens", 280, 24),
                Tile("Go To Jail"),
                Property("Pacific Avenue", 300, 26),
                Property("North Caroliina Avenue", 300, 26),
                Tile("Community Chest"),
                Property("Pennsylvania Avenue", 320, 28),
                Property("Short Line", 200, 50),
                Tile("Chance"),
                Property("Park Place", 350, 35),
                Tile("Luxury Tax"),
                Property("Boardwalk", 400, 50)]

            Game.setup_menu = {}
            Game.setup_menu['1'] = "Add Player." 
            Game.setup_menu['2'] = "Start Game."

            Game.player_menu = {}
            Game.player_menu['1'] = "Roll Dice."
            Game.player_menu['2'] = "Display Owned Properties."

            Game.unowned_property_menu = {}
            Game.unowned_property_menu['1'] = "Buy Property"
            Game.unowned_property_menu['2'] = "Do Not Buy Property"

            print("Welcome to Console Monopoly!")
            while True:
                print("\n")
                Game.display_menu(Game.setup_menu)
                selection = input("Select an option by typing a number: ")
                if selection == '1':
                    player_name = input("Please enter player name: ")
                    Player(player_name)
                elif selection == '2':
                    if len(Player.player_list) == 0:
                        print("Error: Cannot start game without players")
                    else:
                        break
                else:
                    print("Unknown option selected!")

            Game.current_player = Player.player_list[0]
            self.main() # Starts Main Game

        @staticmethod
        def display_menu(menu: dict):
            for option in menu:
                print("{}. {}".format(option, menu[option]))


        def start_player_turn(self):
            if Game.current_player.is_in_jail:
                did_his_time = Game.current_player.num_turns_in_jail == 3
                if did_his_time:
                    Game.current_player.get_out_of_jail()
                else:
                    print("Haven't coded this bit yet!")
                    #TODO:
                    #increment current_player.num_turns_in_jail
                    #display in_jail_menu
                    #code logic for menu selections
            elif True==False: #if player is bankrupt/ has lost
                pass
            else:
                while True:
                    print("\n", "Player Menu:")
                    Game.display_menu(Game.player_menu)
                    selection = input("Select an option by typing a number: ")
                    if selection == '1':
                        # Player Rolls Dice and Moves
                        Game.current_player.roll_and_move()
                    elif selection == '2':
                        # TODO:
                        print("TODO: Code diplay owned properties function")
                    else:
                        print("Unknown option selected!")

        def end_player_turn(self):
            pass

        def main(self):
            while True:
                if Game.current_player.is_in_jail:
                    self.end_player_turn()
                elif True == False: #TODO:make function that checks if there is a winner
                    pass # all other players bankrupt, end game 
                else:
                    self.start_player_turn()



    if __name__ == "__main__":    
        Game()
    
    
    
def rock_paper_scissors():
    import random

    while True:
        user_action = input("Enter a choice (rock, paper, scissors): ")
        possible_actions = ["rock", "paper", "scissors"]
        computer_action = random.choice(possible_actions)
        print(f"\nYou chose {user_action}, computer chose {computer_action}.\n")

        if user_action == computer_action:
            print(f"Both players selected {user_action}. It's a tie!")
        elif user_action == "rock":
            if computer_action == "scissors":
                print("Rock smashes scissors! You win!")
            else:
                print("Paper covers rock! You lose.")
        elif user_action == "paper":
            if computer_action == "rock":
                print("Paper covers rock! You win!")
            else:
                print("Scissors cuts paper! You lose.")
        elif user_action == "scissors":
            if computer_action == "paper":
                print("Scissors cuts paper! You win!")
            else:
                print("Rock smashes scissors! You lose.")

        play_again = input("Play again? (y/n): ")
        if play_again.lower() != "y":
            break

    
def number_guessing():

    #Higher or lower program
    import random

    targetNum = random.randint(1,100)
    userNum = 0
    
    while userNum != targetNum:
        userNum = int(input("Enter your guess"))
        if userNum == targetNum:
            print("Thats the correct number")
        elif userNum > targetNum:
            print("Too high")
        elif targetNum > userNum:
            print("Too low")
        else: break


    
def snake():
   # import required modules
    import turtle
    import time
    import random

    delay = 0.1
    score = 0
    high_score = 0


    # Creating a window screen
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("blue")
    # the width and height can be put as user's choice
    wn.setup(width=600, height=600)
    wn.tracer(0)

    # head of the snake
    head = turtle.Turtle()
    head.shape("square")
    head.color("white")
    head.penup()
    head.goto(0, 0)
    head.direction = "Stop"

    # food in the game
    food = turtle.Turtle()
    colors = random.choice(['red', 'green', 'black'])
    shapes = random.choice(['square', 'triangle', 'circle'])
    food.speed(0)
    food.shape(shapes)
    food.color(colors)
    food.penup()
    food.goto(0, 100)

    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 250)
    pen.write("Score : 0 High Score : 0", align="center",
            font=("candara", 24, "bold"))


    # assigning key directions
    def group():
        if head.direction != "down":
            head.direction = "up"


    def godown():
        if head.direction != "up":
            head.direction = "down"


    def goleft():
        if head.direction != "right":
            head.direction = "left"


    def goright():
        if head.direction != "left":
            head.direction = "right"


    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y+20)
        if head.direction == "down":
            y = head.ycor()
            head.sety(y-20)
        if head.direction == "left":
            x = head.xcor()
            head.setx(x-20)
        if head.direction == "right":
            x = head.xcor()
            head.setx(x+20)


    wn.listen()
    wn.onkeypress(group, "w")
    wn.onkeypress(godown, "s")
    wn.onkeypress(goleft, "a")
    wn.onkeypress(goright, "d")

    segments = []


    # Main Gameplay
    while True:
        wn.update()
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"
            colors = random.choice(['red', 'blue', 'green'])
            shapes = random.choice(['square', 'circle'])
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1
            pen.clear()
            pen.write("Score : {} High Score : {} ".format(
                score, high_score), align="center", font=("candara", 24, "bold"))
        if head.distance(food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)

            # Adding segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("orange") # tail colour
            new_segment.penup()
            segments.append(new_segment)
            delay -= 0.001
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write("Score : {} High Score : {} ".format(
                score, high_score), align="center", font=("candara", 24, "bold"))
        # Checking for head collisions with body segments
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)
        move()
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                colors = random.choice(['red', 'blue', 'green'])
                shapes = random.choice(['square', 'circle'])
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()

                score = 0
                delay = 0.1
                pen.clear()
                pen.write("Score : {} High Score : {} ".format(
                    score, high_score), align="center", font=("candara", 24, "bold"))
        time.sleep(delay)

    wn.mainloop()

    
def battle_ships():
   print("Welcome to Battleships!")	
   print("Do you want to play 2 player or 1 player?")
   
   choice = input("Enter 1 for 1 player or 2 for 2 player: ")
   
   if choice == "1":
       print("Let's play 1 player battleships!")
    
            
    
    
def hang_man():
  #importing the time module
    import time

    #welcoming the user
    name = input("What is your name? ")

    print ("Hello, " + name, "Time to play hangman!")

    #wait for 1 second
    time.sleep(1)

    print ("Start guessing...")
    time.sleep(0.5)

    #here we set the secret. You can select any word to play with. 
    word = ("secret")

    #creates an variable with an empty value
    guesses = ''

    #determine the number of turns
    turns = 10

    # Create a while loop

    #check if the turns are more than zero
    while turns > 0:         

        # make a counter that starts with zero
        failed = 0             

        # for every character in secret_word    
        for char in word:      

        # see if the character is in the players guess
            if char in guesses:    
        
            # print then out the character
                print (char,end=""),    

            else:
        
            # if not found, print a dash
                print ("_",end=""),     
        
            # and increase the failed counter with one
                failed += 1    

        # if failed is equal to zero

        # print You Won
        if failed == 0:        
            print ("You won")
        # exit the script
            break            
        # ask the user go guess a character
        guess = input("guess a character:") 

        # set the players guess to guesses
        guesses += guess                    

        # if the guess is not found in the secret word
        if guess not in word:  
    
        # turns counter decreases with 1 (now 9)
            turns -= 1        
    
        # print wrong
            print ("Wrong")  
    
        # how many turns are left
            print ("You have", + turns, 'more guesses' )
    
        # if the turns are equal to zero
            if turns == 0:           
        
            # print "You Lose"
                print ("You Lose"  )  
    
    

def games():
    print("Press 1 for rock, paper, scissors")
    print("Press 2 for snake")
    print("Press 3 for monopoly")
    print("Press 4 for hangman")
    print("Press 5 for number guessing game")
    print("Press 6 for battleships game")	
    
    games_choice = int(input("Enter your choice"))
    
    if games_choice == 1:
        rock_paper_scissors()
    elif games_choice == 2:
        snake()
    elif games_choice == 3:
        monopoly()
    elif games_choice == 4:
        hang_man()
    elif games_choice == 5:
        number_guessing()
    elif games_choice == 6:
        battle_ships()
    
    
def get_calculator():
    print("Press 1 for simple calculator")
    print("Press 2 for scientific calculator")
    print("Press 3 for complete calculator")
    
    get_calculator_choice = int(input("Enter your choice"))
    
    if get_calculator_choice == 1:
        simple_calc()
    elif get_calculator_choice == 2:
        science_calc()
    elif get_calculator_choice == 3:
        trig_calc()
        
        
        
        
def simple_calc():
    calc = input("Enter calculation")
    print(eval(calc))
    

def science_calc():
    import tkinter as tk
    import math

    class Calculator:
        def __init__(self, master):
            self.master = master
            master.title("Calculator")
            master.geometry("312x324")

            self.total = tk.StringVar()

            self.entry = tk.Entry(master, textvariable=self.total, font=("Helvetica", 20))
            self.entry.grid(row=0, column=0, columnspan=5, pady=5)

            self.create_buttons()

        def create_buttons(self):
            button_list = [
                ['sin', 'cos', 'tan', '^2', '10^x'],
                ['7', '8', '9', '/', 'log(x)'],
                ['4', '5', '6', '*', '1/x'],
                ['1', '2', '3', '-', 'x!'],
                ['0', 'C', '=', '+', 'sqrt']
            ]

            for i, row in enumerate(button_list):
                for j, button_text in enumerate(row):
                    button = tk.Button(
                        self.master, text=button_text, width=5, height=3, font=("Helvetica", 20),
                        command=lambda text=button_text: self.click(text)
                    )
                    button.grid(row=i + 1, column=j, sticky="nsew")
                self.master.rowconfigure(i + 1, weight=1)
            self.master.columnconfigure(0, weight=1)
            self.master.columnconfigure(1, weight=1)
            self.master.columnconfigure(2, weight=1)
            self.master.columnconfigure(3, weight=1)
            self.master.columnconfigure(4, weight=1)

        def click(self, button_text):
            if button_text == '=':
                try:
                    result = eval(self.entry.get())
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'C':
                self.total.set("")
            elif button_text == 'sin':
                try:
                    result = math.sin(math.radians(float(self.entry.get())))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'cos':
                try:
                    result = math.cos(math.radians(float(self.entry.get())))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'tan':
                try:
                    result = math.tan(math.radians(float(self.entry.get())))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == '^2':
                try:
                    
                    result = float(self.entry.get()) ** 2
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'log(x)':
                try:
                    result = math.log(float(self.entry.get()))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == '1/x':
                try:
                    result = 1 / float(self.entry.get())
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'x!':
                try:
                    result = math.factorial(int(self.entry.get()))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == '10^x':
                try:
                    result = 10 ** float(self.entry.get())
                    self.total.set(result)
                except:
                    self.total.set("Error")
            elif button_text == 'sqrt':
                try:
                    result = math.sqrt(float(self.entry.get()))
                    self.total.set(result)
                except:
                    self.total.set("Error")
            else:
                self.total.set(self.entry.get() + button_text)

    if __name__ == '__main__':
        root = tk.Tk()
        my_calculator = Calculator(root)
        root.mainloop()
    
    
    
    
def encoder():
    print("This program uses a Caesar Cipher to encrypt a plain text message using the encryption key you provide")
    name = input("Enter the message to be encrypted:")

    #Take the user input for the encryption key (The key here is saved as string)
    key = input("Enter an integer for an encryption key:")

    name = name.upper()

    values = []

    for x in name:

        #int(key) parses the key to an integer, then it is added to the ascii value of the current letter and is saved in the variable 'encrypted'
        encrypted = ord(x) + int(key)

        #chr(encrypted) parses the number value of 'encrypted' into the corresponding ascii character and then it appends it to the list 'values'
        values.append(chr(encrypted))

    print(values)
        
    

def trig_calc():
    import math
    def trigcalc():
        notdone = True
        print()
        print("Welcome to the trigonometry calculator.")
        print()
        print("Please select a mode from the following:")
        print("1. Pythagoras' Theorem (right angled triangle)")
        print("2. tan(), sin(), cos() for unknown side (right angled triangle)")
        print("3. tan(), sin(), cos() for unknown angle (right angled triangle)")
        print("4. Sine rule (two sides, non-included angle)")
        print("5. Cosine rule (two sides, included angle OR three sides)")
        print("6. Area of triangle (two sides, included angle)")
        print()
        while notdone:
            try:
                mode = int(input("Please enter a mode: "))
                if mode > 0 and mode <= 6:
                    notdone = False
                    if mode == 1:
                        pythagoras()
                    if mode == 2:
                        rightangledtrig()
                    if mode == 3:
                        rightangledtrigangle()
                    if mode == 4:
                        sinrule()
                    if mode == 5:
                        cosrule()
                    if mode == 6:
                        areatriangle()
                else:
                    print()
                    print("Enter a number between 1 and 6 - there are only 6 modes")
                    print()
            except ValueError:
                print()
                print("Please enter a valid number")
                print()

    def pythagoras():
        notdone = True
        while notdone:
            try:
                mode = int(input("Please specify the mode: 1 for finding the hypotenuse or 2 for finding a side given the hypotenuse and a side: "))
                if mode in [1,2]:
                    if mode == 1:
                        side1 = float(input("Side 1: "))
                        side2 = float(input("Side 2: "))
                        result = math.hypot(side1,side2)
                        print("Hypotenuse = sqrt(" + str(side1) + " + " + str(side2) + ")")
                        print()
                        print("The hypotenuse is",result,"units long. (please round off if needed.)")
                        print()
                        notdone = False
                        return
                    if mode == 2:
                        side1 = float(input("Length of hypotenuse: "))
                    side2 = float(input("Length of other known side: "))
                    result = math.sqrt((side1**2 - side2**2))
                    print("Hypotenuse = sqrt(" + str(side1) + "- " + str(side2) + ")")
                    print()
                    print("The hypotenuse is",result,"units long. (please round off if needed.)")
                    print()
                    notdone = False
                    return
                else:
                    print()
                    print("Please enter 1 or 2.")
                    print()
            except ValueError:
                print()
                print("One of your inputs is incorrect.")
                print()

    def sinrule():
        notdone = True
        while notdone:
            try:
                mode = int(input("Please specify the mode: 1 for finding a side and 2 for finding an angle: "))
                if mode in [1,2]:
                    if mode == 1:
                        side1 = float(input("Side 1 length: "))
                        angle1 = float(input("Angle 1 (corresponding to side 1, in degrees, without the unit): "))
                        angle2 = float(input("Angle 2 (corresponding to unknown side, in degrees, without the unit): "))
                        print("By sine rule,")
                        print("unknown side / sin({0}) = {1} / sin({2})".format(angle2,side1,angle1))
                        print("thus,")
                        print("unknown side = {0} * {1}) / sin({2})".format(side1,angle2,angle1))
                        result = (side1 * math.sin(math.radians(angle1))) / math.sin(math.radians(angle2))
                        print()
                        print("The side is",result,"units long. (please round off if needed.)")
                        print()
                        notdone = False
                        return
                    if mode == 2:
                        side1 = float(input("Side 1 length (corresponding to known angle): "))
                        side2 = float(input("Side 2 length (corresponding to unknown angle): "))
                        angle1 = float(input("Angle (corresponding to side 1, in degrees, without the unit): "))
                        print("By sine rule,")
                        print("sin(unknown angle) / {0} = sin({1}) / {2} ".format(side2,angle1,side1))
                        print("thus,")
                        print("unknown angle = inv sine({0}  *  sin({1})) /  {2})".format(side2,angle1,side1))
                        result = math.degrees(math.asin((side2 * math.sin(math.radians(angle1))) / side1))
                        print()
                        print("The angle is",result,"or",(180 - result),"degrees wide. (please round off if needed.) Note that you may have to reject one of the answers.")
                        print()
                        notdone = False
                        return
                else:
                    print()
                    print("Please enter 1 or 2.")
                    print()
            except ValueError:
                print()
                print("One of your inputs is incorrect.")
                print()
        return

    def cosrule():
        notdone = True
        while notdone:
            try:
                mode = int(input("Please specify the mode: 1 for finding a side and 2 for finding an angle."))
                if mode in [1,2]:
                    if mode == 1:
                        side1 = float(input("Side 1 length: "))
                        side2 = float(input("Side 2 length: "))
                        angle1 = float(input("Angle (non-included from specified sides): "))
                        print("By cosine rule,")
                        print('{0}^2 + {1}^2 - (2 * {0} * {1} * cos({2})'.format(side1,side2,angle1))
                        calc = side1 ** 2 + side2 ** 2 - (2*side1*side2*math.cos((math.radians(angle1))))
                        result = math.sqrt(calc)
                        print()
                        print("The side is",result,"units long (please round off if needed.)")
                        print()
                        notdone = False
                        return
                    if mode == 2:
                        a = float(input("Side 1 length: "))
                        b = float(input("Side 2 length: "))
                        c = float(input("Side 3 length: "))
                        print("By cosine rule,")
                        print("Angle A = inv cos( ({0}^2 + {1}^2 - {2}^2) / (2*{0}*{1}) )".format(b,c,a))
                        print("Angle B = inv cos( ({0}^2 + {1}^2 - {2}^2) / (2*{0}*{1}) )".format(a,c,b))
                        print("Angle C = inv cos( ({0}^2 + {1}^2 - {2}^2) / (2*{0}*{1}) )".format(a,b,c))
                        print("Angles found:")
                        calc1 = (b**2 + c**2 - a**2) / (2*b*c)
                        calc2 = (a**2 + c**2 - b**2) / (2*a*c)
                        calc3 = (a**2 + b**2 - c**2) / (2*a*c)
                        calcs = [calc1,calc2,calc3]
                        for calc in calcs:
                            if calc >= -1 and calc <= 1:
                                result = math.degrees(math.acos(calc))
                                print(result)
                        print("If angles are irrational, please round off if needed.")
                        notdone = False
                        return
            except ValueError:
                print("One of your inputs is incorrect.")
            



    def rightangledtrig():
        notdone = True
        while notdone:
            try:
                unknown = input("Specify the unknown side relative to your angle. h for hypotenuse, a for adjacent, o for opposite: ")
                known = input("Specify the known side relative to your angle. h for hypotenuse, a for adjacent, o for opposite: ")
                if unknown.lower() in ["h", "a", "o"] and known.lower() in ["h", "a", "o"] and unknown != known:
                    angle = float(input("Enter your known angle (in degrees, without the sign): "))
                    known1 = float(input("Enter the length of your known side: "))
                    notdone = False
                    if unknown == "h":
                        print("Hypotenuse is unknown")
                        if known == "a":
                            print("Adjacent side known, using cos()")
                            print("Since cos() = adj / hyp,")
                            print("unknown side = {0} / cos({1})".format(known1,angle))
                            result = known1/math.cos(math.radians(angle))
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                        if known == "o":
                            print("Opposite side known, using sin()")
                            print("Since sin() = opp/hyp,")
                            print("unknown side = {0} / sin({1})".format(known1,angle))
                            result = known1/math.sin(math.radians(angle))
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                    if unknown == "a":
                        print("Adjacent side is unknown")
                        if known == "h":
                            print("Hypotenuse known, using cos()")
                            print("Since cos() = adj / hyp,")
                            print("unknown side = {0} * cos({1})".format(known1,angle))
                            result = math.cos(math.radians(angle) * known1)
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                        if known == "o":
                            print("Opposite side known, using tan()")
                            print("Since tan() = opp/adj,")
                            print("unknown side = {0} / tan({1})".format(known1,angle))
                            result = known1/math.tan(math.radians(angle))
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                    if unknown == "o":
                        print("Opposite side is unknown")
                        if known == "h":
                            print("Since sin() = opp/hyp,")
                            print("unknown side = {0} * sin({1})".format(known1,angle))
                            result = math.sin(math.radians(angle) * known1)
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                        if known == "a":
                            print("Opposite side known, using tan()")
                            print("Since tan() = opp/adj,")
                            print("unknown side = {0} * tan({1})".format(known1,angle))
                            result = known1 * math.tan(math.radians(angle))
                            print()
                            print("The side is",result,"units long (please round off if needed.)")
                            print()
                            return
                else:
                    print("Please specify either \"h\", \"a\" or \"o\"")
            except ValueError:
                print()
                print("You did not specify a correct input. Try again.")
                print()

    def rightangledtrigangle():
        notdone = True
        while notdone:
            try:
                known1 = input("Specify the first known side relative to your angle. h for hypotenuse, a for adjacent, o for opposite: ")
                known2 = input("Specify the second known side relative to your angle. h for hypotenuse, a for adjacent, o for opposite: ")
                if known2.lower() in ["h", "a", "o"] and known1.lower() in ["h", "a", "o"] and known1 != known2:
                    length1 = float(input("Specify the length of the first known side: "))
                    length2 = float(input("Specify the length of the second known side: "))
                    if known1 == "h" and known2 == "a":
                        print("Hypotenuse and adjacent side known, using arc (inverse) cosine")
                        print("Since cos() = adj/hyp,")
                        print("unknown angle = inv cos({0} / {1})".format(length2,length1))
                        result = math.degrees(math.acos(length2/length1))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    if known1 == "h" and known2 == "o":
                        print("Hypotenuse and opposite side known, using arc (inverse) sine")
                        print("Since sin() = opp/hyp,")
                        print("unknown angle = inv sin({0} / {1})".format(length2,length1))
                        result = math.degrees(math.asin(length2/length1))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    if known1 == "a" and known2 == "h":
                        print("Hypotenuse and adjacent side known, using arc (inverse) cosine")
                        print("Since cos() = adj/hyp,")
                        print("unknown angle = inv cos({0} / {1})".format(length1,length2))
                        result = math.degrees(math.acos(length1/length2))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    if known1 == "o" and known2 == "h":
                        print("Hypotenuse and opposite side known, using arc (inverse) sine")
                        print("Since sin() = opp/hyp,")
                        print("unknown angle = inv sin({0} / {1})".format(length1,length2))
                        result = math.degrees(math.asin(length1/length2))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    if known1 == "o" and known2 == "a":
                        print("Opposite and adjacent side known, using arc (inverse) tangent")
                        print("Since tan() = opp/adj,")
                        print("unknown angle = inv tan({0} / {1})".format(length1,length2))
                        result = math.degrees(math.atan(length1/length2))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    if known1 == "a" and known2 == "o":
                        print("Adjacent and opposite side known, using arc (inverse) tangent")
                        print("Since tan() = opp/adj,")
                        print("unknown angle = inv tan({0} / {1})".format(length2,length1))
                        result = math.degrees(math.atan(length2/length1))
                        print()
                        print("Angle is",result,"degrees (please round off if needed.)")
                        print()
                    notdone = False
                    return
                else:
                    print("Please specify either \"h\", \"a\" or \"o\"")
            except ValueError:
                    print("One of your inputs is incorrect. Try again.")

    def areatriangle():
        notdone = True
        while notdone:
            try:
                length1 = float(input("Side 1 length: "))
                length2 = float(input("Side 2 length: "))
                angle = float(input("Angle (the inclusive angle of the two sides): "))
                print("As area of triangle = 0.5(a*b*sin(C)),")
                print("area = 0.5({0} * {1} * sin({2}))".format(length1,length2,angle))
                result = 0.5 * length1 * length2 * math.sin(math.radians(angle))
                print()
                print("Area is",result,"units squared (please round off if needed.)")
                print()
                notdone = False
            except ValueError:
                print()
                print("You did not specify a correct input. Try again.")
                print()

    while True:
        trigcalc()
    
    
    
    
                  
                    
        
def start():
    print("Press 1 to navigate to games")
    print("Press 2 to navigate to calculator")
    print("Press 3 to navigate to encoder")
    
    start_choice = int(input("Enter your choice"))
    
    if start_choice == 1:
        games()
    elif start_choice == 2:
        get_calculator()
    elif start_choice == 3:
        encoder()
        
        
        
start()










