import datetime

# Constants
TOTAL_TABLES = 20
LUNCH = 0
EARLY_DINNER = 1
LATE_DINNER = 2
SESSION_NAMES = ["Lunch", "Early Dinner", "Late Dinner"]
DIETARY_OPTIONS = ["gluten-free", "vegetarian", "vegan", "diabetic", "none"]

# Function to initialize the booking system


def initialize_system():
    today_date = datetime.date.today()

    # Array to track available tables for each session
    tables_available = [TOTAL_TABLES, TOTAL_TABLES, TOTAL_TABLES]

    # Arrays to track bookings (None means table is available, True means booked)
    lunch_bookings = [None] * TOTAL_TABLES
    early_dinner_bookings = [None] * TOTAL_TABLES
    late_dinner_bookings = [None] * TOTAL_TABLES

    # Arrays to store passenger names for each table
    lunch_names = [""] * TOTAL_TABLES
    early_dinner_names = [""] * TOTAL_TABLES
    late_dinner_names = [""] * TOTAL_TABLES

    # Arrays to store cabin numbers for each table
    lunch_cabins = [""] * TOTAL_TABLES
    early_dinner_cabins = [""] * TOTAL_TABLES
    late_dinner_cabins = [""] * TOTAL_TABLES

    # Arrays to store dietary requirements for each table
    lunch_dietary = [""] * TOTAL_TABLES
    early_dinner_dietary = [""] * TOTAL_TABLES
    late_dinner_dietary = [""] * TOTAL_TABLES

    # Count dietary requirements
    vegetarian_count = 0
    vegan_count = 0

    return (
        today_date,
        tables_available,
        lunch_bookings,
        early_dinner_bookings,
        late_dinner_bookings,
        lunch_names,
        early_dinner_names,
        late_dinner_names,
        lunch_cabins,
        early_dinner_cabins,
        late_dinner_cabins,
        lunch_dietary,
        early_dinner_dietary,
        late_dinner_dietary,
        vegetarian_count,
        vegan_count,
    )


# Function to display table availability


def display_availability(date, tables_available):
    print("\n" + "=" * 50)
    print(f"TODAY'S DATE: {date.strftime('%d/%m/%Y')}")
    print("=" * 50)
    print("RESTAURANT TABLE AVAILABILITY:")
    print("-" * 50)

    for i in range(3):
        status = f"{tables_available[i]} tables available"
        if tables_available[i] == 0:
            status = "FULLY BOOKED"
        print(f"{SESSION_NAMES[i]}: {status}")

    print("-" * 50)


# Function to get valid input


def get_valid_input(prompt, validation_function=None):
    while True:
        user_input = input(prompt)
        if validation_function is None or validation_function(user_input):
            return user_input
        print("Error: Invalid input. Please try again.")


# Function to make a booking


def make_booking(
    tables_available,
    session_bookings,
    session_names,
    session_cabins,
    session_dietary,
    vegetarian_count,
    vegan_count,
):
    print("\nMAKE A TABLE BOOKING")
    print("-" * 50)

    # Get session choice
    print("Choose a session:")
    for i in range(3):
        print(f"{i+1}. {SESSION_NAMES[i]}")

    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("Error: Please enter a number between 1 and 3.")
        except ValueError:
            print("Error: Please enter a valid number.")

    session_index = choice - 1

    # Check if tables are available
    if tables_available[session_index] == 0:
        print(f"Sorry, {SESSION_NAMES[session_index]} is fully booked.")
        return (tables_available, vegetarian_count, vegan_count)

    # Get passenger name
    name = get_valid_input("Enter passenger name: ")

    # Get cabin number
    cabin = get_valid_input(
        "Enter cabin number: ", lambda x: len(x) > 0 and len(x) <= 10
    )

    # Get dietary requirements
    print("\nSpecial dietary requirements:")
    for i, option in enumerate(DIETARY_OPTIONS, 1):
        print(f"{i}. {option}")

    while True:
        try:
            dietary_choice = int(input("Choose an option (1-5): "))
            if 1 <= dietary_choice <= 5:
                break
            else:
                print("Error: Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Please enter a valid number.")

    dietary_requirement = DIETARY_OPTIONS[dietary_choice - 1]

    # Select the correct arrays based on session choice
    if session_index == LUNCH:
        bookings = session_bookings[0]
        names = session_names[0]
        cabins = session_cabins[0]
        dietary = session_dietary[0]
    elif session_index == EARLY_DINNER:
        bookings = session_bookings[1]
        names = session_names[1]
        cabins = session_cabins[1]
        dietary = session_dietary[1]
    else:  # LATE_DINNER
        bookings = session_bookings[2]
        names = session_names[2]
        cabins = session_cabins[2]
        dietary = session_dietary[2]

    # Find available table and book it
    for i in range(TOTAL_TABLES):
        if bookings[i] is None:
            bookings[i] = True
            names[i] = name
            cabins[i] = cabin
            dietary[i] = dietary_requirement

            # Update available tables count
            tables_available[session_index] -= 1

            # Update counts for vegetarian and vegan
            if dietary_requirement == "vegetarian":
                vegetarian_count += 1
            elif dietary_requirement == "vegan":
                vegan_count += 1

            # Display booking confirmation
            print("\nBooking confirmed!")
            print(f"Name: {name}")
            print(f"Cabin: {cabin}")
            print(f"Session: {SESSION_NAMES[session_index]}")
            print(f"Dietary requirement: {dietary_requirement}")
            print(f"Table number: {i + 1}")

            return (tables_available, vegetarian_count, vegan_count)


# Function to display dietary requirements counts


def display_dietary_counts(vegetarian_count, vegan_count):
    print("\nSPECIAL DIETARY REQUIREMENTS SUMMARY")
    print("-" * 50)
    print(f"Vegetarian: {vegetarian_count} tables")
    print(f"Vegan: {vegan_count} tables")
    print(f"Total plant-based diets: {vegetarian_count + vegan_count} tables")


# Main function


def main():
    # Initialize the system
    (
        today_date,
        tables_available,
        lunch_bookings,
        early_dinner_bookings,
        late_dinner_bookings,
        lunch_names,
        early_dinner_names,
        late_dinner_names,
        lunch_cabins,
        early_dinner_cabins,
        late_dinner_cabins,
        lunch_dietary,
        early_dinner_dietary,
        late_dinner_dietary,
        vegetarian_count,
        vegan_count,
    ) = initialize_system()

    # Group session arrays for easier handling
    session_bookings = [lunch_bookings, early_dinner_bookings, late_dinner_bookings]
    session_names = [lunch_names, early_dinner_names, late_dinner_names]
    session_cabins = [lunch_cabins, early_dinner_cabins, late_dinner_cabins]
    session_dietary = [lunch_dietary, early_dinner_dietary, late_dinner_dietary]

    while True:
        display_availability(today_date, tables_available)
        print("\nMENU OPTIONS:")
        print("1. Make a booking")
        print("2. Display dietary requirements summary")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            tables_available, vegetarian_count, vegan_count = make_booking(
                tables_available,
                session_bookings,
                session_names,
                session_cabins,
                session_dietary,
                vegetarian_count,
                vegan_count,
            )
        elif choice == "2":
            display_dietary_counts(vegetarian_count, vegan_count)
        elif choice == "3":
            print("\nThank you for using the Restaurant Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
