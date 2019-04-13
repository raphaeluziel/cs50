# Crack passwords using brute force and crypt
# Raphael Uziel
# August 25, 2018
# Problem Set 6

import crypt
import sys


def Crack_it(salt):
    # Alphabets with frequencies of letter usages
    alphabet = "aeorisntlmdcphbukgyfwjvzxqASERBTMLNPOIDCHGKFJUWYVZQX"

    for A in alphabet:
        key = A
        if crypt.crypt(key, salt) == sys.argv[1]:
            return key
    for A in alphabet:
        for B in alphabet:
            key = A + B
            if crypt.crypt(key, salt) == sys.argv[1]:
                return key
    for A in alphabet:
        for B in alphabet:
            for C in alphabet:
                key = A + B + C
                if crypt.crypt(key, salt) == sys.argv[1]:
                    return key
    for A in alphabet:
        for B in alphabet:
            for C in alphabet:
                for D in alphabet:
                    key = A + B + C + D
                    if crypt.crypt(key, salt) == sys.argv[1]:
                        return key
    for A in alphabet:
        for B in alphabet:
            for C in alphabet:
                for D in alphabet:
                    for E in alphabet:
                        key = A + B + C + D + E
                        if crypt.crypt(key, salt) == sys.argv[1]:
                            return key


# Prompt user for input
while True:
    if len(sys.argv) != 2:
        print("Usage: python crack.py hash")
        break

    # Separate the salt and hash from user input
    salt = sys.argv[1][0:2]
    print(Crack_it(salt))
    break