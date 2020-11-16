//program to print mario blocks to screen based on heights

//libraries
#include <cs50.h>
#include <stdio.h>

//function prototype
void draw(int h);

//main
int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    draw(height);
}


// void draw(int h)
// {
//     int i = 1;
//     int j = 1;
//     int k = 0;
//     for (i = 1; i < h+1; i++)
//     {
//         for (j = 0; j < h- i; j++)
//         {
//             printf(" ");
//         }
//         for (k = 0; k < h - j; k++)
//         {
//             printf("#");
//         }
//         printf("\n");
//     }
// }


//left aligned
// void draw(int h)
// {
//     int i=1;
//     int j = 1;
//     int k =0;
//     for (i =1; i <h +1; i++)
//     {
//         for (j=1; j <= i; j++)
//         {
//             printf("#");
//         }
//         printf("\n");
//     }
// }

void draw(int h)
{
    int i =1;
    int j=1;
    int k = 0;
    int s = 0;
    for (i = 1; i < h+1; i++)
    {
        for (j = 0; j < h-i; j++)
        {
            printf(" ");
        }
        for (k = 0;  k < h - j; k++)
        {
            printf("#");
        }
        printf(" ");
        for (k = 0; k< h - j; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
