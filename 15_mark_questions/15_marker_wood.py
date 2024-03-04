customers = [] * 100
quotes = [[]] * 100
wood_type = ["Laminate", "Pine", "Oak"]
price = [29.99, 39.99, 54.99]
length = 0
width = 0
area = 0
amount = 0
name = ""
wood = ""




def validation():
    if length < 1.5 or length > 10:
        print("Invalid length")
        print("Please enter length between 1.5 and 10 meters")
        return False
    elif width < 1.5 or width > 10:
        print("Invalid width")
        print("Please enter length between 1.5 and 10 meters")
        return False
    else:
        return True
def main():
    name = input("Enter your name: ")
    customers.append(name)
    room_length = float(input("Enter the length of the room: "))
    length = round(room_length, 1)
    validation()
    room_width = float(input("Enter the width of the room: "))
    validation()
    width = round(room_width, 1)
    validation()
    area_x = length * width
    area = round(area_x)
    wood = input("Enter the type of wood: ")
    for i in range(len(wood_type)):
        if wood == wood_type[i]:
            amount = area * price[i]
    for i in range(len(quotes)):
        for j in range(len(quotes[i])):
            quotes[i][j] = [name, length, width, area, wood, amount]
            print(quotes[i][j])
    for i in range(len(wood_type)):
        if wood == wood_type[i]:
            print(price[i])
    for i in range(len(quotes)):
        for j in range(len(quotes[i])):
            print(quotes[i][j])


main()


    




    


        
 