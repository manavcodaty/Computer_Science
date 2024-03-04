file = open("3a. Task1Data (3).txt", "a")
msg = input("Enter the message to append: ")
file.write(msg)
print("Data appended successfully")
file = open("3a. Task1Data (3).txt", "r")
content = file.read()
print(content)

file.close()
