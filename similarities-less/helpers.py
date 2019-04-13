def lines(a, b):
    """Return lines in both a and b"""

    # Split the strings received parameters of function lines into lists
    # splitlines being a method of string which splits into lines
    one = a.splitlines()
    two = b.splitlines()

    duplicates = []

    # Iterate through each line of one, and check to see if it is in two
    # if so, add it to the duplicates list, unless that string is already there
    for i in one:
        if i in two:
            if not i in duplicates:
                duplicates.append(i)

    return duplicates


def sentences(a, b):
    """Return sentences in both a and b"""
    from nltk.tokenize import sent_tokenize

    # Split string using imported method into sentences (separated by .!?)
    one = sent_tokenize(a)
    two = sent_tokenize(b)

    duplicates = []

    # Iterate as done in previous function
    for i in one:
        if i in two:
            if not i in duplicates:
                duplicates.append(i)

    return duplicates


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Function to chop string into substrings
    def chop(text, n):
        splittext = []
        k = 0
        while k < len(text) - n + 1:
            splittext.append(text[k:k + n])
            k += 1
        return splittext

    one = chop(a, n)
    two = chop(b, n)

    duplicates = []

    # Iterate as done before in the two previous functions
    for i in one:
        if i in two:
            if not i in duplicates:
                duplicates.append(i)

    return duplicates
