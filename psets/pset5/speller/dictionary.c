// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include<stdlib.h>
#include "dictionary.h"

#define HASTABLE_SIZE 1000
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1;

// Hash table
node *hashtable[HASTABLE_SIZE];

unsigned int num_words = 0;
bool is_loaded_dict = false;
//// Hashes word to a number
unsigned int hash(const char* word)
{
    int hash = 0;
    int n = 0;
    for (int i =0 ; word[i] != '\0'; i++)
    {
        if (isalpha(word[i]))
            n =  word[i] - 'a' +1;
        else
            n = 27;
        hash - ((hash << 3) + n) % HASTABLE_SIZE;
    }
    return hash;
}
//// Returns true if word is in dictionary else false
bool check(const char* word)
{
    char check_word[strlen(word)];
    strcpy(check_word, word);
    for (int i = 0; check_word[i] != '\0'; i++)
    {
        check_word[i] = tolower(check_word[i]);
    }
    int index = hash(check_word);
    if(hashtable[index] != NULL)
    {
        for (node* nodeptr = hashtable[index]; nodeptr != NULL; nodeptr = nodeptr->next)
        if (strcmp(nodeptr->word, check_word) == 0)
            return true;
    }
    return false;
}
//// Loads dictionary into memory, returning true if successful else false
bool load(const char* dictionary)
{
    FILE *infile = fopen(dictionary, "r");
    if (infile == NULL)
        return false;
    for (int i = 0; i < HASTABLE_SIZE; i++)
        hashtable[i] = NULL;
    char word[LENGTH + 1];
    node* new_nodeptr;
    while (fscanf(infile, "%s", word) != EOF)
    {
        num_words ++;
        do
        {
            new_nodeptr = malloc(sizeof(node));
            if (new_nodeptr == NULL)
                free(new_nodeptr);
        }
        while(new_nodeptr == NULL);
        strcpy(new_nodeptr->word, word);
        int index = hash(word);
        new_nodeptr-> next = hashtable[index];
        hashtable[index] = new_nodeptr;

    }
    fclose(infile);
    is_loaded_dict = true;
    return true;
}
//// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(is_loaded_dict)
        return 0;
    return num_words;
}
//// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if(!is_loaded_dict)
        return false;
    for(int i = 0; i < HASTABLE_SIZE; i++)
    {
        if (hashtable[i] != NULL)
        {
            node* ptr = hashtable[i];
            while (ptr != NULL)
            {
                node* preptr = ptr;
                ptr = ptr-> next;
                free(preptr);
            }
        }

    }
    return true;
}

