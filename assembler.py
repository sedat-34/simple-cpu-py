import io

def assemble():

    def register_decode(R): #R0 - R15 become integers 0X0-0XF
        return int(R[-1:], 16)

    machinecode = bytearray(256) #Initialise empty machine code.

    with io.open("main.scp", "r") as f: #Open script to interpret.
        rawcode = f.read()

    codelines = rawcode.splitlines()
    for i in range(len(codelines)):
        codelines[i] = codelines[i].split("!")[0] #Remove comments, split all commands before an !.
    print(codelines) #Print the full code with no comments.
    codelineindex = 0

    for line in codelines:
        command = line.split() #Split a line into list command, which contains a keyword and at most 3 args.
        while len(command) < 4:
            command.append("0")
        opcode = command[0]

        match opcode:
            case "PRINT":
                machinecode[codelineindex*2] = 0x0 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = 0x00

            case "LOADCELL":
                machinecode[codelineindex*2] = 0x1 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = int(command[2], 16)

            case "LOADHEX":
                machinecode[codelineindex*2] = 0x2 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = int(command[2], 16)

            case "STORECELL":
                machinecode[codelineindex*2] = 0x3 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = int(command[2], 16)

            case "LOOP:":
                machinecode[codelineindex*2] = 0x7 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = register_decode(command[2]) << 4 | int(command[3], 16)

            case "ENDLOOP":
                machinecode[codelineindex*2] = 0x8 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = register_decode(command[2]) << 4

            case "HALT":
                machinecode[codelineindex*2] = 0xF0
                machinecode[codelineindex*2 + 1] = 0x00

        codelineindex += 1

    return machinecode