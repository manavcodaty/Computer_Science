
email = input("Enter email address: ")

has_at = False
has_dot = False
has_space = False

at_position = -1
dot_position = -1

length = len(email)

# Loop through each character (MID equivalent)
for i in range(length):
    char = email[i]

    if char == " ":
        has_space = True
    elif char == "@":
        has_at = True
        at_position = i
    elif char == ".":
        has_dot = True
        dot_position = i

# Check validity
if has_at and has_dot and not has_space and at_position < dot_position:
    print("Valid email address")
else:
    print("Invalid email address")
