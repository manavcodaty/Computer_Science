
while msg != -1:
    msg = input("Enter the message to append: ")
    file = open("hello_world.txt", "w")
    msg = input("Enter the message to append: ")
    file.write(msg)
    print("Data appended successfully")
    file = open("hello_world.txt", "r")
    content = file.read()
    print(content)
    file.close()
        
