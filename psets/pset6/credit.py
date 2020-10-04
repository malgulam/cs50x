print('Please what is the cc input number: ')
ccNumber = int(input('number: '))

#function to find credit card type
def cardType(cc):
    global result 
    result = str()
    ccLength = len(cc)
    divisor = 10
    firstNum = cc / divisor
    firstTwoNum = cc / (divisor/10)
    #checking for credit card type
    if firstNum == 4 & ccLength == 13 or ccLength == 16:
        result = "VISA"
    elif firstTwoNum == 34 or firstTwoNum == 37 & ccLength == 15:
        result = "AMEX"
    elif 50 < firstTwoNum &  firstTwoNum < 56 & ccLength == 16:
        result = "MASTERCARD"
    else:
        result = "INVALID"
    return result
#implementation of Luhn Algorithm
def luhnAlgorithm(cc):
    ccLength = len(cc)
    workingcc = cc / 10
    workingcc2 = cc
    tmpccnum = cc
    divisor = 10
    while workingcc > 10:
        LastDigTmp = workingcc % 10
        multByTwo = LastDigTmp * 2
        sum = sum + (multByTwo % 10) + (multByTwo / 10)
        workingcc = workingcc / 100
    while workingcc2 > 0:
        lastDigTmp = workingcc2 % 10
        sum = sum + lastDigTmp
        workingcc2 = workingcc2 / 100
    if sum % 10 == 0:
        cardType(cc)
    else:
        print("INVALID")
luhnAlgorithm(ccNumber)