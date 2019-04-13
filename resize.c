// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize f infile oufile\n");
        return 1;
    }

    // parse float input
    double fl = 1.0;
    sscanf(argv[1], "%lf\n", &fl);
    int f = (int) fl;

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // outfile's new header informatiion variables
    BITMAPFILEHEADER bfout = bf;
    BITMAPINFOHEADER biout = bi;

    biout.biWidth *= f;
    biout.biHeight *= f;
    int paddingout = (4 - (biout.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    biout.biSizeImage = ((sizeof(RGBTRIPLE) * biout.biWidth) + paddingout) * abs(biout.biHeight);
    bfout.bfSize = biout.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfout, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biout, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // create temporary array to hold one line of the resized image
        RGBTRIPLE *tripleArray = malloc(f * bi.biWidth * sizeof(RGBTRIPLE));

        // iterate over pixels in scanline of infile
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage of a single triple RGB value
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // add f times each pixel of infile into temporary outfile array
            for (int counter = j * f; counter < (j + 1) * f; counter++)
            {
                tripleArray[counter] = triple;
            }
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // repeat each line f times
        for (int l = 0; l < f; l++)
        {
            // write out one line to the output file
            for (int m = 0; m < biout.biWidth; m++)
            {
                fwrite(&tripleArray[m], sizeof(RGBTRIPLE), 1, outptr);
            }
            // add padding
            for (int k = 0; k < paddingout; k++)
            {
                fputc(0x00, outptr);
            }
        }

        free(tripleArray);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
