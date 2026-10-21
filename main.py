memory = bytearray(256)
programcounter = 0x00
loadedhex = (0x1000)
halted = False

opcodes = [None] * 16

opcodes[0x0] = lambda hex1, hex2, hex3: print(f"{hex1:x}{hex2:x}{hex3:x}")
opcodes[0x1] = lambda hex1, hex2, hex3: globals().update({'halted': True})

memory[0x00] = 0x00
memory[0x01] = 0xaf
memory[0x02] = 0x10
memory[0x03] = 0x00

while not halted:
    #Fetch
    loadedhex = memory[programcounter] << 8 | memory[programcounter + 1]

    #Decode
    loadedhexstr = f"{loadedhex:04x}"
    activeopcode = opcodes[int(loadedhexstr[0], 16)]
    operands = [None] * 4
    for i in range(3):
        operands[i+1] = int(loadedhexstr[i+1], 16)

    #Execute
    activeopcode(operands[1], operands[2], operands[3]) #Pass the 3 hex digits

    #Increment pc
    programcounter = programcounter + 0x02
