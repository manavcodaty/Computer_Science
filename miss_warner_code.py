#piece of code that is missing from the mark questions

import random
def task2(): 
    count1 = 1 
    while count1 <= 5: 
        answer = False 
        attempts = 1 
        multiply = 6 
        num1 = random.randint (1,12) 
        print (multiply ,"x", num1) 
        ask = int(input("Enter a number")) 
        while attempts < 3 and answer == False: 
            if ask == multiply * num1: 
                answer = True 
            else: 
                if ask > multiply * num1: 
                    print ("Answer is too large") 
                    ask = int(input("Enter a number")) 
                    attempts = attempts + 1
                else: 
                    print ("Answer is too small") 
                    ask = int(input("Enter a number")) 
                    attempts = attempts + 1 
            if attempts >= 3:
                    print (multiply * num1) 
            else: 
                print ("Answer is correct") 
                count1 = count1 + 1 

task2()