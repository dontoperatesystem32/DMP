#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LOWERBOUND 1
#define UPPERBOUND 10000

#define MAX_INPUT_SIZE 3072

// to parse string input of integers into an array
int parse_input(char *input, int **array)
{
    char *token;
    int count = 0;
    int *temp_array = malloc(sizeof(int));

    token = strtok(input, " ");
    while (token != NULL)
    {
        temp_array[count] = atoi(token);
        count++;
        temp_array = realloc(temp_array, (count + 1) * sizeof(int));
        token = strtok(NULL, " ");
    }

    *array = temp_array;
    return count;
}

// the algorithm itself implemented using dinamic programming
int knapsack(int s, int *numbers, int num_of_bars)
{
    // define array of maximum weight for each knapsack capacity from 0 to s
    int dp[num_of_bars + 1][s + 1];

    // assign first row and first column to zeros
    for (int i = 0; i <= s; i++)
    {
        dp[0][i] = 0;
    }
    for (int i = 0; i <= num_of_bars; i++)
    {
        dp[i][0] = 0;
    }

    // i for weights
    // j for capacity
    for (int i = 1; i <= num_of_bars; i++)
    {
        for (int j = 1; j <= s; j++)
        {
            // esli nelzya provesti diagonalnuyu strelku
            if (j - numbers[i - 1] < 0)
            {
                dp[i][j] = dp[i - 1][j];
            }
            // esli mojno provesti diag strelku
            else
            {
                if ((dp[i - 1][j - numbers[i - 1]] + numbers[i - 1]) > dp[i - 1][j])
                {
                    dp[i][j] = dp[i - 1][j - numbers[i - 1]] + numbers[i - 1];
                }
                else
                {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
    }

    return dp[num_of_bars][s];
}

int main()
{
    int s;

    // input s
    scanf(" %d ", &s);

    // check if s is in the range
    if (s < LOWERBOUND || s > UPPERBOUND)
    {
        printf("invalid input\n");
        exit(1);
    }

    // input weights
    char input[MAX_INPUT_SIZE];
    fgets(input, MAX_INPUT_SIZE, stdin);
    input[strcspn(input, "\n")] = 0; // remove trailing newline

    int *array;
    int length = parse_input(input, &array);

    // print result

    printf("%d", knapsack(s, array, length));

    return 0;
}