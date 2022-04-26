
# list of conditionals

from atexit import register
from dataclasses import replace
from multiprocessing import Condition
import opcode
from pickletools import long1
from posixpath import split
from textwrap import fill
from numpy import byte, int0

from setuptools import Command


ARMInstructions = """
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
SUB AL S R5, R5, 1
BR PL 0xFFFFFD
ADD AL R3, R4, 28
MOVW AL R2, 0x0000
MOVT AL R2, 0x0020
STR AL R2, R3,
MOVW AL R5, 0xC3500
MOVT AL R5, 0xC
SUB AL S R5, R5, 1
BR PL 0xFFFFFD
BR AL 0xFFFFE8
"""

class Assembler():

    def __init__(self,instuctions):
        # self.instructions = instuctions
        self.instructionSet = instuctions
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
            "S": 0b0
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
            'BRa': 0b101,
        }
        self.singleDataTransfer = {
            'LDR': 0b01000001,
            'STR': 0b01000000
        }

        self.movSet = {
            'MOVW': 0b00110000,
            'MOVT': 0b00110100
        }
        

    # def createInstructionSet(self):
    #     for letter in self.instructions:
            
    #         if letter == "\n":
    #             self.instructionSet.append(self.command)
    #             self.command =""
                    
    #         else:
    #             self.command += letter
    #     # print(self.instructionSet)            

    def printInstructions(self):
        for i in self.FinalBinary:
            print("finally Binary")
            print(i)
            print('\n')

    def createBinary(self):
        # self.createInstructionSet()

        for command in self.instructionSet:
            
            if(command == ""):
                print('blank command')
            
            if("MOVW" in command):
                self.MOVW(command)
            if("MOVT" in command):
                self.MOVT(command)
            if("ADD" in command):
                self.dataProcess(command)
            if("LDR"in command):
                self.dataTransfer(command)
            if("STR" in command):
                self.dataTransfer(command)
            if("ORR" in command):
                self.dataProcess(command)
            if("SUB" in command):
                self.dataProcess(command)
            if("BR" in command):
                self.B(command)


            
