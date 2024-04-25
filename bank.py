import sys
import pretty_errors
id = 0

Account = [["Ben","12345"],
           ["Sarah","password"],
           ["Glen","Glen123"]]
AccDetails = [[10050.50,300.00,300.000],
              [250.50,100.00,200.00],
              [10.50,500.00,1000.00]]
size = len(Account) #Size was mentioned in the question as we do not know the size of the array\

def display_balance():
    print("Your balance is", AccDetails[id][0])
    menu()
    
def withdraw():
    amount = int(input("Enter the amount you would like to withdraw: "))
    if amount > AccDetails[id][0]:
        print("Insufficient funds")
    else:
        AccDetails[id][0] -= amount
        print("Your new balance is", AccDetails[id][0])
    menu()

def deposit():
    amount = int(input("Enter the amount you would like to deposit: "))
    AccDetails[id][0] += amount
    print("Your new balance is", AccDetails[id][0])
    menu()
    

def menu():
    print("Welcome to the bank")
    print("1. Display Balance")
    print("2. Withdraw Money")
    print("3. Deposit Money")
    print("4. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        display_balance()
    elif choice == 2:
        withdraw()
    elif choice == 3:
        deposit()
    elif choice == 4:
        sys.exit()
        

def login():
    id = int(input("Enter your account number: "))
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    for i in range(size):
        if Account[id][0] == username and Account[id][1] == password:
            print("Welcome", username)
            menu()
            return username
        else:
            print("Incorrect username or password")
            login()
            
            
login()