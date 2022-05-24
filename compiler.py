# compiler class 


class Compiler():

    # constructor that takes in data from file and sets up assebly
    def __init__(self, data):
        self.command = data
    
    def createAssebly(self):
        number = int(self.command,16)
        return self.boilerPlate(number-1)
        

    def boilerPlate(self,data):
        hexCode = hex(data)

        myCode = f"""
MOVW AL R13, 0x0
MOVT AL R13, 0x0
MOVW AL R1, {hexCode}
MOVT AL R1, 0x0000
STR AL R1, R13!,
LDR AL R1, R13!,
MOVW AL R4, 0x0000
MOVT AL R4, 0x3F20
ADD AL R2, R4, 0x08
LDR AL R3, R2,
ORR AL R3, R3, 0x000008
STR AL R3, R2,
ADD AL R3, R4, 0x1c
MOVW AL R2, 0x0000
MOVT AL R2, 0x0020
STR AL R2, R3,
MOVW AL R5, 0xC3500
MOVT AL R5, 0xC
STR AL R5, R13!,
BRL AL :Delay
ADD AL R3, R4, 0x28
MOVW AL R2, 0x0000
MOVT AL R2, 0x0020
STR AL R2, R3,
MOVW AL R5, 0xC3500
MOVT AL R5, 0xC
STR AL R5, R13!,
BRL AL :Delay
SUB AL S R1, R1, 1
BR PL 0xFFFFED
MOVW AL R5, 0x0900
MOVT AL R5, 0x3D
BRL AL :Delay
BR AL 0xFFFFDD
:Delay
LDR AL R5, R13!,
SUB AL S R5, R5, 1
BR PL 0xFFFFFD
BX AL R14
        """
        return myCode


    def addition(self,data):
        pass
    
    def subtract(self,data):
        pass


def main():
    
    with open('program.txt','r') as command_file:
        commands = command_file.read()
        # print(commands)

    compileBot = Compiler(commands)
    assembly = compileBot.createAssebly()
    # print(assembleBot.FinalBinary)

    with open("assembly.txt", "w") as binary_file:
        
        binary_file.write(assembly)
    binary_file.close()
main()