# methods to compile commands into binary
    def MOVW(self,command):
        con='0000';
        imm4='0000'
        rd='rR'
        imm12 ='0000'

        # convert string into each word
        splitCommands = self.splitCommand(command)
        # print(splitCommands)

        con = self.splitCondition(self.conditionCodes[splitCommands[1]])

        # print(splitCommands[-1])
        # get hex value and assign to either imm4 or imm12
        hexValue = self.hexToBinary(splitCommands[-1],16)
        hexValue =str(hexValue)
        # print(hexValue)
        
        imm4 = hexValue[0:4]
        
        imm12 = hexValue[4:16]
        

        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace(",",""))

        
        
        binaryValue = f'{con} 0011 0000 {imm4} {rd} {imm12}'

        numberValue = int(binaryValue.replace(' ',''),2)
        byt = numberValue.to_bytes(4,'little')
        # print(binaryValue)
        self.FinalBinary.append(byt)
        
    def MOVT(self,command):
        con='0000';
        imm4='0000'
        rd='rR'
        imm12 ='0000'

        # convert string into each word
        splitCommands = self.splitCommand(command)

        con = self.splitCondition(self.conditionCodes[splitCommands[1]])

        # print(splitCommands[-1])
        # get hex value and assign to either imm4 or imm12
        hexValue = self.hexToBinary(splitCommands[-1],16)
        hexValue =str(hexValue)
        
        imm4 = hexValue[0:4]
        
        imm12 = hexValue[4:16]
        

        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace(",",""))

        binaryValue = f'{con} 0011 0100 {imm4} {rd} {imm12}'
        num = int(binaryValue.replace(' ',''),2)
        byt = num.to_bytes(4,'little')

        self.FinalBinary.append(byt)

    def dataProcess(self,command):
        con='0000'
        opCode=self.dataProcessing["ADD"]
        imm4='0000'
        rd='rR'
        rn='rn'
        imm12 ='0000'
        immO='1'
        s=''
        rpoint = 0
        dpoint = 0

        splitCommands = self.splitCommand(command)
        # print(command)

        if("S" in command):
            s ='1'
            rpoint = 4
            dpoint = 3
        else:
            s='0'
            dpoint = 2
            rpoint = 3
        
        con = self.splitCondition(self.conditionCodes[splitCommands[1]])
        
        opCode = self.getOpCode(self.dataProcessing[splitCommands[0]]).zfill(4)
        # print(opCode)

        

        rn = self.getRegisterBinary(splitCommands[rpoint].replace('R',"").replace(",",""))
        # print("RN " +rn)
        rd = self.getRegisterBinary(splitCommands[dpoint].replace('R',"").replace(",",""))
        # print("RD "+rd)

        hexValue = self.hexToBinary(splitCommands[-1],12)
        hexValue =str(hexValue)

        # print(hexValue)
        imm12 = hexValue
        

        binaryValue = f'{con} 00{immO} {opCode} {s} {rn} {rd} {imm12}'
        num = int(binaryValue.replace(' ',''),2)
        byt = num.to_bytes(4,'little')
        # print(binaryValue)
        self.FinalBinary.append(byt)

    def dataTransfer(self,command):
        con = "0000"
        i='0'
        LorS =''
        rn=""
        rd=""
        imm12='0000 0000 0100'
        prePOST = ''

        splitCommands = self.splitCommand(command)
        con = self.splitCondition(self.conditionCodes[splitCommands[1]])

        if("LDR" in command):
            LorS ='1'
            prePOST ='1'
        if("STR" in command):
            LorS = '0'
            prePOST = '0'


        rn = self.getRegisterBinary(splitCommands[3].replace('R',"").replace(",",""))
        # print("RN " +rn)
        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace(",",""))
        # print("RD "+rd)

        binaryValue = f'{con} 01{i}{prePOST} 000{LorS} {rn} {rd} {imm12}'
        num = int(binaryValue.replace(" ", ""),2)
        byt = num.to_bytes(4,'little')
        print(byt)
        self.FinalBinary.append(byt)
    
    def B(self,command):
        con =''
        L = '0'
        imm24 =''

        splitCommands = self.splitCommand(command)
        # print(splitCommands)
        con = self.splitCondition(self.conditionCodes[splitCommands[1]]).zfill(4)

        # print(con)

        imm24 = self.hexToBinary(splitCommands[-1],24)
        # print(imm24) 
        binayrValue = f'{con} 101{L} {imm24}'
        num = int(binayrValue.replace(' ',''),2)
        byt = num.to_bytes(4,'little')
        self.FinalBinary.append(byt)


# helper methods for getting info

    def splitCommand(slef,command):
        commandArray = command.split(" ")
        return commandArray

    def splitCondition(self,binary):
        binaryStr = str(bin(binary))
        binaryStr = binaryStr.split('0b')
        return binaryStr[1]
    
    def hexToBinary(self,hexNum,fillVal):
        # print("hexNum  " + hexNum)
        hexValue =int(hexNum,16)
        # print("hexValue:  " + str(hexValue))
        binaryValue = hex(hexValue).replace('0x',"")
        # print(bin(int(binaryValue,16))[2:16].zfill(16))
        value=bin(int(binaryValue,16))[2:]
        # print(value[0:16].zfill(16))
        return value[0:fillVal].zfill(fillVal)
    
    def getRegisterBinary(self,register):
        regNumber = int(register)
        return bin(regNumber)[2:].zfill(4)

    def getOpCode(self,code):
        binaryStr = bin(code)
        binaryStr = binaryStr.split('0b')
        return binaryStr[1]


def main():
    commands =''''''

    with open('commands.txt','r') as command_file:
        commands = command_file.read().split("\n")
        print(commands)


    assembleBot = Assembler(commands)
    assembleBot.createBinary()
    print(assembleBot.FinalBinary)

    with open("kernel7.img", "wb") as binary_file:
        for command in assembleBot.FinalBinary:
            binary_file.write(command)
    binary_file.close()

main()


