
"""
Text-Based Shop (CLI)
- Add items, view basket, apply discounts, checkout
- Uses loops for menu + basket totals
- Uses selection (if/elif) for pricing/discount rules
- Extensions: tiered discounts (best-of), promo codes, save/load basket
"""

import json
from pathlib import Path

# ---------- Shop Data ----------
CATALOG = {
    "apples":  {"price": 3.00},
    "bread":   {"price": 4.50},
    "milk":    {"price": 6.00},
    "eggs":    {"price": 12.00},
    "cheese":  {"price": 18.00},
    "chicken": {"price": 25.00},
}

PROMO_CODES = {
    # code: percent off (cart-level)
    "SAVE5":  5,
    "SAVE10": 10,
    "VIP15":  15,
}

SAVE_FILE = Path("basket.json")


# ---------- Basket Helpers ----------
def add_to_basket(basket: dict, item: str, qty: int) -> None:
    if item not in CATALOG:
        print("❌ Item not found in catalog.")
        return
    if qty <= 0:
        print("❌ Quantity must be a positive integer.")
        return

    price = CATALOG[item]["price"]
    if item in basket:
        basket[item]["qty"] += qty
    else:
        basket[item] = {"price": price, "qty": qty}

    print(f"✅ Added {qty} x {item} to basket.")


def remove_from_basket(basket: dict, item: str, qty: int) -> None:
    if item not in basket:
        print("❌ That item is not in your basket.")
        return
    if qty <= 0:
        print("❌ Quantity must be a positive integer.")
        return

    basket[item]["qty"] -= qty
    if basket[item]["qty"] <= 0:
        del basket[item]
        print(f"✅ Removed {item} from basket.")
    else:
        print(f"✅ Removed {qty} x {item}. Now have {basket[item]['qty']}.")


def show_catalog() -> None:
    print("\n--- Catalog ---")
    for name, info in CATALOG.items():
        print(f"- {name:<8} : {info['price']:.2f}")
    print()


def show_basket(basket: dict) -> None:
    if not basket:
        print("\n🧺 Basket is empty.\n")
        return

    print("\n--- Your Basket ---")
    for item, data in basket.items():
        print(f"- {item:<8}  qty={data['qty']:<3}  unit={data['price']:.2f}")
    print()


# ---------- Discount Logic ----------
def compute_subtotal(basket: dict) -> float:
    subtotal = 0.0
    for item, data in basket.items():  # loop through basket to compute totals
        subtotal += data["price"] * data["qty"]
    return subtotal


def bogo_apples_discount(basket: dict) -> float:
    """
    BOGO on apples: for every 2 apples, 1 is free (i.e., pay for ceil(qty/2)).
    Discount = free_apples * unit_price
    """
    if "apples" not in basket:
        return 0.0

    qty = basket["apples"]["qty"]
    unit = basket["apples"]["price"]
    free = qty // 2  # every pair gives 1 free
    return free * unit


def cart_percent_discount_options(is_member: bool, promo_code: str, after_item_discounts: float) -> list:
    """
    Returns possible cart-level percent discounts (name, percent).
    Tiered discounts approach:
      - Item-level discounts (like BOGO) ALWAYS apply.
      - For cart-level discounts, we choose the single BEST percentage discount
        (member vs promo vs spend threshold) to avoid double-discounting.
    """
    options = []

    # Member vs non-member
    if banning := False:  # placeholder to show selection use (not used)
        pass
    if is_member:
        options.append(("Member 5% off", 5))

    # Promo code (validate against a list)
    if promo_code:
        code = promo_code.strip().upper()
        if code in PROMO_CODES:
            options.append((f"Promo {code} ({PROMO_CODES[code]}% off)", PROMO_CODES[code]))
        else:
            options.append(("Invalid promo code (0%)", 0))

    # Spend threshold
    if after_item_discounts > 100:
        options.append(("Spend > 100 (10% off)", 10))

    if not options:
        options.append(("No cart discount (0%)", 0))

    return options


