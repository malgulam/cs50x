#include <stdio.h>
#include<string.h>
// #include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
//no cs50.h here

//prototypes
int count_sentences(int temp);
int count_words(int temp);
int count_letters(int temp);
float calculate_it();

char *userInput;

int words = 0;
int letters = 0;
int sentences = 0;

int main(){
  userInput =(char*) malloc (sizeof(char) *500);
  //get usrinput
   printf("GG: ");
   fgets(userInput, 499, stdin);
   
  //count letters plus spaces and puncts
  int temp = strlen(userInput);
  
  words = count_words(temp);
  sentences = count_sentences(temp);
  letters = count_letters(temp);
  
//   printf("Word(s)%i\n",words);
//   printf("Letter(s)%i\n",letters);
//   printf(" sentence(s)%i\n",sentences);

//now to calculate it
  int result = (int)calculate_it();
//   printf("%d\n", result);
  if(result < 1)
  {
    printf("Before Grade 1 \n");
  }
  else if(result > 16)
  {
    printf("Grade 16+\n");
  }
  else
  {
    printf("Grade %d\n", result);
  }
  
 
}  
   //count letters
int count_letters(int temp)
{
  //number of things that are not actual letters
  int stuff = 0;
  for (int i =0 ; i< temp; i++)
  {
    if (ispunct(userInput[i]))
    {
      stuff ++;
    }
    else if (isspace(userInput[i]))
    {
      stuff++;
    }
    else
    {
      printf("");
    }
  }
  return temp - stuff;
  
}

//count number of words
int count_words(int temp){
  //this portion dosent add spaces at to the length of the sentences
  int a = 0;
  int b = 0;
  int zz = 1;
  for(int j=0;b==0;j++){
    if(!isalpha(userInput[j])){
     a++;
     }
     else{
       b++;
     }
  }
  for (int i = a;i< temp;i++){
    if(isspace(userInput[i])){
      zz++;
    }
  }
  return zz;

}

int count_sentences(int temp)
{
  char exclamation = '!';
  char fullstop = '.';
  char question = '?';
  
  for (int i = 0; i < temp; i++)
  {
      if(exclamation == userInput[i] || fullstop == userInput[i] || question == userInput[i] ){
       sentences++;// do nothing
    }
  }
      return sentences;
}
float calculate_it(void)
{
    float L = letters/words * 100;
    float S = sentences / words * 100;
    float grade = 0.0588* L - 0.296 * S -15.8;
    int Grade = round(grade);
    return Grade;
    //  double L = 100 *((double) letters / words); 
    //  double S = 100 *((double)sentences / words);
    //  float grade = round(0.0588 * L - 0.296 * S - 15.8);
    //  return (int) round(grade);
}
/*
int count_sentences(int temp)
{
  for (in i = 0; )
}
*/
/*IT WORKS BROOOOOOOOOOOOOO!!!!!!!!!!
SEND ME A MAIL IF YOU ARE DONE WITH WHATEVER YOU DOING
bgfdnyjrtdjrjytrd*/