// Draws a pyramid using #
// Raphael Uziel
// July 13, 2018
// Problem Set 1

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt user for height
    int h = get_int("Height: ");

    while (h > 23 || h < 0)
    {
        h = get_int("Height: ");
    }

    // Draw the pyramid
    for (int i = 1; i <= h; i++)
    {
        // Indent before writing the #
        for (int j = 0; j < h - i; j++)
        {
            printf(" ");
        }
        // Draw a half pyramid of #
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        // Draw a gap between half pyramids
        printf("  ");
        // Draw second half of pyramid
        for (int l = 0; l < i; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}