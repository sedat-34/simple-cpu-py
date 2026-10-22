import io
import sys

def assemble():

    def hex_strip(H): #Strips the leading char from RX, CYZ, etc. and return as integer.
        return int(H[1:], 16) 

    machinecode = bytearray(256) #Initialise empty machine code.

    with io.open("main.scp", "r") as f: #Open script to interpret.
        rawcode = f.read()

    codelines = rawcode.splitlines()
    for i in range(len(codelines)):
        codelines[i] = codelines[i].split("!")[0] #Remove comments, split all commands before an !.
    codelineindex = 0 #Used when loading LOC into the binary
    lineindex = 1 #Tracks the current line in the file in case assembly halts
    for line in codelines:
        if line:
            command = line.split() #Split a line into list command, which contains a keyword and at most 3 args.
            while len(command) < 4:
                command.append("0")
            opcode = command[0]

            match opcode:
                case "PRINT":
                    machinecode[codelineindex*2] = 0x0 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) << 4 | (int(command[3], 16) & 0xF)

                case "LOADCELL":
                    machinecode[codelineindex*2] = 0x1 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] =  hex_strip(command[2]) & 0XFF

                case "LOADHEX":
                    machinecode[codelineindex*2] = 0x2 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = int(command[2], 16) & 0XFF

                case "STORECELL":
                    machinecode[codelineindex*2] = 0x3 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = hex_strip(command[2]) & 0XFF

                case "ADD":
                    machinecode[codelineindex*2] = 0x4 << 4 | hex_strip(command[1])
                    machinecode[codelineindex*2 + 1] = (hex_strip(command[2]) << 4 | hex_strip(command[3])) & 0XFF

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
                    machinecode[codelineindex*2 + 1] = (hex_strip(command[2]) << 4) & 0XFF

                case "HALT":
                    machinecode[codelineindex*2] = 0xF0
                    machinecode[codelineindex*2 + 1] = 0x00

                case _:
                    detectedcode = ""
                    for i in range(len(command)):
                        detectedcode = detectedcode + f"{command[i]} "
                    print(f"Invalid command at line {lineindex} of source")
                    print(f"The command was detected as {command}")
                    print(f"Please edit your code and try again")
                    print(f"If you think this shouldn't happen, raise an issue.")
                    sys.exit(1)

            codelineindex += 1
        lineindex += 1

    return machinecode