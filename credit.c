// Check credit card for validity and type (AMEX, VISA, MASTERCARD)
// Raphael Uziel
// July 13, 2018
// Problem set 1

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get input from user and initialize some variables
    long long credit = 0;
    long long power = 10000000000000000;
    int checksum = 0;

    // Check if user gave a positive number, otherwise repromt
    do
    {
        credit = get_long_long("Credit Card Number: ");
    }
    while (credit < 0);
    long long num = credit;

    // Test for validity using Luhn’s algorithm
    for (int i = 16; i > 0; i--)
    {
        power /= 10;
        // Add the odd placed numbers
        if (i % 2 == 1)
        {
            checksum += (num - num % power) / power;
        }
        // Multiply the even places by two, then add the digits
        else
        {
            checksum += ((num - num % power) * 2) / power / 10;
            checksum += ((num - num % power) * 2) / power % 10;
        }
        num = num % power;
    }

    // Get the last digit of the checksum
    checksum = checksum % 10;

    // If checksum is valid determine which card it is based
    // on number of digits and first one or two numbers
    power = 10000000000000000;
    if (checksum == 0)
    {
        if (credit >= power / 10)
        {
            if (credit * 10 / power == 4)
            {
                printf("VISA\n");
                return 0;
            }
            else if (credit * 100 / power > 50 && credit * 100 / power < 56)
            {
                printf("MASTERCARD\n");
                return 0;
            }
            else
            {
                printf("INVALID\n");
                return 0;
            }
        }
        if (credit >= power / 100)
        {
            if (credit * 1000 / power == 34 || credit * 1000 / power == 37)
            {
                printf("AMEX\n");
                return 0;
            }
            else
            {
                printf("INVALID\n");
                return 0;
            }
        }
        if (credit <= power / 1000 && credit >= power / 10000)
        {
            if (credit * 10000 / power == 4)
            {
                printf("VISA\n");
                return 0;
            }
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}