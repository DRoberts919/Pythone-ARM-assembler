# compiler class 


class Compiler():

    # constructor that takes in data from file and sets up assebly
    def __init__(self, data):
        self.command = data
    
    def createAssebly(self):
        
        pass

    def boilerPlate(self,data):
        code = """
        MOVW AL R13, 0x0
        MOVT AL R13, 0x0
        
        #put gpio pin in write mode ------------------------
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
        #-----------------------------------------------------

        STM AL R13!, 1-12
        MOVW AL R5, 0xA3C0
        MOVT AL R5, 0x9B
        STR AL R5, R13!, 
        BRL AL :timer
        LDM AL R13!, 1-12

        # turn off code -------
        ADD AL R3, R4, 0x28
        MOVW AL R2, 0x0000
        MOVT AL R2, 0x0020
        STR AL R2, R3,
        STM AL R13!, 1-12
        MOVW AL R5, 0xC3500
        MOVT AL R5, 0xC
        ------------------------

        STR AL R5, R13!, 
        BRL AL :timer
        LDM AL R13!, 1-12
        BR AL 0xFFFFE2
        :timer
        LDR AL R5, R13!,
        SUB AL S R5, R5, 1
        BR PL 0xFFFFFD
        BX AL R14
        """

        myCode = """
        MOVW AL R13, 0x0
        MOVT AL R13, 0x0
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
        MOVW AL R1, 0x0007
        MOVT AL R1, 0x0000
        STR AL R1, R13!,
        BL :Delay



        :Delay
        LDR AL R5, R13!,
        SUB AL S R5, R5, 1
        BR PL 0xFFFFFD
        BX AL R14
        """
        return code


def main():
    

    with open('program.txt','r') as command_file:
        commands = command_file.read()
        # print(commands)

    compileBot = Compiler(commands)
    assembly = compileBot.createAssebly()
    # print(assembleBot.FinalBinary)

    with open("kernel7.img", "wb") as binary_file:
        
        binary_file.write(assembly)
    binary_file.close()
main()