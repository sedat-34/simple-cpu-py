import io

def assemble():

    def hex_strip(H): #Strips the leading char from RX, CYZ, etc. and return as integer.
        return int(H[1:], 16)

    machinecode = bytearray(256) #Initialise empty machine code.

    with io.open("main.scp", "r") as f: #Open script to interpret.
        rawcode = f.read()

    codelines = rawcode.splitlines()
    for i in range(len(codelines)):
        codelines[i] = codelines[i].split("!")[0] #Remove comments, split all commands before an !.
    codelineindex = 0

    for line in codelines:
        if line:
            command = line.split() #Split a line into list command, which contains a keyword and at most 3 args.
            while len(command) < 4:
                command.append("0")
            opcode = command[0]

            match opcode:
                case "PRINT":
                    machinecode[codelineindex*2] = 0x0 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4

                case "LOADCELL":
                    machinecode[codelineindex*2] = 0x1 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] =  hex_strip(command[2])

                case "LOADHEX":
                    machinecode[codelineindex*2] = 0x2 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = int(command[2], 16)

                case "STORECELL":
                    machinecode[codelineindex*2] = 0x3 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2])

                case "ADD":
                    machinecode[codelineindex*2] = 0x4 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4 | hex_strip(command[3])

                case "SHIFT":
                    machinecode[codelineindex*2] = 0x5 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = int(command[2], 16) << 4 | int(command[3], 16)

                case "AND":
                    machinecode[codelineindex*2] = 0x6 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4 | hex_strip(command[3])

                case "LOOP:":
                    machinecode[codelineindex*2] = 0xd << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4 | int(command[3], 16)

                case "ENDLOOP":
                    machinecode[codelineindex*2] = 0xe << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4

                case "HALT":
                    machinecode[codelineindex*2] = 0xF0
                    machinecode[codelineindex*2 + 1] = 0x00

            codelineindex += 1

    return machinecode