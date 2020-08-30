import sys
import logging
#user input is plain text
def encrypt(key, userInput):
  cipherText = ""
  symbolsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"#this is inefficient but I will change it latter
  symbolsLower = "abcdefghijklmnopqrstuvwxyz" #i reckon list for it's speed but I will use string
  for i in range(len(userInput)):
    #checking for alnum
    if userInput[i].isalnum():
     "checking whther it is uppert"

    if str(userInput[i]).isupper():
      pos_upper = symbolsUpper.find(userInput[i]) + key
      if pos_upper >= 25:
        #wrap around
        new_upper_pos = pos_upper -  len(symbolsUpper) 
        cipherText += symbolsUpper[new_upper_pos]
      else:
        cipherText += symbolsUpper[pos_upper]
    elif str(userInput[i]).islower():
      pos_lower = symbolsLower.find(userInput[i]) + key
      if pos_lower >= 25:
        #wrap around lower 
        new_lower_pos = pos_lower - len(symbolsLower) 
        cipherText += symbolsLower[new_lower_pos]
      else:
        cipherText += symbolsLower[pos_lower]
        
    else:
      cipherText += userInput[i]
  print(f"ciphertext: {cipherText}")
def wrap_around(character, key):
    symbolsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"#this is inefficient but I will change it latter
    symbolsLower = "abcdefghijklmnopqrstuvwxyz" #i reckon list for it's speed but I will use string
    if character.islower():
        pos = symbolsLower.find(character) + key
        if 25 % pos == 0:
            pos =  25 - int(pos)
        else:
            pass
    elif character.isupper():
        pos = symbolsUpper.find(character) + key
        if 25 % pos == 0:
            pos = symbolsUpper.find(character) + key
        else:
            pass
    else:
        pass
    return pos
            
        



  

def main():
  #logger = logging.basicConfig()
  print("the syntax is python3 main 1 where 1 is the key")
  if len(sys.argv) <= 1:
    print("the syntax is python3 main 1 where 1 is the key")
    exit(1)
  else:
      
      Cipherkey = int(sys.argv[1])
      text = str(input("Text: "))
  encrypt(key=Cipherkey, userInput=text)
  

if __name__ == "__main__":
  main()


# def shiftcode(key,usrinput):
#   uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#   lowercase = "abcdefghijklmnopqrstuvwxyz"
#   cyphercode= []
#   for i in range(len(usrinput)):
#     if i.strip() and i in uppercode:
#       cyphercode.append(str((usrinput[i] + key) % 26))
#     elif i.strip() and i in lowercode:
#       cyphercode.append(str(usrinput[i] + key ) % 26)
#   return cyphercode
