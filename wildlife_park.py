ticket_type = ["One Adult", "One Child (An adult may bring up to two children)", "One Senior", "Family Ticket (Up to two adults or seniors, and three children )", "Group of Six or more, price per person"]
day_cost = [20,12,16,60,15]
day_cost_2 = [30,18,24,90,22.50]
extra_attractions = ["Lion feeding", "penguin feeding", "Evening barbecue (two day tickets only)"]  
extra_price = [2.50,2,5]
days = ["+"]*30
bookings = [0]*30
booking_num = 0
num_days = 0

def validation():
    if ticket_type != "One Adult" or "One Child (An adult may bring up to two children)" or "One Senior" or "Family Ticket (Up to two adults or seniors, and three children )" or "Group of Six or more, price per person":
        print("Invalid ticket type")
        add_info()
    elif extra_attractions != "Lion feeding" or "penguin feeding" or "Evening barbecue (two day tickets only)":
        print("Invalid extra attractions")
        add_info()
    elif num_days != 1 or 2:
        print("Invalid number of days")
        add_info()
        
def add_info():
    while True:
        print("Welcome to the Wildlife Park")
        would_like = input("Would you like to book a ticket? (yes/no)")
        if would_like == "yes":
            print("Choose ticket type")
            ticket_type = input()
            validation()
            print("Choose number of days")
            num_days = int(input())
            print("Choose extra attractions")
            extra = input()
            booking_num += 1
            print("Booking number is", booking_num)
            print("Booking details")
            print("Ticket type:", ticket_type)
            print("Number of days:", num_days)
            print("Extra attractions:", extra)
            print("Total cost")
            if num_days == 1:
                for i in range(len(ticket_type)):
                    if ticket_type == i+1:
                        total_cost = day_cost[i]
                for i in range(len(extra_attractions)):
                    if extra == i+1:
                        total_cost += extra_price[i]
                print("Total cost is", total_cost)
            else:
                for i in range(len(ticket_type)):
                    if ticket_type == i+1:
                        total_cost = day_cost_2[i]
                for i in range(len(extra_attractions)):
                    if extra == i+1:
                        total_cost += extra_price[i]
                print("Total cost is", total_cost)
        else:
            break
    
    


def display_info():
    print("Welcome to the Wildlife Park")
    print("Ticket Types")
    for i in range(len(ticket_type)):
        print(i+1, ticket_type[i])
    print("1 Day Cost")
    for i in range(len(day_cost)):
        print(i+1, day_cost[i])
    print("2 day cost")
    for i in range(len(day_cost_2)):
        print(i+1, day_cost_2[i])
    print("Extra Attractions")
    for i in range(len(extra_attractions)):
        print(i+1, extra_attractions[i])
    print("Extra attractions Price")
    for i in range(len(extra_price)):
        print(i+1, extra_price[i])
    print("Available Days")
    print(days)
    
def main():
    print("Welcome to the Wildlife Park")
    print("1: Add booking")
    print("2: Display booking")
    print("3: Check value of a booking")