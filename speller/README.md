# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

    *The longest word in the English dictionary.  Used to set a maximum size limit for the array that is to hold the words to be chaecked against the dictionary.  Also defined as a
pneumoconiosis caused by inhalation of very fine silicate or quartz dust.*

## According to its man page, what does `getrusage` do?

    *Returns usage stats for things, specifically in this case the time to load, check, implement size and unload*

## Per that same man page, how many members are in a variable of type `struct rusage`?

    *16*

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

    *Not sure, but I think it's because getrusage changes the values of before and after.  That is its purpose, to measure time, so as time passes, these values will change.*

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

    *It first opens a file for reading, using the line FILE *file = fopen(text, "r");
    The for loop's fgetc(file) part is the trick to advancing the loop, since fgetc(file)
    will return the NEXT character in the file (this would be similar to using i++ counter.
    The c != EOF tells the for loop to stop once the end of the file (EOF) is reached, or rather
    to continue until fgetc returns EOF.  In this manner it reads from the file, one character
    at a time.*

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

    *Not sure, but I think that using fscanf with %s will allow through characters other than
    letters and apostrophes, such as (){}[]+=*^%$#@! etc....*

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

    *The functions are not supposed to change the values, just compare them.*
