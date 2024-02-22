import sys

import pandas as pd

arr = ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0])

df = pd.DataFrame(arr)

print(df)


def make_booking():
    booking_row = int(input("Enter row number: "))
    booking_col = int(input("Enter column number: "))

    if df.iloc[booking_row, booking_col] == 0:
        df.iloc[booking_row, booking_col] = "B"
        print("Booking successful")
        print(df)
    else:
        print("Seat already booked")


print("Would you like to book another seat? (y/n)")
another_booking = input()
if another_booking == "y":
    make_booking()
else:
    sys.exit(0.5)
