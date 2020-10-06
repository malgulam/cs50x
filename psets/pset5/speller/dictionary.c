// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 456976;

//number of counted nodes
unsigned int count = 0;

// Hash table
node *table[N];

//set all pointers to null
void set_null(){
    for(int i = 0;i < N; i++){
        table[i] = NULL;
    }
}
//makes strings lower case
void makelower(char *str){
    for(int i = 0;str[i]; i++){
  str[i] = tolower(str[i]);
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //create temp variable and store word in it
    /*This is because hash table works with ascii values and uppercase and lower case
    do not have the same values so produce different results in hash function*/
    char hi[LENGTH];
    strcpy(hi,word);
    makelower(hi);

   //Allocate memory for temp node
   unsigned int hash_value = hash(hi);
   node *fake;

   //temp points to first thing list head is pointing at
   if(table[hash_value] == NULL) return false;
   fake = table[hash_value];

   //while the two are not matching check if there is no address in next to go to
   while(strcmp(hi,fake->word) != 0){
       if(fake->next == NULL) return false;
       else fake = fake->next;
   }
   return true;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
     unsigned int length = strlen(word);
     unsigned int  hash_value = 0;
     for(int j = 0; j < length; j++){
         hash_value += word[j];
         hash_value *= LENGTH;
         hash_value = (hash_value * word[j]) % N;
     }
     return hash_value;
}



// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    //open dictionary file
   FILE *yeah = fopen(dictionary,"r");
       if (yeah == NULL) return false;

       //create buffer to put strings in
       char *buffer = (char *)malloc(sizeof(char) * LENGTH);
       if(buffer == NULL){
           fclose(yeah);
           return false;
       }

       //set all pointers to NULL in table
       set_null();

       //add words and put new nodes in hash table
       while(fscanf(yeah, "%s",buffer) != EOF){
           //create node for that word
           node *tmp =(node *) malloc(sizeof(node));
           if(tmp == NULL){
               fclose(yeah);
               free(buffer);
               return false;
           }
           tmp->next = NULL;
           //make all words in the loaded dictionary lower case
           makelower(buffer);
           strcpy(tmp->word,buffer);

           //get hash value
          unsigned int hash_value = hash(buffer);

           //check the situation of the node and how to fit it into table
           if(table[hash_value] == NULL){
               table[hash_value] = tmp;

           }
           else{
               tmp->next = table[hash_value];
               table[hash_value] = tmp;
           }
           count++;

       }
       fclose(yeah);
       free(buffer);
       return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
     return count;
}
//function that uses recursion to delete nodes
void deletenodes(node *temp){
    if(temp==NULL)return;
    else{
        deletenodes(temp->next);
        free(temp);
    }
}
// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
   for(int i = 0;i<N;i++){
       deletenodes(table[i]);
   }
   return true;
}

