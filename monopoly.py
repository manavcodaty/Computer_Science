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