import math
print("What is the change owed?")
change_owed = float(input("$: "))

#todo: greedyAlgorithm(change)owed)

def greedyAlgorithm(change):
    global remainder
    global cents
    global totalCoins
    global tmpNumber
    totalCoins = 0
    remainder =0
    cents = 0
    tmpNumber = 0
    #coins lists
    coins = [25, 10, 5, 1]
    cents = round(change * 100)
    for c in range(len(coins)):
        if cents >= coins[c]:
            remainder = cents % coins[c]
            tmpNumber = cents - remainder
            cents = remainder
            totalCoins = totalCoins + tmpNumber / coins[c]
        else:
            continue
    return totalCoins
print(greedyAlgorithm(change_owed))
