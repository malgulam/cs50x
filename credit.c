#include <cs50.h>
#include <string.h>
#include <stdio.h>
void luhnAlgorithm(long creditcard);
void cardType(long creditcard);
//remainder of any large number %10 is last digit
int main(void)
{
    long cc;
    do{
        printf("Please what is the cc input number: \n");
        printf("number: ");
        scanf("%ld", &cc);
    }
    while(cc<=0);
    luhnAlgorithm(cc);
}

void luhnAlgorithm(long creditcard)
{
 
    int ccLength = 0;
    int sum = 0;

    long divisor = 10;
    long workingcc = creditcard / 10;
    long workingcc2 = creditcard;
  long tmpccnum = creditcard;
    while(tmpccnum != 0)
    {
        tmpccnum = tmpccnum / 10;
        ccLength ++;
    }
    while(workingcc > 0)
    {
        int LastDigTmp = workingcc % 10;
        int multByTwo = LastDigTmp * 2;
        sum = sum + (multByTwo % 10) + (multByTwo / 10);
        workingcc = workingcc / 100;
    }
    
    while (workingcc2> 0)
    {
        int lastDigtmp  = workingcc2 % 10;
        sum = sum + lastDigtmp;
        workingcc2 = workingcc2 / 100;
    }
    
    else
    {
        printf("INVALID\n");
    }
    
}

void cardType(long creditcard)
{
    char result[11];
    int ccLength = 0;
    long divisor = 10;
    
    //checking for the length of the card
    long tmpccnum = creditcard;
    while(tmpccnum != 0)
    {
        tmpccnum = tmpccnum / 10;
        ccLength ++;
    }
    for (int i = 0; i < ccLength - 2; i++)
    {
        divisor = divisor * 10;
    }
        int firstNum = creditcard / divisor;
    int firstTwoNum = creditcard / (divisor /10);
    //first number in ccNum
       if (firstNum == 4 && (ccLength == 13 || ccLength == 16))
        {
            strcpy(result, "VISA");
        }
        else if ((firstTwoNum == 34 || firstTwoNum == 37) && ccLength == 15)
        {
            strcpy(result, "AMEX");
        }
        else if ((50 < firstTwoNum && firstTwoNum < 56) && ccLength == 16)
        {
            strcpy(result, "MASTERCARD");
        }
        else 
        {
            strcpy(result, "INVALID");
        }
  
  

    printf("%s\n", result);
    
        
}
