
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

int evaluate(char * symbols);
int substitution(char *symbols);
int main(int argc , char *argv[]){
    char *symbols = malloc(sizeof(char)*26);
  //check if there are only two comnd line arguments
  if(argc != 2){
    printf("Usage: ./substitution KEY\n");
    return 1;
  }
    else
    {
        symbols = argv[1];
        if (evaluate(symbols) ==0 )
        {
           substitution(symbols);
        }
        else
        {
          return 1;
        }
    }
  }

int evaluate(char * symbols)
{
  //checking symbols length
  int symLength = strlen(symbols);
  if (symLength < 26)
  {
    printf("Must be 26 characters\n");
    return 1;
  }
  else
  {
    //checking each char in symbols to show it's alnum
    for (int i=0; i< symLength; i++)
    {
      if (isalnum(symbols[i]) == 0)
      {
        //checking for repated char
        int counter =0;
        for (int j =0; i< symLength; i++)
        if (symbols[i] == symbols[j])
        {
          counter ++;
        }
        else
        {
          printf("");
        }
        if (counter >1)
        {
          return 1;
        }
        else
        {
          printf("");
        }
      }
      else
      {
        return 1;
      }
    }
  }
  return 0;
}
  
int substitution(char *symbols)
{
  char *plaintext = malloc(sizeof(char)*500);
  char *ciphertext = malloc(sizeof(plaintext));
  char * alphabetsLower = malloc(sizeof(char)*26);
  char *alphabetsUpper = malloc(sizeof(char) *26);
  alphabetsLower = "abcdefghijklmnopqrstuvwxyz";
  alphabetsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  int symLength = strlen(symbols);
  printf("plaintext: ");
  fgets(plaintext, 500, stdin);
  for (int i = 0; i < symLength; i++)
  {
    if (islower(plaintext[i]) == 0)
    {
      char *e = plaintext;
      int index = 0;
      while (*e++ != plaintext[i]) index++;
    // e = strchr(symbols, plaintext[i]);
    // int index_for_character =  (int) (e - symbols);
    plaintext[i] = symbols[index];
    }
    else if (isupper(plaintext[i]) == 0)
    {
      char *e = plaintext;
      int index = 0;
      while (*e++ != plaintext[i]) index++;
    // e = strchr(symbols, plaintext[i]);
    // int index_for_character = (int) (e - symbols);
    plaintext[i] = symbols[index];
    }
  }
  strcpy(ciphertext, plaintext);
  printf("%s", ciphertext);
  return 0;
  
}

//  for (int i=0; i < strlen(plaintext); i++)
//   {
//     // if (isupper(plaintext[i]) != 0)
//     if (isupper(plaintext[i]))
//     {
//       for (int j=0; j < strlen(alphabetsUpper); j++)
//       {
//         if (alphabetsUpper[j] == plaintext[i])
//         {
//           //use the index of the position of the upper text in
//           //alphabets upper in the symbols to encrypt
//           plaintext[i] = symbols[j];
//         }
//         else continue;
//       }
//     }
//     //checking whether it is lower rather
//     // else if(islower(plaintext[i])!= 0)
//     else if(islower(plaintext[i]))
//     {
//        for (int k=0; k < strlen(alphabetsUpper); k++)
//       {
//         if (alphabetsUpper[k] == plaintext[i])
//         {
//           //use the index of the position of the upper text in
//           //alphabets upper in the symbols to encrypt
//           plaintext[i] = symbols[k];
//         }
//         else continue;
//       }
//     }
//     else
//     {
//       printf("not a upper or lower value");
//       break;
//     }
    
//   }

// int getIndexofChar(char *c, char *alphabets, char *symbols)
// {
//   int index =0;
//   for (int i =0; i < strlen(alphabets)+1; i++)
//   {
//     char a = alphabets[i];
//     char h = *c;
//     if (h == a) 
//     {
//       index = index + i;
//       //put break statement here
//       break;
//     }
//     else continue;
//   }
//   //put return index statement here
//   printf("%d", index);
//   return index;
// }

// //symbols is needless in function call