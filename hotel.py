Guests = [] * 50
Bookings = [[] * 50]
price = [50, 80, 120]
room_type = ["Single", "Double", "Suite"]


def add_guest():
    for i in range(50):
        guest_name = input("Enter the name of the guest: ")
        nights = int(input("Enter the number of nights the guest will be staying: "))
        if nights < 1 or nights > 30:
            print("Invalid number of nights, please try again.")
            i -= 1
            add_guest()
        else:
            print("Night booking is valid")
        room_type = int(
            input("Enter the room type (1 for single, 2 for double, 3 for suite): ")
        )
        print(f"Price for {room_type} room is: {price[room_type-1]}")
        print(
            f"Price for {nights} nights in a {room_type} room is: {price[room_type-1]*nights}"
        )
        Guests[i] = guest_name
        Bookings[i] = [guest_name, nights, room_type]
        print("Guest added successfully.")


add_guest()
