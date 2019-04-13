// Helper functions for music
// Raphael Uziel
// July 27, 2018
// Problem set 2

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "helpers.h"

#define A4 440  // The frequency of A4, the reference
#define aTwelfth 0.083333333333 // Power to increase frequencies by a semitone

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    char Xstr[] = { '1', '\0' };
    char Ystr[] = { '1', '\0' };

    Xstr[0] = fraction[0];
    Ystr[0] = fraction[2];

    int X = atoi(Xstr);
    int Y = atoi(Ystr);

    return 8 * X / Y;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    char noteSequence[] = { 'C', '#', 'D', '#', 'E', 'F', '#', 'G', '#', 'A', '#', 'B', '\0' };

    // Convert the note (ex, B#5) into a note(B), and accidental(#), and an octave(5)
    char noteChar;
    char accidentalChar;
    char octaveChar;

    noteChar = note[0];
    int numberSemitones = 0;
    float power = 0;

    // Compare note to the array to see how many semitones it's from A4
    for (int i = 0; i < 12; i++)
    {
        if (noteSequence[i] == noteChar)
        {
            numberSemitones = i - 9;
        }
    }
    // Adjust semitones up if #, and down if b
    if (note[1] == '#')
    {
        accidentalChar = note[1];
        octaveChar = note[2];
        numberSemitones += 1;
    }
    else if (note[1] == 'b')
    {
        accidentalChar = note[1];
        octaveChar = note[2];
        numberSemitones -= 1;
    }
    else
    {
        accidentalChar = 'X';
        octaveChar = note[1];
    }

    float freq = A4;
    int octaveNumber = (int) octaveChar - 48;
    power = (float)numberSemitones / 12;

    freq = A4 * pow(2, octaveNumber - 4) * pow(2, power);

    return (int) round(freq);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}
