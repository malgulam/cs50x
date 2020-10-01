#!/usr/bin/python2

# please don't use python 2, it is deprecated!
# use python 3 instead

left_align_counter =  0
print("Printing  left aligned")
print("Height: ", end="")
height =  int(input())

for h in range(height):
    left_align_counter +=1 
    print("#"*left_align_counter)

print("DONE.")

right_align_counter = 0
print("Printing right align ")

for h in range(height):
    right_align_counter += 1
    print(" "*int(height-right_align_counter), end="")
    print("#"*int(right_align_counter))
    
print("DONE.")

#here we can use any counter for the blocks be it right or left so just use counter variable
counter = 0
for h in range(height):
    counter += 1
    print(" "*int(height-counter), end="")
    print("#"*int(counter), end=' ')
    print("#"*int(counter),end="\n")
  
    
