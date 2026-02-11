# ==============================
# 1. Calculator Program
# ==============================

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

def calculator():
    print("Simple Calculator")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print("Operations: +, -, *, /")
    op = input("Enter operation: ")

    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        result = divide(num1, num2)
    else:
        result = "Invalid operation"

    print("Result:", result)


# ==============================
# 2. Count Uppercase and Lowercase Letters
# ==============================

def count_case(phrase):
    upper = 0
    lower = 0
    for ch in phrase:
        if ch.isupper():
            upper += 1
        elif ch.islower():
            lower += 1
    return upper, lower

def run_case_counter():
    phrase = input("Enter Phrase: ")
    u, l = count_case(phrase)
    print("No of Upper Case Characters:", u)
    print("No of Lower Case Characters:", l)


# ==============================
# 3. Pangram Checker
# ==============================

import string

def is_pangram(text):
    alphabet = set(string.ascii_lowercase)
    text_letters = set(text.lower())
    return alphabet <= text_letters

def run_pangram():
    phrase = input("Enter Phrase: ")
    if is_pangram(phrase):
        print("This is a pangram.")
    else:
        print("This is not a pangram.")


# ==============================
# 4. Palindrome Checker
# ==============================

def is_palindrome(text):
    cleaned = ''.join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]

def run_palindrome():
    phrase = input("Enter Phrase: ")
    if is_palindrome(phrase):
        print("This is a palindrome.")
    else:
        print("This is not a palindrome.")


# ==============================
# 5. Sort Hyphen-Separated Words
# ==============================

def sort_words(words):
    parts = words.split('-')
    parts.sort()
    return '-'.join(parts)

def run_sort_words():
    phrase = input("Enter Phrase: ")
    print(sort_words(phrase))


# ==============================
# 6. Unique Elements from List
# ==============================

def unique_list(lst):
    unique = []
    for i in lst:
        if i not in unique:
            unique.append(i)
    return unique

def run_unique_list():
    sample = input("Enter Sample List (comma separated): ")
    nums = [int(x) for x in sample.split(',')]
    print(", ".join(str(x) for x in unique_list(nums)))


# ==============================
# 7. Pascal's Triangle
# ==============================

def pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [1]
        if triangle:
            last_row = triangle[-1]
            row.extend([sum(pair) for pair in zip(last_row, last_row[1:])])
            row.append(1)
        triangle.append(row)

    for row in triangle:
        print(' '.join(str(x) for x in row))

def run_pascal():
    num = int(input("Enter the number: "))
    pascal_triangle(num)


# ==============================
# 8. Perfect Number Checker
# ==============================

def is_perfect(n):
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def run_perfect_number():
    num = int(input("Enter the number: "))
    if is_perfect(num):
        print("This number is perfect.")
    else:
        print("This number is not perfect.")


# ==============================
# MAIN MENU
# ==============================

def main():
    while True:
        print("\n===== PYTHON FUNCTION PROGRAMS =====")
        print("1. Calculator")
        print("2. Count Upper/Lower Case Letters")
        print("3. Pangram Checker")
        print("4. Palindrome Checker")
        print("5. Sort Hyphen-Separated Words")
        print("6. Unique Elements from List")
        print("7. Pascal's Triangle")
        print("8. Perfect Number Checker")
        print("9. Exit")

        choice = input("Enter choice (1-9): ")

        if choice == '1':
            calculator()
        elif choice == '2':
            run_case_counter()
        elif choice == '3':
            run_pangram()
        elif choice == '4':
            run_palindrome()
        elif choice == '5':
            run_sort_words()
        elif choice == '6':
            run_unique_list()
        elif choice == '7':
            run_pascal()
        elif choice == '8':
            run_perfect_number()
        elif choice == '9':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
