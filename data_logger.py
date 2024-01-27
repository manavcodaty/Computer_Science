import time

midday_temps = [0] * 30
midnight_temps = [0] * 30


def enter_temps():
    for i in range(30):
        midday_temps[i] = int(input(f"Enter midday temperature for day {i + 1}: "))
        validate_temps()
        midnight_temps[i] = int(input(f"Enter midnight temperature for day {i + 1}: "))
        validate_temps()
        
def validate_temps():
    for i in range(30):
        if midday_temps[i] < 10 or midday_temps[i] > 55:
            print(f"Invalid midday temperature for day {i + 1}.")
            time.sleep(0.5)
            enter_temps()
            
        if midnight_temps[i] < 0 or midnight_temps[i] > 35:
            print(f"Invalid midnight temperature for day {i + 1}.")
            time.sleep(0.5)
            enter_temps()
            
            
            
def average_temp():
    total = 0
    for i in range(30):
        total += midday_temps[i]
    average = total / 30
    print(f"Average midday temperature: {average:.2f}")
    
    total = 0
    for i in range(30):
        total += midnight_temps[i]
    average = total / 30
    print(f"Average midnight temperature: {average:.2f}")
    
    
    
def hottest_coldest_day():
    hottest = 0
    coldest = 0
    for i in range(30):
        if midday_temps[i] > midday_temps[hottest]:
            hottest = i
        if midnight_temps[i] < midnight_temps[coldest]:
            coldest = i
    print(f"Hottest day: {hottest + 1}")
    print(f"Coldest day: {coldest + 1}")
    
    
    
enter_temps()
average_temp()
hottest_coldest_day()
