import assembler

memory = assembler.assemble() #Assemble given scp (simple-cpu-py) program into custom hexadecimal format and load to memory

cpuregister = [None] * 16 #Init cpu registers R0-RF
programcounter = 0X00 #Init pc from beginning of memory
loadedhex = (0XF000) #Placeholder halt command

jumped = False #Initialise cpu jump flag
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

def init_loop(R, S, X):
    global cpuregister
    cpuregister[R] = X #Set counter to provided value.
    cpuregister[S] = programcounter + 2 #Cell of the beginning of the loop contents, not the LOOP: statement.

def check_loop(R, S):
    global cpuregister, programcounter, jumped
    if not (cpuregister[R] == 0):
        cpuregister[R] -= 1 #Reduce counter register's value by 1
        programcounter = cpuregister[S] #Set PC to beginning of loop.
        jumped = True


opcodes[0X0] = lambda R, nib2, nib3: print(f"{cpuregister[R]:02X}") #Print Register R's contents as hex on the terminal.
opcodes[0X1] = lambda R, X, Y: ( #LOAD the register R with the bit pattern stored in memory cell XY
    cellid := X << 4 | Y,
    load_cell_register(R, cellid),
    )
opcodes[0X2] = lambda R, X, Y: ( #LOAD the register R with the hex value XY
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
opcodes[0X6] = lambda R, S, N: ( #SHIFT RR's contents N*sign times. S == 0, shift right; S==1, shift left.
    shift_bin(R, S, N)
)
opcodes[0XD] = lambda R, S, X: ( #Initialise a LOOP: with counter at register R with 4-bit hex value X
                                 #Store the loop's starting memory cell at register S.
    init_loop(R, S, X)
)
opcodes[0XE] = lambda R, S, nib3: (# ENDLOOP. Check if register R is zero. if not, JUMP to address stored at register S
    check_loop(R, S)
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
    if jumped:
        jumped = False
    else:
        programcounter = (programcounter + 0X02) #& 0XFF #Prevent overflow, loop to beginning.
