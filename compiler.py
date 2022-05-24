# compiler class 


class Compiler():

    # constructor that takes in data from file and sets up assebly
    def __init__(self, data):
        self.command = data
    
    def createAssebly(self):
        commands = self.command.split(" ")
        number = int(commands[0],16)
        numberTwo = int(commands[2],16)
        # subRoutine = self.addition()
        label = self.addition().split("\n")

        print(label[1])
        return self.boilerPlate(number-1,numberTwo-1,self.addition(),label[1])
        

    def boilerPlate(self,dataOne,dataTwo,subRoutine,label):
        hexCode1 = hex(dataOne)
        hexCode2 = hex(dataTwo)
        myCode = f"""
MOVW AL R13, 0x0
MOVT AL R13, 0x0
MOVW AL R1, {hexCode1}
MOVT AL R1, 0x0000
STR AL R1, R13!,
MOVW AL R2, {hexCode2}
MOVT AL R2, 0x00000
STR AL R1, R13!,
BRL AL {label}
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
BR PL 0xFFFFD9
BX AL R14
{subRoutine}
        """
        return myCode


    def addition(self):
        command ="""
:OPPERATION
LDR AL R1, R13!,
LDR AL R2, R13!,
ADD AL R1, R2, R1
STR AL R1, R13!
BX AL R14
        """
        return command
    
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