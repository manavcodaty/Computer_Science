from __future__ import annotations

from typing import List, Optional, Tuple

# =========================================================
# 1) BANKING SYSTEM — BvRef/BvVal
# =========================================================
# We store the balance in a mutable dict so it can be updated "by reference".
# Transaction details (amount, type) are plain values (by value).


def process_transaction(
    balance_ref: dict,
    amount: float,
    tx_type: str,
    tx_log_ref: Optional[List[Tuple[str, float, float]]] = None,
) -> None:
    """
    Updates balance_ref['balance'] in place (BvRef).
    tx_type: 'deposit' or 'withdraw'
    amount: positive number (BvVal)
    tx_log_ref: BvRef transaction log; appends (type, amount, new_balance)
    """
    if "balance" not in balance_ref:
        raise KeyError("balance_ref must contain key 'balance'")

    if amount < 0:
        raise ValueError("amount must be non-negative")

    if tx_type == "deposit":
        balance_ref["balance"] += amount
    elif tx_type == "withdraw":
        balance_ref["balance"] -= amount
    else:
        raise ValueError("tx_type must be 'deposit' or 'withdraw'")

    if tx_log_ref is not None:
        tx_log_ref.append((tx_type, amount, balance_ref["balance"]))


def get_balance(balance_val: float) -> float:
    """Returns the current balance (BvVal)."""
    return balance_val


# =========================================================
# 2) SCHOOL ARRAYS — AddStudent (BvRef) & AverageGrade (BvVal)
# =========================================================


def add_student(
    names_ref: List[str], grades_ref: List[float], name: str, grade: float
) -> None:
    """Updates the arrays in place (BvRef)."""
    names_ref.append(name)
    grades_ref.append(float(grade))


def average_grade(grades_val: List[float]) -> float:
    """Returns the average grade (BvVal)."""
    return sum(grades_val) / len(grades_val) if grades_val else 0.0


# --- Extensions ---
def update_grade(
    grades_ref: List[float], names_val: List[str], name: str, new_grade: float
) -> bool:
    """
    Changes a student's grade (BvRef for grades, BvVal for the rest).
    Returns True if updated, False if name not found.
    """
    try:
        i = names_val.index(name)
        grades_ref[i] = float(new_grade)
        return True
    except ValueError:
        return False


def find_top_student(
    names_val: List[str], grades_val: List[float]
) -> Tuple[Optional[str], Optional[float]]:
    """Returns (name, grade) of the highest-scoring student, or (None, None) if empty."""
    if not grades_val:
        return None, None
    i = max(range(len(grades_val)), key=lambda k: grades_val[k])
    return names_val[i], grades_val[i]


# =========================================================
# 3) SORTING — Swap (BvRef) + Bubble Sort (optimised)
# =========================================================


def swap(arr_ref: List[int], i: int, j: int) -> None:
    """Exchanges two values in arr_ref in place (BvRef)."""
    arr_ref[i], arr_ref[j] = arr_ref[j], arr_ref[i]


def is_sorted(numbers_val: List[int]) -> bool:
    """Returns True if already in non-decreasing order (BvVal)."""
    return all(
        numbers_val[i] <= numbers_val[i + 1] for i in range(len(numbers_val) - 1)
    )


def bubble_sort(arr_ref: List[int]) -> None:
    """
    In-place bubble sort using swap(). Optimised to stop early if no swaps occur in a pass.
    """
    n = len(arr_ref)
    if n < 2 or is_sorted(arr_ref):  # early exit if already sorted
        return

    last_unswapped = n - 1
    while last_unswapped > 0:
        new_last_unswapped = 0
        swapped = False
        for i in range(last_unswapped):
            if arr_ref[i] > arr_ref[i + 1]:
                swap(arr_ref, i, i + 1)
                swapped = True
                new_last_unswapped = i
        if not swapped:  # fully sorted; stop early
            break
        last_unswapped = new_last_unswapped


# =========================================================
# DEMO
# =========================================================
if __name__ == "__main__":
    print("=== 1) BANKING ===")
    account = {"balance": 1000.0}  # BvRef container
    log: List[Tuple[str, float, float]] = []
    process_transaction(account, 250.0, "deposit", log)
    process_transaction(account, 90.0, "withdraw", log)
    print("Balance (ref):", account["balance"])
    print("Balance (val):", get_balance(account["balance"]))
    print("Transaction log:", log)

    print("\n=== 2) SCHOOL ARRAYS ===")
    names, grades = [], []
    add_student(names, grades, "Samir", 84)
    add_student(names, grades, "Maya", 92)
    add_student(names, grades, "Alex", 77)
    print("Names:", names)
    print("Grades:", grades)
    print("Average:", average_grade(grades))
    updated = update_grade(grades, names, "Alex", 83)
    print("Updated Alex?", updated, "->", grades)
    top_name, top_grade = find_top_student(names, grades)
    print("Top student:", top_name, top_grade)

    print("\n=== 3) BUBBLE SORT ===")
    arr = [5, 1, 4, 2, 8, 0, 2]
    print("Before:", arr, "is_sorted?", is_sorted(arr))
    bubble_sort(arr)
    print("After: ", arr, "is_sorted?", is_sorted(arr))
