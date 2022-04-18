
# list of conditionals
from mimetypes import common_types


ARMInstructions = """
MOVW R4, 0
MOVT R4, 0x3F20
ADD R2, R4, 0x08
LDR R3,(R2)
ORR R3, R3, 0x00000008
STR R3, (R2)
ADD R3, R4, 0x1c
MOVW R2, 0x0000
MOVT R2, 0x0020
STR R2, (R3)
MOVW R5, 0xC3500
MOVT r5, 0xC
SUBS R5, R5, 1
(addBranch Command)
ADD R3, R4, 28
MOVW R2, 0x0000
MOVT R2, 0x0020
STR R2, (R3)
MOVW R5, 0xC3500
MOVT R5,0xC
SUBS R5, R5, 1
(add branch to go back 3)
(add branch to go back 24)
"""

class Assembler():

    def __init__(self,instuctions):
        self.instructions = instuctions
        self.instructionSet = []
        self.command = ""
        self.binary = ""

    def createInstructionSet(self):
        for letter in self.instructions:
            
            if letter == "\n":
                self.instructionSet.append(self.command)
                self.command =""
                    
            else:
                self.command += letter
        print(self.instructionSet)            
                    

    def printInstructions(self):
        for i in self.instructions:
            print(i)

    def createBinary(self):
        pass




assembleBot = Assembler(ARMInstructions)

assembleBot.createInstructionSet()