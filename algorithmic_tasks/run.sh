#!/bin/bash

# Function to compile the specified program
compile() {
    program=$1
    gcc -Wall -Wextra -pedantic -std=c11 -o "$program" "$program.c"
    if [ $? -ne 0 ]; then
        echo "Compilation of $program failed."
        exit 1
    fi
}

# Function to clean up the compiled files
clean() {
    rm -f atm digits knapsack *.o
    echo "Cleaned up compiled files."
}

# Check the input argument
if [ "$#" -ne 1 ]; then
    echo "Usage: sh run.sh [ atm | digits | knapsack | clear ]"
    exit 1
fi

# Handle the input argument
case $1 in
    atm)
        compile atm
        ./atm
        ;;
    digits)
        compile digits
        ./digits
        ;;
    knapsack)
        compile knapsack
        ./knapsack
        ;;
    clear)
        clean
        ;;
    *)
        echo "Invalid input. Usage: sh run.sh [ atm | digits | knapsack | clear ]"
        exit 1
        ;;
esac
