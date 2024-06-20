# Algorithmic Tasks Written in C

This repository contains three C programs: `atm`, `digits`, and `knapsack`. The provided shell script `run.sh` allows you to compile and execute these programs or clean up the compiled files.

## Prerequisites

- **GCC Compiler**: It is recommended to have GCC version 9.2.0 or later installed to compile these C programs.

You can check your GCC version by running:
```sh
gcc --version
```

## Files

- `atm.c`: Source file for the ATM program.
- `digits.c`: Source file for the Digits program.
- `knapsack.c`: Source file for the Knapsack program.
- `run.sh`: Shell script to compile and run the programs or clean up the compiled files.

## Usage

### Compiling and Running Programs

The `run.sh` script allows you to compile and run any of the three programs. The script takes one argument which specifies the program to compile and run, or the `clear` command to clean up the compiled files.

#### Running the ATM Program

```sh
sh run.sh atm
```

#### Running the Digits Program

```sh
sh run.sh digits
```

#### Running the Knapsack Program

```sh
sh run.sh knapsack
```

### Cleaning Up Compiled Files

To clean up the compiled files (executables and object files), you can use the `clear` command:

```sh
sh run.sh clear
```