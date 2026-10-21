memory = bytearray(256)
programcounter = 0x00 #Init pc from beginning of memory
loadedhex = (0x1000) #Placeholder halt command
halted = False

opcodes = [None] * 16

opcodes[0x0] = lambda nib1, nib2, nib3: print(f"{nib1:x}{nib2:x}{nib3:x}")
opcodes[0x1] = lambda nib1, nib2, nib3: globals().update({'halted': True})

#Simple example program, prints 0fb, 011 on the console and halts.
memory[0x00] = 0x00
memory[0x01] = 0xfb
memory[0x02] = 0x00
memory[0x03] = 0x11
memory[0x04] = 0x10
memory[0x05] = 0x00

while not halted:
    #Fetch
    loadedhex = memory[programcounter] << 8 | memory[programcounter + 1]

    #Decode
    loadedhexstr = f"{loadedhex:04x}"
    activeopcode = opcodes[(loadedhex & 0xf000) >> 12]
    operands = [None] * 4
    for i in range(3):
        operands[i+1] = (loadedhex & (0xf * (16 ** (2-i)))) >> (4 * (2-i))

    #Execute
    activeopcode(operands[1], operands[2], operands[3]) #Pass the 3 hex digits

    #Increment pc
    programcounter = programcounter + 0x02