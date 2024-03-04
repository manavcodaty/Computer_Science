def main(choice):
    while choice != -1:
        msg = input("Enter the message to append: ")
        file = open("hello_world.txt", "w")
        file.write(msg)
        print("Data appended successfully")
        file = open("hello_world.txt", "r")
        content = file.read()
        print(content)
        file.close()
        main(choice)


    
choice = input("Do you want to append data to the file? (1/-1), (y/n)): ")
main(choice)




        
