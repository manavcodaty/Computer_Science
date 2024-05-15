mealSchedule = [["" for i in range(3)] for y in range(7)]


def add_meal():
    for meal in mealSchedule:
        meal[0] = input("Enter the meal you would like to have for breakfast: ")
        meal[1] = input("Enter the meal you would like to have for lunch: ")
        meal[2] = input("Enter the meal you would like to have for dinner: ")


def display_schedule():
    for i in range(7):
        print(f"Day {i+1}:")
        print("--------")
        print(f"Breakfast: {mealSchedule[i][0]}")
        print(f"Lunch: {mealSchedule[i][1]}")
        print(f"Dinner: {mealSchedule[i][2]}")


def change_meal():
    day = int(input("Enter the day you would like to change the meal for: "))
    meal = int(
        input(
            "Enter the meal you would like to change (1 for breakfast, 2 for lunch, 3 for dinner): "
        )
    )
    new_meal = input("Enter the new meal: ")
    mealSchedule[day - 1][meal - 1] = new_meal


def start():
    while True:
        print("1. Add meal")
        print("2. Display schedule")
        print("3. Change meal")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_meal()
        elif choice == 2:
            display_schedule()
        elif choice == 3:
            change_meal()
        elif choice == 4:
            break
        else:
            print("Invalid choice, please try again.")


start()
