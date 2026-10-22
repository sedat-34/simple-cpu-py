# Simple-Cpu-Py
(c) Sedat Arıtürk 2026 under the MIT License

See [LICENSE](LICENSE) for information.

## What is this?
This is a simple emulated 16-bit CPU and assembler running on Python.

# Documentation

## Specs

The cpu has 16 registers (R0-RF) and 256 bytes of emulated memory.

## Assembly reference

To comment on any line, write anything after an ! at the end of code on that line or start a comment-only line with an !

In code, a register of id X is represented as RX (single hex digit)

In code, a cell of id XY is represented as CXY (two hex digits, pad 0 at the beginning if needed)

### PRINT TX RY (Optional: L)

Prints the data in register Y to the terminal in type X

X = 0 > Hexadecimal

X = 1 > Decimal

X = 2 > Binary

x = 3 > ASCII text

In ASCII type, L is used such that the data starts from the cell stored in RY and moves on for L cells.

L can only be a maximum of 15.

### LOADCELL RX CYZ

Loads data from emulated cell YZ in register X

### LOADHEX RX YZ

Loads the hexadecimal YZ in register X

### STORECELL RX CYZ

Stores the data in register X in emulated cell YZ

### ADD RX RY RZ

Adds RY and RZ, stores result in RX. Handles overflow automatically.

### SHIFT RX S N

Shifts RX' value N times (range 0 - F) in a direction determined by S (0 or 1)

If S is 0, the value will be shifted right. Otherwise, it will be shifted left.

### LOOP: RX RY Z

Initialise a loop that will run Z+1 times (range 0-F)

RX will be used up during the loop to store how many loops remain after the current loop

RY will be used up during the loop to store the auto-detected cell to return to if the loop isn't over.

### ENDLOOP RX RY

Finish the loop definition for the loop that uses RX for the loop iteration and RY for the cell storage.

### HALT

Halt execution.

## Limitations

A script cannot exceed 128 LOC.

# Setup and execution

1) Install python 3.14.7 (minimum tested)
2) Write your assembly code in main.scp
3) run python main.py