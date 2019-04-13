# Check credit card for validity and type (AMEX, VISA, MASTERCARD)
# Raphael Uziel
# August 23, 2018
# Problem Set 6

from cs50 import get_int

# Prompt user for height
h = get_int("Height: ")
if h == 0:
    exit()
while h > 23 or h < 0:
    h = get_int("Height: ")

# Draw the pyramid
for i in range(1, h + 1, 1):
    for j in range(h - i):
        print(" ", end="")
    for k in range(i):
        print("#", end="")
    print("  ", end="")
    for l in range(i):
        print("#", end="")
    print()