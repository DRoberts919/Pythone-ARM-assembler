
# list of conditionals
from mimetypes import common_types


ARMInstructions = """
mov r1, 0
loop:
ldrb r2, [a1], 1
cmp r2, 0
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