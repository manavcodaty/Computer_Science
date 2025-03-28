import datetime

# Constants
TOTAL_TABLES = 20
SESSION_NAMES = ["Lunch", "Early Dinner", "Late Dinner"]
DIETARY_OPTIONS = ["gluten-free", "vegetarian", "vegan", "diabetic", "none"]

# Global variables
tables_available = [TOTAL_TABLES, TOTAL_TABLES, TOTAL_TABLES]  # [Lunch, Early, Late]

# Booking arrays - each holds 20 tables for each session
booking_status = [[False] * TOTAL_TABLES for _ in range(3)]  # [session][table]
passenger_names = [[""] * TOTAL_TABLES for _ in range(3)]    # [session][table]
cabin_numbers = [[""] * TOTAL_TABLES for _ in range(3)]      # [session][table]
dietary_reqs = [[""] * TOTAL_TABLES for _ in range(3)]       # [session][table]

# Counters for vegetarian and vegan
veg_count = 0
vegan_count = 0

# Display the date and table availability
def display_screen():
    today = datetime.date.today()
    print("\n" + "=" * 40)
    print(f"TODAY'S DATE: {today.strftime('%d/%m/%Y')}")
    print("=" * 40)
    print("RESTAURANT TABLE AVAILABILITY:")
    
    for i in range(3):
        status = f"{tables_available[i]} tables available"
        if tables_available[i] == 0:
            status = "FULLY BOOKED"
        print(f"{SESSION_NAMES[i]}: {status}")
    
    print("=" * 40)

# Make a booking
def make_booking():
    global veg_count, vegan_count
    
    print("\nMAKE A BOOKING")
    print("-" * 40)
    
    # Get session choice
    print("Select a session:")
    for i in range(3):
        print(f"{i+1}. {SESSION_NAMES[i]}")
    
    while True:
        try:
            session = int(input("Enter choice (1-3): ")) - 1
            if 0 <= session <= 2:
                break
            print("Error: Please enter 1, 2, or 3.")
        except ValueError:
            print("Error: Please enter a number.")
    
    # Check if tables available
    if tables_available[session] == 0:
        print(f"Sorry, {SESSION_NAMES[session]} is fully booked.")
        return
    
    # Get passenger details
    name = input("Enter passenger name: ")
    while name == "":
        print("Error: Name cannot be empty.")
        name = input("Enter passenger name: ")
    
    cabin = input("Enter cabin number: ")
    while cabin == "":
        print("Error: Cabin number cannot be empty.")
        cabin = input("Enter cabin number: ")
    
    # Get dietary requirements
    print("\nDietary requirements:")
    for i in range(len(DIETARY_OPTIONS)):
        print(f"{i+1}. {DIETARY_OPTIONS[i]}")
    
    while True:
        try:
            diet_choice = int(input("Select option (1-5): ")) - 1
            if 0 <= diet_choice <= 4:
                diet = DIETARY_OPTIONS[diet_choice]
                break
            print("Error: Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Please enter a number.")
    
    # Find first available table
    table_num = -1
    for i in range(TOTAL_TABLES):
        if not booking_status[session][i]:
            table_num = i
            break
    
    # Book the table
    booking_status[session][table_num] = True
    passenger_names[session][table_num] = name
    cabin_numbers[session][table_num] = cabin
    dietary_reqs[session][table_num] = diet
    tables_available[session] -= 1
    
    # Update dietary counts
    if diet == "vegetarian":
        veg_count += 1
    elif diet == "vegan":
        vegan_count += 1
    
    # Display confirmation
    print("\nBooking confirmed!")
    print(f"Name: {name}")
    print(f"Cabin: {cabin}")
    print(f"Session: {SESSION_NAMES[session]}")
    print(f"Dietary requirement: {diet}")
    print(f"Table number: {table_num + 1}")

# Display dietary requirements summary
def display_dietary_summary():
    print("\nSPECIAL DIETARY REQUIREMENTS SUMMARY")
    print("-" * 40)
    print(f"Vegetarian: {veg_count} tables")
    print(f"Vegan: {vegan_count} tables")
    print(f"Total plant-based: {veg_count + vegan_count} tables")

# Main program
def main():
    while True:
        display_screen()
        
        print("\nMENU:")
        print("1. Make a booking")
        print("2. Display dietary summary")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            make_booking()
        elif choice == "2":
            display_dietary_summary()
        elif choice == "3":
            print("Thank you for using the booking system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()


    
