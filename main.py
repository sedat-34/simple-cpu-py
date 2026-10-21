import io

def assemble():

    machinecode = bytearray(256)

    with io.open("main.scp", "r") as f:
        rawcode = f.read()

    codelines = rawcode.splitlines()
    for i in range(len(codelines)):
        codelines[i] = codelines[i].split("!")[0]
    print(codelines)
    codelineindex = 0

    for line in codelines:
        command = line.split()
        for i in range(3):
            if not command[i+1]:
                command[i+1] = 0
        opcode = command[0]

        match opcode:
            case "PRINT":
                machinecode[codelineindex*2] = 0x0 << 4 | int(command[1], 16)
                machinecode[codelineindex*2 + 1] = int(command[2], 16) << 4 | int(command[3], 16)

            case "HALT":
                machinecode[codelineindex*2] = 0xF0
                machinecode[codelineindex*2 + 1] = 0x00
        codelineindex += 1

    
    return machinecode

memory = assemble() #Assemble given scp (simple-cpu-py) program into custom hexadecimal format and load to memory

cpuregister = [None] * 16 #Init cpu registers R0-RF
programcounter = 0X00 #Init pc from beginning of memory
loadedhex = (0XF000) #Placeholder halt command
halted = False

opcodes = [None] * 16 #Initialise opcodes list.

def load_byte_register(R, B):
    cpuregister[R] = B
    
def load_cell_register(R, C):
    cpuregister[R] = memory[C]
    
def store_register_cell(R, C):
    memory[C] = cpuregister[R]

def add_bin(R, S, T):
    cpuregister[R] = (cpuregister[S] + cpuregister[T]) & 0XFF

def and_bin(R, S, T):
    cpuregister[R] = cpuregister[S] & cpuregister[T] & 0XFF

def shift_bin(R, S, N):
    if S == 0:
        cpuregister[R] = cpuregister[R] >> N
    elif S == 1:
        cpuregister[R] = (cpuregister[R] << N) & 0XFF

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
opcodes[0X5] = lambda R, S, T: ( #AND RS and RT, store in RR.
    and_bin(R, S, T)
)
opcodes[0X6] = lambda R, S, N: ( #Shift RR's contents N*sign times. S == 0, shift right; S==1, shift left.
    shift_bin(R, S, N)

)
opcodes[0XF] = lambda nib1, nib2, nib3: globals().update({'halted': True})

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
    programcounter = (programcounter + 0X02) #& 0XFF #Prevent overflow, loop to beginning.