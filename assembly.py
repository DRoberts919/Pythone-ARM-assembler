
# list of conditionals

from atexit import register
from dataclasses import replace
from multiprocessing import Condition
import opcode
from pickletools import long1
from posixpath import split
from numpy import int0

from setuptools import Command


ARMInstructions = """
MOVW AL R4, 0x0000
MOVT AL R4, 0x3F20
ADD AL R2, R4, 0x08
LDR AL R3,(R2)
ORR AL R3, R3, 0x00000008
STR AL R3, (R2)
ADD AL R3, R4, 0x1c
MOVW AL R2, 0x0000
MOVT AL R2, 0x0020
STR AL R2, (R3)
MOVW AL R5, 0xC3500
MOVT AL r5, 0xC
SUB S R5, R5, 1
B PL 0xFFFFFD
ADD AL R3, R4, 28
MOVW AL R2, 0x0000
MOVT AL R2, 0x0020
STR AL R2, (R3)
MOVW AL R5, 0xC3500
MOVT AL R5,0xC
SUB S R5, R5, 1
B PL 0xFFFFFD
(add branch to go back 24)
"""

class Assembler():

    def __init__(self,instuctions):
        self.instructions = instuctions
        self.instructionSet = []
        self.command = ""
        self.binary = ""
        self.FinalBinary =[]
        
        self.conditionCodes ={
            "AL": 0b1110,
            "LE": 0b1101,
            "GT": 0b1100,
            "LT": 0b1011,
            "GE": 0b1010,
            "LS": 0b1001,
            "HI": 0b1000,
            "VC": 0b0111,
            "VS": 0b0110,
            "PL": 0b0101,
            "MI": 0b0100,
            "CC": 0b0011,
            "CS": 0b0010,
            "NE": 0b0001,
            "EQ": 0b0000,
        }
        self.dataProcessing = {
            'AND': 0b1000,
            'EOR': 0b0001,
            'SUB': 0b0010,
            'RSB': 0b0011,
            'ADD': 0b0100,
            'ADC': 0b1010,
            'SBC': 0b0110,
            'RSC': 0b0111,
            'TST': 0b1000,
            'TEQ': 0b1001,
            'CMP': 0b1010,
            'CMN': 0b1011,
            'ORR': 0b1100,
            'MOV': 0b1101,
            'BIC': 0b1110,
            'MVN': 0b1111,
            'B': 0b101,
        }
        self.singleDataTransfer = {
            'LDR': 0b01000001,
            'STR': 0b01000000
        }

        self.movSet = {
            'MOVW': 0b00110000,
            'MOVT': 0b00110100
        }
        

    def createInstructionSet(self):
        for letter in self.instructions:
            
            if letter == "\n":
                self.instructionSet.append(self.command)
                self.command =""
                    
            else:
                self.command += letter
        # print(self.instructionSet)            
                    

    def printInstructions(self):
        for i in self.instructions:
            print(i)

    def createBinary(self):
        self.createInstructionSet()

        for command in self.instructionSet:
            
            if(command == ""):
                print('blank command')
            
            if("MOVW" in command):
                self.MOVW(command)
            # if("MOVT" in command):
            #     self.MOVT(command)
            # if("ADD" in command):
            #     self.ADD(command)
            # if("LDR"in command):
            #     self.LDR(command)
            # if("ORR" in command):
            #     self.ORR(command)
            # if("STR" in command):
            #     self.STR(command)
            # if("SUBS" in command):
            #     self.SUBS(command)


            
# methods to compile commands into binary
    def MOVW(self,command):
        con='0000';
        imm4='0000'
        rd='rR'
        imm12 ='0000'

        # convert string into each word
        splitCommands = self.splitCommand(command)
        print(splitCommands)

        con = self.splitCondition(self.conditionCodes[splitCommands[1]])

        # print(splitCommands[-1])
        # get hex value and assign to either imm4 or imm12
        hexValue = self.hexToBinary(splitCommands[-1])
        hexValue =str(hexValue)
        
        imm4 = hexValue[0:4]
        print(imm4)
        imm12 = hexValue[4:16]
        print(imm12)

        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace(",",""))

        
        
        binaryValue = f'{con} 0011 0000 {imm4} {rd} {imm12} \n'
        print(binaryValue)
        


        
    def MOVT(self,command):
        print(command)

    def ADD(self,command):
        print(command)

    def LDR(self,command):
        print(command)
    
    def ORR(self,command):
        print(command)

    def STR(self,command):
        print(command)
    
    def SUBS(self,command):
        print(command)
    
    def B(self,command):
        print(command)


# helper methods for getting info

    def splitCommand(slef,command):
        commandArray = command.split(" ")
        return commandArray

    def splitCondition(self,binary):
        binaryStr = str(bin(binary))
        binaryStr = binaryStr.split('0b')
        return binaryStr[1]
    
    def hexToBinary(self,hexNum):
        # print("hexNum  " + hexNum)
        hexValue =int(hexNum,16)
        # print("hexValue:  " + str(hexValue))
        binaryValue = hex(hexValue).replace('0x',"")
        # print(bin(int(binaryValue,16))[2:16].zfill(16))
        value=bin(int(binaryValue,16))[2:]
        # print(value[0:16].zfill(16))
        return value[0:16].zfill(16)
    
    def getRegisterBinary(self,register):
        
        regNumber = int(register)
        return bin(regNumber)[2:].zfill(4)




assembleBot = Assembler(ARMInstructions)

# assembleBot.createInstructionSet()
assembleBot.createBinary()
