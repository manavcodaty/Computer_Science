import pandas as pd

arr = ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0])

df = pd.DataFrame(arr)

print(df)

booking_row = int(input("Enter row number: "))
booking_col = int(input("Enter column number: "))

if df.iloc[booking_row, booking_col] == 0:
    df.iloc[booking_row, booking_col] = 1
    print("Booking successful")
    print(df)
