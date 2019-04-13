// Implements a dictionary's functionality
// Raphael Uziel
// August 15, 2018
// Problem set 5

// I chose to implement speller using a has function
// The hash function I chose is djb2
// by Daniel J. Bernstein

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Prototype for the hash function
unsigned int DJBHash(const char *str, unsigned int length);

// Define the node structure
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Setting up global variables
// Trial and error gave me 70000 as the best number of buckets
const int num_buckets = 70000 + 1;
node *head[num_buckets];
node *hashtable[num_buckets];
int num_words = 0;
int i = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Create a copy of the word recieved and convert it to lower case
    char lowerword[46];
    int g = 0;
    while (word[g])
    {
        lowerword[g] = tolower(word[g]);
        g++;
    }
    const char *sendword = lowerword;

    // Send the word to the hash function to know which bucket
    // in the hash table it would be in if it exists
    i = DJBHash(sendword, strlen(word)) % num_buckets;

    // Start the search at the head of the linked list
    node *cursor = head[i];

    // Test each word from the text to see if it matches any of the
    // words in the linked list
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open the dictionary to read from and check to see if it can be opened
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        unload();
        return 1;
    }

    // Read first word from the dictionary and count it
    fscanf(file, "%s", word);
    num_words++;

    // allocate space for the head pointers
    // used calloc instead of malloc since I couldn't figure
    // out how to initialize it to null
    for (int l = 0; l < num_buckets; l++)
    {
        head[l] = calloc(1, sizeof(node));
        if (head[l] ==  0)
        {
            unload();
            return false;
        }
    }

    // Hash the word to find which index of hash table it belongs in
    i = DJBHash(word, strlen(word)) % num_buckets;

    // Copy the word onto the head of that bucket in the hash table
    strcpy(head[i]->word, word);

    // Insert the word into the hash table
    hashtable[i] = head[i];

    while (fscanf(file, "%s", word) != EOF)
    {
        num_words++;
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        // Repeat for all words making sure never to lose
        // pointer to the head of the hash table
        i = DJBHash(word, strlen(word)) % num_buckets;
        strcpy(new_node->word, word);
        hashtable[i] = new_node;
        new_node->next = head[i];
        head[i] = new_node;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // frees up memory created by calloc
    for (int k = 0; k < num_buckets; k++)
    {
        node *cursor = head[k];
        // Frees each node in the linked list without
        // never losing pointer to the head of the list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}

// Hash function by Daniel J. Bernstein
unsigned int DJBHash(const char *str, unsigned int length)
{
    unsigned int hash = 5381;
    unsigned int m = 0;

    for (m = 0; m < length; str++, m++)
    {
        hash = ((hash << 5) + hash) + (*str);
    }

    return hash;
}