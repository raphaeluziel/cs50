// Use Caesar's Cipher to convert plain text to encrypted text
// Raphael Uziel
// July 20, 2018
// Problem set 2

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // User begins program passing the k value to main
    string plaintext;
    if (argc == 2)
    {
        plaintext = get_string("plaintext: ");
    }
    else
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // Convert input to integer for k
    int k = atoi(argv[1]);

    // Encrypt each letter of plaintext to the encrypted text
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                plaintext[i] = (plaintext[i] - 'A' + k) % 26 + 'A';
            }
            else
            {
                plaintext[i] = (plaintext[i] - 'a' + k) % 26 + 'a';
            }
        }
    }

    printf("ciphertext: %s\n", plaintext);
}