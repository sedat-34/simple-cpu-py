import io

def assemble():

    def register_decode(R):
        return int(R[-1:], 16)

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
                machinecode[codelineindex*2] = 0x0 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = 0x00

            case "LOADCELL":
                machinecode[codelineindex*2] = 0x1 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = int(command[2], 16) << 4 | int(command[3], 16)
            
            case "LOADHEX":
                machinecode[codelineindex*2] = 0x2 << 4 | register_decode(command[1])
                machinecode[codelineindex*2 + 1] = int(command[2], 16) << 4 | int(command[3], 16)

            case "HALT":
                machinecode[codelineindex*2] = 0xF0
                machinecode[codelineindex*2 + 1] = 0x00
        codelineindex += 1

    
    return machinecode