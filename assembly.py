
from distutils.version import LooseVersion
from math import dist
from turtle import distance


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

    def printInstructions(self):
        for i in self.FinalBinary:
            print(i)
            print('\n')

    def createBinary(self):
        # self.createInstructionSet()
        for index, command in enumerate( self.instructionSet):
            
            if(command == "" or command ==' '):
                continue
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
                self.B(command,index)
            if("BX" in command):
                self.branchEx(command)
            if("STM" in command):
                self.blockDataTransfer(command)
            if("LDM" in command):
                self.blockDataTransfer(command)


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
        # get hex value and assign to either imm4 or imm12
        hexValue = self.hexToBinary(splitCommands[-1],16)
        hexValue = str(hexValue)  
        imm4 = hexValue[0:4]       
        imm12 = hexValue[4:16]
        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace(",",""))

        binaryValue = f'{con} 0011 0000 {imm4} {rd} {imm12}'

        byt = self.convertToByteArray(binaryValue)
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
        byt = self.convertToByteArray(binaryValue)

        self.FinalBinary.append(byt)

    def dataProcess(self,command):
        con='0000'
        opCode=self.dataProcessing["ADD"]
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

        rn = self.getRegisterBinary(splitCommands[rpoint].replace('R',"").replace(",",""))
        # print("RN " +rn)
        rd = self.getRegisterBinary(splitCommands[dpoint].replace('R',"").replace(",",""))
        # print("RD "+rd)

        hexValue = self.hexToBinary(splitCommands[-1],12)
        hexValue =str(hexValue)

        # print(hexValue)
        imm12 = hexValue
        

        binaryValue = f'{con} 00{immO} {opCode} {s} {rn} {rd} {imm12}'
        byt = self.convertToByteArray(binaryValue)
        # print(binaryValue)
        self.FinalBinary.append(byt)

    def dataTransfer(self,command):
        con = "0000"
        i='0'
        LorS =''
        rn=""
        rd=""
        imm12='0000 0000 0000'
        prePOST = ''
        writeback=''

        splitCommands = self.splitCommand(command)
        con = self.splitCondition(self.conditionCodes[splitCommands[1]])

        if("LDR" in command):
            LorS ='1'
            prePOST ='1'
        if("STR" in command):
            LorS = '0'
            prePOST = '0'

        print(splitCommands)
        if("!," in splitCommands[3]):
            # sets write back bit
            # print('command has !, postion 3')
            writeback = "1"
            # print(splitCommands[3])
        elif("!," in splitCommands[2]):
            # print('command has !, postion 2')
            writeback ="1"
            # print(splitCommands[2])
        else:
            writeback = "0"
            splitCommands[2].replace('!','')
        
        rn = self.getRegisterBinary(splitCommands[3].replace('R',"").replace('!','').replace(',',''))
        # print("RN " +rn)
        rd = self.getRegisterBinary(splitCommands[2].replace('R',"").replace('!','').replace(",",""))
        # print("RD "+rd)

        binaryValue = f'{con} 01{i}{prePOST} 00{writeback}{LorS} {rn} {rd} {imm12}'
        print(binaryValue)
        byt = self.convertToByteArray(binaryValue)
        
        
        self.FinalBinary.append(byt)
    
    def B(self,command,index):
        con =''
        L = '0'
        imm24 =''

        splitCommands = self.splitCommand(command)
        # print(splitCommands)
        
        if(splitCommands[-1].startswith(':')):
            # print('Label Branch Command')
            # print(index)
            # print(splitCommands[-1])
            imm24 = self.getBranchDistance(splitCommands[-1],index)

        else:
            
            imm24 = self.hexToBinary(splitCommands[-1],24)

        con = self.splitCondition(self.conditionCodes[splitCommands[1]]).zfill(4)
        
        if(splitCommands[0] == "BRL"):
            L = "1"
        else:
            L="0"


        # print(imm24) 
        binaryValue = f'{con} 101{L} {imm24}'
        # print(f'COMMAND: \n{command}')
        # print(f'LBIT \n {L}')
        # print(f'IMM24\n{imm24}')
        
        byt = self.convertToByteArray(binaryValue)
        self.FinalBinary.append(byt)
    
    def branchEx(self,command):

        con ="0000"
        rn = '0000'

        splitCommands = self.splitCommand(command)

        con = self.splitCondition(self.conditionCodes[splitCommands[1]]).zfill(4)

        if( splitCommands[-1] == "LR"):
            # print("register 14 hit")
            rn = self.getRegisterBinary("14")
        else:
            rn = self.getRegisterBinary(splitCommands[-1].replace('R',"").replace(",",""))

        finalyBinary = f'{con} 0001 0010 1111 1111 1111 0001 {rn}'

        byt = self.convertToByteArray(finalyBinary)
        self.FinalBinary.append(byt)

    def blockDataTransfer(self,command):
        splitCommands = self.splitCommand(command)
        con = self.splitCondition(self.conditionCodes[splitCommands[1]]).zfill(4)
        prePost = ''
        LorS =''
        upDown =''
        writeback=''
        registers =''

        if(splitCommands[1] == "STM"):
            prePost = "0"
            upDown='1'
            LorS='0'
            
        if(splitCommands[1] == "LDM"):
            prePost = "1"
            upDown='0'
            LorS ='1'
        
        if(splitCommands[2].endswith('!,')):
            writeback="1"
            # splitCommands[2].replace('!,',"")


        if(splitCommands[-1] == "1-12"):
            registers = '0000111111111111'

        Rn = self.getRegisterBinary(splitCommands[2].replace('R',"").replace("!",""))

        finalyBinary = f'{con} 100{prePost} {upDown}1{writeback}{LorS} {Rn} {registers}'
        byt = self.convertToByteArray(finalyBinary)
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
        hexValue =int(hexNum,16)
        binaryValue = hex(hexValue).replace('0x',"")
        # print(binaryValue)
        value=bin(int(binaryValue,16))[2:]
        return value[0:fillVal].zfill(fillVal)
    
    def getRegisterBinary(self,register):
        regNumber = int(register)
        return bin(regNumber)[2:].zfill(4)

    def getOpCode(self,code):
        binaryStr = bin(code)
        binaryStr = binaryStr.split('0b')
        return binaryStr[1]

    def convertToByteArray(self,code):
        num = int(code.replace(' ',''),2)
        byt = num.to_bytes(4,'little')
        return byt
    
    def getBranchDistance(self,label,index):
        # decrement = 0
        # subRoutine = 0
        # branch = 0
        
        # for i, command in enumerate(self.instructionSet):
        #     if command.startswith(f':{label}') or command == '':
        #         decrement += 1
        #     if command.startswith(label):
        #         subRoutine = (i-decrement) - index

        #         branch = subRoutine - 2
        distance = 0
        branchLabel = index
        labelDistance=0
        for i, command in enumerate(self.instructionSet):
            if(command == label):
                # print("label found")
                labelDistance = i

        distance = (labelDistance - branchLabel) - 2

        distance = bin(distance * -1).replace('0b','').replace('-','').zfill(24)

        # print('\n')
        # print(f'Branch Lable: {branchLabel}')
        # print(f'Label Position: {labelDistance}')
        # print(f'distance {distance}')
        
        return distance
        


def main():
    commands =''''''

    with open('commandsWithStack.txt','r') as command_file:
        commands = command_file.read().split("\n")
        # print(commands)

    assembleBot = Assembler(commands)
    assembleBot.createBinary()
    # print(assembleBot.FinalBinary)

    with open("kernel7.img", "wb") as binary_file:
        for command in assembleBot.FinalBinary:
            binary_file.write(command)
    binary_file.close()
main()