def calculate_bill(basket: dict, is_member: bool, promo_code: str) -> dict:
    """
    Returns a breakdown dict for printing.
    """
    subtotal = compute_subtotal(basket)

    # Item-level discount: BOGO apples
    bogo_discount = bogo_apples_discount(basket)
    after_item_discounts = max(0.0, subtotal - bogo_discount)

    # Tiered cart discounts: choose BEST single percent discount
    options = cart_percent_discount_options(is_member, promo_code, after_item_discounts)
    best_name, best_percent = max(options, key=lambda x: x[1])

    cart_discount = after_item_discounts * (best_percent / 100.0)
    total = max(0.0, after_item_discounts - cart_discount)

    return {
        "subtotal": subtotal,
        "bogo_discount": bogo_discount,
        "after_item_discounts": after_item_discounts,
        "cart_discount_name": best_name,
        "cart_discount_percent": best_percent,
        "cart_discount_value": cart_discount,
        "total": total,
    }


# ---------- Persistence ----------
def save_basket(basket: dict, filename: Path = SAVE_FILE) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(basket, f, indent=2)
    print(f"💾 Basket saved to {filename.resolve()}")


def load_basket(filename: Path = SAVE_FILE) -> dict:
    if not filename.exists():
        print("❌ No saved basket found.")
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Ensure types are correct
    basket = {}
    for item, info in data.items():
        if item in CATALOG and isinstance(info, dict):
            basket[item] = {
                "price": float(info.get("price", CATALOG[item]["price"])),
                "qty": int(info.get("qty", 0)),
            }
            if basket[item]["qty"] <= 0:
                del basket[item]
    print(f"📂 Basket loaded from {filename.resolve()}")
    return basket


# ---------- Input Helpers ----------
def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a whole number.")


def read_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("❌ Please type 'y' or 'n'.")


# ---------- Main Program ----------
def main():
    basket = {}
    promo_code = ""
    is_member = False

    print("🛒 Welcome to the Text Shop!")
    print("You can add items, view basket, apply discounts, and checkout.\n")

    # Persistent menu loop until checkout
    while True:
        print("\n=== MENU ===")
        print("1) Show catalog")
        print("2) Add item to basket")
        print("3) Remove item from basket")
        print("4) View basket")
        print("5) Membership (member vs non-member)")
        print("6) Enter promo code")
        print("7) View bill (with discounts)")
        print("8) Save basket")
        print("9) Load basket")
        print("0) Checkout & exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_catalog()

        elif choice == "2":
            show_catalog()
            item = input("Item name to add: ").strip().lower()
            qty = read_int("Quantity: ")
            add_to_basket(basket, item, qty)

        elif choice == "3":
            show_basket(basket)
            item = input("Item name to remove: ").strip().lower()
            qty = read_int("Quantity to remove: ")
            remove_from_basket(basket, item, qty)

        elif choice == "4":
            show_basket(basket)

        elif choice == "5":
            is_member = read_yes_no("Are you a member? (y/n): ")
            print("✅ Member status set to:", "MEMBER" if is_member else "NON-MEMBER")

        elif choice == "6":
            promo_code = input("Enter promo code (or blank to clear): ").strip().upper()
            if promo_code == "":
                print("✅ Promo code cleared.")
            elif promo_code in PROMO_CODES:
                print(f"✅ Promo code applied: {promo_code} ({PROMO_CODES[promo_code]}% off)")
            else:
                print("⚠️ Promo code not recognized (will count as invalid).")

        elif choice == "7":
            if not basket:
                print("🧺 Basket is empty.")
                continue
            bill = calculate_bill(basket, is_member, promo_code)
            print("\n--- Bill Breakdown ---")
            print(f"Subtotal:              {bill['subtotal']:.2f}")
            print(f"BOGO apples discount:  -{bill['bogo_discount']:.2f}")
            print(f"After item discounts:   {bill['after_item_discounts']:.2f}")
            print(f"Cart discount chosen:   {bill['cart_discount_name']}")
            print(f"Cart discount value:   -{bill['cart_discount_value']:.2f}")
            print(f"TOTAL:                  {bill['total']:.2f}")

        elif choice == "8":
            save_basket(basket)

        elif choice == "9":
            basket = load_basket()

        elif choice == "0":
            if not basket:
                print("\n✅ Checkout complete. (Basket was empty.) Goodbye!")
                break

            bill = calculate_bill(basket, is_member, promo_code)
            print("\n=== CHECKOUT ===")
            show_basket(basket)
            print(f"TOTAL TO PAY: {bill['total']:.2f}")
            print("Thanks for shopping! 👋")
            break

        else:
            print("❌ Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    main()
