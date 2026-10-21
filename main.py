memory = bytearray(256)
cpuregister = [None] * 16 #Init cpu registers R0-RF
programcounter = 0x00 #Init pc from beginning of memory
loadedhex = (0x1000) #Placeholder halt command
halted = False

sum = 0x00 #Initialise custom sum register.
opcodes = [None] * 16 #Initialise opcodes list.

def load_byte_register(R, B):
    cpuregister[R] = B
    
def load_cell_register(R, C):
    cpuregister[R] = memory[C]
    
def store_register_cell(R, C):
    memory[C] = cpuregister[R]

def add_bin(R, S, T):
    sum = cpuregister[S] + cpuregister[T]
    sum = sum & 0xFF
    cpuregister[R] = sum
    sum = 0x00

opcodes[0x0] = lambda X, Y, Z: print(f"{X:X}{Y:X}{Z:X}") #Print XYZ as hex on the terminal.
opcodes[0x1] = lambda R, X, Y: ( #Load the register R with the bit pattern stored in memory cell XY
    cellid := X << 4 | Y,
    load_cell_register(R, cellid),
    )
opcodes[0x2] = lambda R, X, Y: ( #Load the register R with the bit pattern XY
    bitpattern := X << 4 | Y,
    load_byte_register(R, bitpattern),
    )
opcodes[0x3] = lambda R, X, Y: ( #Store the bit pattern found in register R in memory cell XY
    cellid := X << 4 | Y,
    store_register_cell(R, cellid)
    )
opcodes[0x4] = lambda R, S, T: (
    add_bin(R, S, T)
    )
opcodes[0xf] = lambda nib1, nib2, nib3: globals().update({'halted': True})

#Simple example program.
memory[0x00] = 0x11
memory[0x01] = 0x97 #Load R1 with data from cell 0x97
memory[0x02] = 0x31
memory[0x03] = 0x05 #Overwrite cell 0x05 with contents of R1
memory[0x04] = 0x00
memory[0x05] = 0x00 #Print nibbles 2-4 of cells 0x04 and 0x05. Cell 0x05 was overwritten with contents of cell 0x97
memory[0x06] = 0x21
memory[0x07] = 0xff #Load hex 0xff into R1
memory[0x08] = 0x22
memory[0x09] = 0x02 #Load hex 0x02 into R2
memory[0x0a] = 0x43
memory[0x0b] = 0x12 #Add R1 and R2, store in R3
memory[0x0c] = 0x33
memory[0x0d] = 0x0f #Store the contents of R3 in cell 0x0f
memory[0x0e] = 0x00
memory[0x0f] = 0x00 #Print nibbles 2-4 of cells 0x0e and 0x0f. 0x0f was overwritten with the sums of R1 and R2.
memory[0x10] = 0xf0
memory[0x11] = 0x00 #Halt.
memory[0x97] = 0xFB


while not halted:
    #Fetch
    loadedhex = memory[programcounter] << 8 | memory[programcounter + 1]

    #Decode
    activeopcode = opcodes[(loadedhex & 0xf000) >> 12]
    operands = [None] * 4
    for i in range(3):
        operands[i+1] = (loadedhex & (0xf * (16 ** (2-i)))) >> (4 * (2-i))

    #Execute
    activeopcode(operands[1], operands[2], operands[3]) #Pass the 3 hex digits

    #Increment pc
    programcounter = programcounter + 0x02