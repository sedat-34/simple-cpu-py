# Simple-Cpu-Py

## What is this?
This is a simple emulated 16-bit CPU and assembler running on Python.

Currently, only 7 of the 10 defined opcodes are supported in the assembler.

# Documentation

## Specs

The cpu has 16 registers (R0-RF) and 256 bytes of emulated memory.

## Assembly reference

To comment on any line, write anything after an ! at the end of code on that line

In code, a register of id X is represented as RX (single hex digit)

In code, a cell of id XY is represented as CXY (two hex digits, pad 0 at the beginning if needed)

### PRINT RX

Prints the data in register X to the terminal

### LOADCELL RX CYZ

Loads data from emulated cell YZ in register X

### LOADHEX RX YZ

Loads the hexadecimal YZ in register X

### STORECELL RX CYZ

Stores the data in register X in emulated cell YZ

### ADD RX RY RZ

Adds RY and RZ, stores result in RX. Handles overflow automatically.

### SHIFT

### LOOP: RX RY Z

Initialise a loop that will run Z+1 times (range 0-F)

RX will be used up during the loop to store how many loops remain after the current loop

RY will be used up during the loop to store the auto-detected cell to return to if the loop isn't over.

### ENDLOOP RX RY

Finish the loop definition for the loop that uses RX for the loop iteration and RY for the cell storage.

### HALT

Halt execution.