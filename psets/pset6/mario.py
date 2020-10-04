height = int(input('Height: '))
counter = 0
for i in range(height):
    counter += 1
    space_counter = height-counter
    print(' '*space_counter, end='')
    print('#'*counter)

