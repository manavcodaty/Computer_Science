# TASK 1 - Setting up the menu.
menu = {
    "FF": {"name": "French fries", "price": 2.00},
    "QP": {"name": "1/4 pound burger", "price": 5.00},
    "QC": {"name": "1/4 pound cheeseburger", "price": 5.55},
    "HP": {"name": "1/2 pound burger", "price": 7.00},
    "HC": {"name": "1/2 pound cheeseburger", "price": 7.50},
    "MP": {"name": "Medium pizza", "price": 9.00},
    "MEP": {"name": "Medium pizza with extra toppings", "price": 11.00},
    "LP": {"name": "Large pizza", "price": 12.00},
    "LEP": {"name": "Large pizza with extra toppings", "price": 14.50},
    "GB": {"name": "Garlic bread", "price": 4.50}
}

def print_menu():
    print("-----------Menu-----------")
    for item_code, item in menu.items():
        print(f"{item_code} - {item['name']} (${item['price']:.2f})")

# TASK 2 - Placing an order.
orders = []
def place_order():
    order = {}
    print("Enter item code and quantity. Enter 'done' when finished.")
    while True:
        item_code = input("Item code: ")
        if item_code.lower() == "done":
            break
        quantity = int(input("Quantity: "))
        order[item_code] = quantity
    order_code = len(orders) + 1
    orders.append({"order_code": order_code, "items": order})
    print_order(order_code)

def print_order(order_code):
    order = orders[order_code - 1]
    total_cost = 0
    print(f"Order code: {order['order_code']}")
    for item_code, quantity in order["items"].items():
        item_name = menu[item_code]["name"]
        item_price = menu[item_code]["price"]
        total_item_cost = item_price * quantity
        total_cost += total_item_cost
        print(f"{item_name} x {quantity} = ${total_item_cost:.2f}")
    print(f"Total cost: ${total_cost:.2f}")

# TASK 3 - Calculating daily takings and profit.
def calculate_takings_and_profit(profit_percentage):
    total_takings = 0
    for order in orders:
        for item_code, quantity in order["items"].items():
            total_takings += menu[item_code]["price"] * quantity
    profit = total_takings * profit_percentage / 100
    print(f"Total daily takings: ${total_takings:.2f}")
    print(f"Profit: ${profit:.2f} ({profit_percentage}%)")
    
    

print_menu()
place_order()
calculate_takings_and_profit(10)
