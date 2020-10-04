#imports
import math

def count_letters(txt):
    alpha_count = 0
    for i in range(len(text)):
        if text[i].isalpha():
            alpha_count += 1
        else:
            continue
    return alpha_count

def count_words(txt):
    space_count = 0
    for i in range(len(txt)):
        if txt[i] == " ":
            space_count += 1
        else:
            continue
def count_sentences(txt):
    sentenceCount = 0
    accepted_puncs = ['!', '.', '?']
    #try for dot in txt or?
    for i in range(len(txt)):
        if not txt[i].isalpha():
            if txt[i] in accepted_puncs:
                sentenceCount += 1
            else:
                pass
        else:
            pass
    return sentenceCount

def calculate_it(letters, words, sentences):
    L = float(letters / words * 100)
    S = float (sentences / words * 100)
    grade = float (0.0588* L - 0.296 * S -15.8)
    Grade =  round(grade)
    return Grade
            

def main():
    #get user input
    text = str(input("Text: "))
    tmp = len(text)
    words = count_words(text)
    sentences = count_sentences(tmp)
    #ltters function takes the text, removes all spaces
    #counts the letters
    letters = count_letters(text)

    result =  calculate_it(letters, words, sentences)
    if result < 1:
        print('Before Grade 1')
    elif result > 16:
        print("Grade 16+")
    else:
        print(f'Grade {result}')
main()