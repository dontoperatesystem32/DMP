#include <stdio.h>
#define LOWERBOUND 10
#define UPPERBOUND 1000000

int main()
{
    long amount;
    int banknotes[] = {500, 200, 100, 50, 20, 10};
    int number_of_banknote_types = sizeof(banknotes) / sizeof(banknotes[0]);
    int banknotes_count[number_of_banknote_types]; // each index represents the number of banknotes of the corresponding value
    int number_of_banknotes = 0;
    int i;

    scanf("%d", &amount);

    // chack if n is in the range
    if (amount < LOWERBOUND || amount > UPPERBOUND)
    {
        printf("-1\n");
        return 0;
    }

    // calculate the number of banknotes of each type
    // convenient if printing the number of banknotes of each type is required
    for (i = 0; i < number_of_banknote_types; i++)
    {
        banknotes_count[i] = amount / banknotes[i];
        amount = amount % banknotes[i];
    }

    // calculate the total number of banknotes
    for (i = 0; i < number_of_banknote_types; i++)
    {
        number_of_banknotes += banknotes_count[i];
    }

    printf("%d\n", number_of_banknotes);

    return 0;
}