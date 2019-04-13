#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Useage: ./recover image\n");
        return 1;
    }

    // open the forensic image file
    FILE *inputfilepointer = fopen(argv[1], "r");
    if (inputfilepointer == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // setup some variables
    BYTE imagearray[512];
    char imagefilenames[] = { 'a', 'b', 'c', 'p', 'j', 'p', 'g', '\0' };
    int imgcount = 0;
    FILE *recoveredimagesfilepointer;

    while (fread(&imagearray, 512, 1, inputfilepointer) != 0)
    {
        if (imagearray[0] == 0xff && imagearray[1] == 0xd8 &&
            imagearray[2] == 0xff && (imagearray[3] & 0xf0) == 0xe0)
        {
            imgcount++;

            // generate a name for the next image file
            sprintf(imagefilenames, "%03i.jpg", imgcount - 1);

            // open a file for writing recovered images to
            recoveredimagesfilepointer = fopen(imagefilenames, "w");
            if (recoveredimagesfilepointer == NULL)
            {
                fclose(inputfilepointer);
                fprintf(stderr, "Could not create %s.\n", imagefilenames);
                return 3;
            }
            fwrite(&imagearray, 512, 1, recoveredimagesfilepointer);
        }
        else if (imgcount)
        {
            fwrite(&imagearray, 512, 1, recoveredimagesfilepointer);
        }
    }

    // close infile
    fclose(inputfilepointer);

    // close outfile
    fclose(recoveredimagesfilepointer);

    // success
    return 0;
}


