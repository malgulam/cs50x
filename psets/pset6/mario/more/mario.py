height = int(input('Height: '))
left_counter =0 
right_counter = 0
for h in range(height):
    left_counter += 1
    right_counter += 1
    left_space = height - left_counter 
    print(' '*left_space, end='')
    print('#'*left_counter, end='')
    print(' ',end=' ')
    print('#'*right_counter)
