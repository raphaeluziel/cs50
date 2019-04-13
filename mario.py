# Draws a pyramid using #
# Raphael Uziel
# August 22, 2018
# Problem Set 6

from cs50 import get_int

# Prompt user for height
while True:
    h = get_int("Height: ")
    if h <= 23 and h >= 0:
        break

# Draw the pyramid
for i in range(1, h + 1, 1):
    print(" " * (h - i), end="")
    print("#" * i, end="")
    print("  ", end="")
    print("#" * i, end="")
    print()