# Questions

## What's `stdint.h`?

    *Definitions of fixed width integer types*

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

    *Specifies the number of bits exactly, so that a computer that uses
    different numbers of bits will still have to use the specified number
    of bits that the program requires.*

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

    *BYTE = 8 bit unsigned char
    *DWORD = 32 bit unsigned long integer
    *LONG = 32 bit signed integer
    *WORD = 16 bit unsigned integer

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

    BM (hexadecimal characters)

## What's the difference between `bfSize` and `biSize`?

    *bfSize is the size of the bitmap file (total), while biSize is the
    size of the structure (the BITMAPINFOHEADER)*

## What does it mean if `biHeight` is negative?

    *Negative for biHeight means the information is top-down, where the first
    RGBTRIPLE gives information about the top-left corner fo the image first.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

    biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

    *If the file it's trying to open does not exist?  File pointers need to
    point to NULL initially, otherwise they can point to areas of RAM that
    shouldn't be accessed*

## Why is the third argument to `fread` always `1` in our code?

    *Because we are only reading in one pixel at a time?**

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

    *Padding = 3 (on line 63, not 65, I think)*

## What does `fseek` do?

    *Allows you to move forward and backwards within a file*

## What is `SEEK_CUR`?
    *When using fseek, SEEK_CUR tells the offset to be measured
    relative to the current position as opposed to the beginning
    of the file*

## Whodunit?

    *It was Professor Plum with the candlestick in the library*
