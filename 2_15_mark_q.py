import random
import time

def ask_2():
    global name 
    name = input("Enter your name") 
    global mult_table
    mult_table = int(input("Enter your desired multiplication "))
    time.sleep(2)
    testing()


def testing():
    i == 1
    score = 0
    
    if mult_table <= 1 or mult_table >= 13:
        print("This is not valid")
        time.sleep(10)``
        ask_2()
        
        
        
    while i <= 5:
        ans = random.randint(1,12)
        print(f"{name} what is {mult_table} x  {ans}")

        answer = int(input())

        if answer == mult_table * ans:
            print("Correct")
        else:
            print(f"Incorrect, the answer is {mult_table} x ans = {mult_table*ans}")

        time.sleep(1)

        i += 1
        
    

        
        
def ask_1():
    global name 
    name = input("Enter your name")
    global mult_table
    mult_table = int(input("Enter your desired multiplication "))
    time.sleep(2)
    learning()
        
def learning(): 
    count1 = 1 
    while count1 <= 5: 
        answer = False 
        attempts = 1 
        multiply = 6 
        num1 = random.randint (1,12) 
        print(f"{name}, what is {multiply} x {num1}?") 
        ask = int(input(name, "Enter a number")) 
        while attempts < 3 and answer == False: 
            if ask == multiply * num1: 
                answer = True 
            else: 
                if ask > multiply * num1: 
                    print (f"{name} Answer is too large") 
                    ask = int(input(name, "Enter a number")) 
                    attempts = attempts + 1
                else: 
                    print (f"{name} Answer is too small") 
                    ask = int(input(name, "Enter a number")) 
                    attempts = attempts + 1 
            if attempts >= 3:
                    print (multiply * num1) 
            else: 
                print ("Answer is correct") 
                count1 = count1 + 1 


    

        


        
def start():
    choice = int(input("Enter 1 for learning and 2 for testing"))
    
    if choice == 1:
        ask_1()
    elif choice == 2:
        testing()   


    
    







start()