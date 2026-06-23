"""Efficient cruise ship restaurant booking system.

This keeps the same user-facing behaviour as ``cruise_ship_q.py`` while avoiding
parallel global arrays and repeated scans for the next free table.
"""

from __future__ import annotations

import datetime
from collections import Counter, deque
from dataclasses import dataclass
from typing import Deque

TOTAL_TABLES = 20
SESSION_NAMES = ("Lunch", "Early Dinner", "Late Dinner")
DIETARY_OPTIONS = ("gluten-free", "vegetarian", "vegan", "diabetic", "none")
PLANT_BASED_DIETS = {"vegetarian", "vegan"}


@dataclass(frozen=True)
class Booking:
    """A single restaurant table booking."""

    passenger_name: str
    cabin_number: str
    dietary_requirement: str
    table_number: int


@dataclass
class DiningSession:
    """Bookings and available table numbers for one dining session."""

    name: str
    bookings: list[Booking | None]
    available_tables: Deque[int]

    @classmethod
    def create(cls, name: str) -> "DiningSession":
        return cls(
            name=name,
            bookings=[None] * TOTAL_TABLES,
            available_tables=deque(range(1, TOTAL_TABLES + 1)),
        )

    @property
    def tables_available(self) -> int:
        return len(self.available_tables)

    @property
    def is_full(self) -> bool:
        return not self.available_tables

    def add_booking(
        self,
        passenger_name: str,
        cabin_number: str,
        dietary_requirement: str,
    ) -> Booking:
        if self.is_full:
            raise ValueError(f"{self.name} is fully booked.")

        table_number = self.available_tables.popleft()
        booking = Booking(
            passenger_name=passenger_name,
            cabin_number=cabin_number,
            dietary_requirement=dietary_requirement,
            table_number=table_number,
        )
        self.bookings[table_number - 1] = booking
        return booking


sessions = [DiningSession.create(name) for name in SESSION_NAMES]
dietary_counts: Counter[str] = Counter()


def read_menu_choice(prompt: str, minimum: int, maximum: int) -> int:
    """Read a menu choice and return it as a zero-based index."""
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Error: Please enter a number.")
            continue

        if minimum <= choice <= maximum:
            return choice - 1

        print(f"Error: Please enter a number between {minimum} and {maximum}.")


def read_required_text(prompt: str, field_name: str) -> str:
    """Read a non-empty string from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"Error: {field_name} cannot be empty.")


def display_screen() -> None:
    """Display today's date and table availability."""
    today = datetime.date.today()
    print("\n" + "=" * 40)
    print(f"TODAY'S DATE: {today.strftime('%d/%m/%Y')}")
    print("=" * 40)
    print("RESTAURANT TABLE AVAILABILITY:")

    for session in sessions:
        status = (
            "FULLY BOOKED"
            if session.is_full
            else f"{session.tables_available} tables available"
        )
        print(f"{session.name}: {status}")

    print("=" * 40)


def select_session() -> DiningSession:
    print("Select a session:")
    for index, session in enumerate(sessions, start=1):
        print(f"{index}. {session.name}")

    session_index = read_menu_choice("Enter choice (1-3): ", 1, len(sessions))
    return sessions[session_index]


def select_dietary_requirement() -> str:
    print("\nDietary requirements:")
    for index, option in enumerate(DIETARY_OPTIONS, start=1):
        print(f"{index}. {option}")

    diet_index = read_menu_choice(
        "Select option (1-5): ",
        1,
        len(DIETARY_OPTIONS),
    )
    return DIETARY_OPTIONS[diet_index]


def make_booking() -> None:
    """Make a restaurant booking."""
    print("\nMAKE A BOOKING")
    print("-" * 40)

    session = select_session()
    if session.is_full:
        print(f"Sorry, {session.name} is fully booked.")
        return

    name = read_required_text("Enter passenger name: ", "Name")
    cabin = read_required_text("Enter cabin number: ", "Cabin number")
    diet = select_dietary_requirement()

    booking = session.add_booking(name, cabin, diet)
    if diet in PLANT_BASED_DIETS:
        dietary_counts[diet] += 1

    print("\nBooking confirmed!")
    print(f"Name: {booking.passenger_name}")
    print(f"Cabin: {booking.cabin_number}")
    print(f"Session: {session.name}")
    print(f"Dietary requirement: {booking.dietary_requirement}")
    print(f"Table number: {booking.table_number}")


def display_dietary_summary() -> None:
    """Display vegetarian and vegan booking totals."""
    vegetarian_count = dietary_counts["vegetarian"]
    vegan_count = dietary_counts["vegan"]

    print("\nSPECIAL DIETARY REQUIREMENTS SUMMARY")
    print("-" * 40)
    print(f"Vegetarian: {vegetarian_count} tables")
    print(f"Vegan: {vegan_count} tables")
    print(f"Total plant-based: {vegetarian_count + vegan_count} tables")


def main() -> None:
    while True:
        display_screen()

        print("\nMENU:")
        print("1. Make a booking")
        print("2. Display dietary summary")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

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
