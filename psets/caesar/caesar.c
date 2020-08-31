//use shell terminal to run because it takes command line arguments

//Mac- Command + Shift + S
//Windows - Control + Shift + S

#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

 // prototypes
int checker(char* argv[]);
char *chyfunc(char *input, int key,unsigned int yah);

int main(int argc , char *argv[]){
  //check if there are only two comnd line arguments
  if(argc != 2){
    printf("Usage: ./caesar [number]\n");
    return 1;
  }
 //returns 0 if argv[1] is not a number else it returns the number
  int cyphnum = checker(argv);
  if(!cyphnum){
     printf("That is not a number,\n");
     return 1;
  }
  //prompt for input and store it in userinput
  char *userinput = malloc(sizeof(char)*500);
  if(userinput == NULL){
    printf("couldn't allocate mem\n");
    return 1;
  }
  printf("Text: ");
  fgets(userinput,500,stdin);

  // length of user string
  unsigned int length = strlen(userinput);
  
  //print cypher code
  printf("Cypher Text: %s\n",chyfunc(userinput,cyphnum,length));

  free(userinput);
  return 0;
 
}
// check if argv[1] is a number
int checker(char *argv[]){
  //returns 0 if it is not a number and if it is a number it returns the number itself
  return atoi(argv[1]);
}
  //rollover loop to cycle through the alphabet through the ASCII code and get the cypher code
char get_char(int character,int key){ 
  // itterate number of times of the key
    for(int j = 0;j<key;j++){
      //If character is Z, make it A
      if(character == 90){
        character = 65;
      }
      //if character is z make it a 
      else if(character == 122){
        character = 97;
      }
      //else character + 1 is equal next alphabet
      else character++;
     }
     return character;
  }
 

//change to cypher code
char *chyfunc(char *input,int key,unsigned int yah){

  //iterrate through the whole text
for (int i = 0; i < yah;i++){
  //if it is an alphabetic letter, enter this rollover loop to cypher code
  if(isalpha(input[i])){
    //copy cypher char into new char
     input[i] = get_char(input[i],key);
  }
 }
 return input;
}



