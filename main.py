memory = bytearray(256)
cpuregister = [None] * 16 #Init cpu registers R0-RF
programcounter = 0X00 #Init pc from beginning of memory
loadedhex = (0X1000) #Placeholder halt command
halted = False

sum = 0X00 #Initialise custom sum register.
opcodes = [None] * 16 #Initialise opcodes list.

def load_byte_register(R, B):
    cpuregister[R] = B
    
def load_cell_register(R, C):
    cpuregister[R] = memory[C]
    
def store_register_cell(R, C):
    memory[C] = cpuregister[R]

def add_bin(R, S, T):
    sum = cpuregister[S] + cpuregister[T]
    sum = sum & 0XFF
    cpuregister[R] = sum
    sum = 0X00

def and_bin(R, S, T):
    cpuregister[R] = cpuregister[S] & cpuregister[T] & 0XFF

opcodes[0X0] = lambda X, Y, Z: print(f"{X:X}{Y:X}{Z:X}") #Print XYZ as hex on the terminal.
opcodes[0X1] = lambda R, X, Y: ( #LOAD the register R with the bit pattern stored in memory cell XY
    cellid := X << 4 | Y,
    load_cell_register(R, cellid),
    )
opcodes[0X2] = lambda R, X, Y: ( #LOAD the register R with the bit pattern XY
    bitpattern := X << 4 | Y,
    load_byte_register(R, bitpattern),
    )
opcodes[0X3] = lambda R, X, Y: ( #STORE the bit pattern found in register R in memory cell XY
    cellid := X << 4 | Y,
    store_register_cell(R, cellid)
    )
opcodes[0X4] = lambda R, S, T: ( #ADD RS and RT, store in RR. Handles overflow.
    add_bin(R, S, T)
    )
opcodes[0X05] = lambda R, S, T: ( #AND RS and RT, store in RR.
    and_bin(R, S, T)

)
opcodes[0XF] = lambda nib1, nib2, nib3: globals().update({'halted': True})

#Simple example program.
memory[0X00] = 0X11
memory[0X01] = 0X97 #Load R1 with data from cell 0X97
memory[0X02] = 0X31
memory[0X03] = 0X05 #Overwrite cell 0X05 with contents of R1
memory[0X04] = 0X00
memory[0X05] = 0X00 #Print nibbles 2-4 of cells 0X04 and 0X05. Cell 0X05 was overwritten with contents of cell 0X97
memory[0X06] = 0X21
memory[0X07] = 0XFF #Load hex 0XFF into R1
memory[0X08] = 0X22
memory[0X09] = 0X02 #Load hex 0X02 into R2
memory[0X0A] = 0X43
memory[0X0B] = 0X12 #Add R1 and R2, store in R3
memory[0X0C] = 0X33
memory[0X0D] = 0X0f #Store the contents of R3 in cell 0X0F
memory[0X0E] = 0X00
memory[0X0F] = 0X00 #Print nibbles 2-4 of cells 0X0E and 0X0F. 0X0F was overwritten with the sums of R1 and R2.
memory[0x10] = 0X21
memory[0x11] = 0x01 #Load hex 01 into R1
memory[0x12] = 0X22
memory[0x13] = 0x03 #Load hex 01 into R2
memory[0x14] = 0X53
memory[0x15] = 0x12 #Store "R1 AND R2" in R3
memory[0x16] = 0x33
memory[0x17] = 0x19 #Load R3 in cell 0x19
memory[0x18] = 0x00
memory[0x19] = 0x00 #Print nibbles 2-4. 0x19 was overwritten with "R1 AND R2"
memory[0X1A] = 0XF0
memory[0X1B] = 0X00 #Halt.
memory[0X97] = 0XFB


while not halted:
    #Fetch
    loadedhex = memory[programcounter] << 8 | memory[programcounter + 1]

    #Decode
    activeopcode = opcodes[(loadedhex & 0Xf000) >> 12]
    operands = [None] * 4
    for i in range(3):
        operands[i+1] = (loadedhex & (0Xf * (16 ** (2-i)))) >> (4 * (2-i))

    #Execute
    activeopcode(operands[1], operands[2], operands[3]) #Pass the 3 hex digits

    #Increment pc
    programcounter = programcounter + 0X02