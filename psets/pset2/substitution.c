
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <locale.h>
#include <limits.h>

//prototypes
int evaluateLength(char * symbols);
int characterEvaluate(char *symbols, int symLength);
void substitution(char *symbols);
int  getIndexofChar(char *c, char *alphabets, char *symbols);

int main(int argc, char *argv[])
{
  char *symbols = malloc(sizeof(char)*26);
  if (argc != 2)
  {
    printf("Usage: ./substitution KEY\n");
    return 1;
  }
  else
  {
    symbols = argv[1];
  }
  evaluateLength(symbols);

}
int evaluateLength(char * symbols)
{
  //check symbols length
  int symLength =  strlen(symbols);
  if (symLength<26 || symLength>26)
  {
    printf("Must be 26 characaters\n");
    return 1;
  }
  else
  {
    characterEvaluate(symbols, symLength);
  }
  return 0;
}

int characterEvaluate(char *symbols, int symLength)
{
  //checking each character whether it is alpha
  for (int i=0; i < symLength; i++)
  {
    char c = symbols[i];
    if (isalpha(c) != 0)
    {
      continue;
    }
    else
    {
      printf("Not alpha character %c", c);
      return 1;
    }

  }
  //symbolsARRAY
  char symbolsARRAY[26];
  //appending all chars to symbolsARRAY
  for (int i=0; i<symLength; i++)
  {
    char c = symbols[i];
    symbolsARRAY[i] = c;
  }
  //checking for repeated characters
  for (int i=0; i <symLength; i++)
  {
    char c = symbols[i];
    int counter = 0;
    //checking for repeated chars in symbolsARRAY
    for (int  j=0; j<symLength+1; j++)
    {
      if (symbolsARRAY[j] == c) counter++;
      else continue;
    }
    if (counter >1)
    {
      printf("Repeated  character %c", c);
      return 1;
    }
    else continue;
  }
  substitution(symbols);
  return 0;
}

void substitution(char *symbols)
{
  //remember to free(symbols)
  //free(alphabetsUpper)
  //free(alphabetsLower)
  //free(plaintext)
  //free(ciphertext)
  char *alphabetsUpper = malloc(sizeof(char)*26);
  char *alphabetsLower = malloc(sizeof(char) *26);
  //getting plaintext
  char *plaintext = malloc(sizeof(char) *500);
  printf("plaintext: ");
  fgets(plaintext, 500, stdin);
  //allocating space for ciphertext
  char *ciphertext = malloc(sizeof(plaintext));
  alphabetsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  alphabetsLower = "abcdefghijklmnopqrstuvwxyz";

  for (int i=0; i < strlen(plaintext)-1; i++)
  {
    int index;
    char c = plaintext[i];
    if (isupper(c) !=0 )
    {
      index = getIndexofChar(&c, alphabetsUpper, symbols);
      // printf("%d", index);
      ciphertext[i] = symbols[index];
    }
    else
    {
      index = getIndexofChar(&c, alphabetsLower, symbols);
      // printf("%d", index);
      ciphertext[i] = tolower(symbols[index]);
    }
  }
  // strcpy(ciphertext, plaintext);
  printf("ciphertext: %s\n", ciphertext);
  // printf("%s\n", ciphertext);

  // free(symbols);
  // free(alphabetsUpper);
  // free(alphabetsLower);
  // free(plaintext);
  // free(ciphertext);
}
int getIndexofChar(char *c, char *alphabets, char *symbols)
{
  //pass func
  // void pass()
  // {
  //   __asm__("nop");
  // }
  int index =0;
  int alphabetsLen = strlen(alphabets);
  char h = *c;
  for (int i=0; i < alphabetsLen; i++)
  {
    
    char a = alphabets[i];
    if (a == h)
    {
      index = index + i;
      return index;
      break;
    }
    else 
    {
      
    }
  }
  
  return 0;
}