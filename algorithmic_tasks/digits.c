#include <stdio.h>
#include <stdlib.h>
#define LOWERBOUND 0
#define UPPERBOUND 2000000000

int main()
{
    int n;
    int number_of_digits = 0;

    scanf("%d", &n);

    // check if n is in the range
    if (n < LOWERBOUND || n > UPPERBOUND)
    {
        printf("invalid input\n");
        exit(1);
    }

    // increment number_of_digits and divide n by 10 while it is greater than 0
    while (n > 0)
    {
        n /= 10;
        number_of_digits++;
    }

    printf("%d\n", number_of_digits);

    return 0;
}