import os
from time import perf_counter, process_time
import math

class Packet:

    def __init__(self,inputBitStream,startingIndex):
        
        #Every packet begins with a standard header: 
        # the first three bits encode the packet version, 
        # and the next three bits encode the packet type ID. 
        pvBStart = startingIndex
        pvBEnd = pvBStart+3
        packetVersionBitString = inputBitStream[pvBStart:pvBEnd]
        ptIDBStart = pvBEnd
        ptIDBEnd = ptIDBStart+3
        packetTypeIDBitString =inputBitStream[ptIDBStart:ptIDBEnd]
        
        self.startIndex = startingIndex
        self.endPosInBitStream = -1
        self.packetVersion = int(packetVersionBitString,2)
        self.typeID  = int(packetTypeIDBitString,2)

        print("Stream position {} started new packet version {} typeID {}".format(startingIndex,self.packetVersion,self.typeID))

        if self.typeID == 4:
            #Literal value packets encode a single binary number
            self.subPackets = []
            self.number=-1
            self.eatLiteralFromStream(inputBitStream,ptIDBEnd)
            print("Literal value {} - end of packet started at {} uses up to bit {}".format(self.number,startingIndex,self.endPosInBitStream))
        
        # Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some calculation on
        # one or more sub-packets contained within.
        # Right now, the specific operations aren't important; focus on parsing the hierarchy of sub-packets.
        else:
            self.number=-1
            self.subPackets = []
            # an operator packet can use one of two modes indicated by the bit immediately after the packet header; this is called the length type ID
            self.lengthType = 15 # If length type is '0' - total length in bits of the sub-packets contained by this packet
            if inputBitStream[ptIDBEnd] == '1':
                self.lengthType = 11 #  the number of sub-packets immediately contained by this packet

            if self.lengthType == 11:
                nSubPacketString = inputBitStream[ptIDBEnd+1:ptIDBEnd+12]
                assert(len(nSubPacketString) == 11)
                nSubpackets = int(nSubPacketString,2)
                print("{} subpackets to read starting from {}".format(nSubpackets,ptIDBEnd+12))
                self.endPosInBitStream = self.eatNSubPackets(inputBitStream,ptIDBEnd+12,nSubpackets)
            else:
                assert(self.lengthType == 15)
                nSubPacketLengthString = inputBitStream[ptIDBEnd+1:ptIDBEnd+16]
                assert(len(nSubPacketLengthString) == 15)
                nSubpacketLength = int(nSubPacketLengthString,2)
                subpacketRegionStart = ptIDBEnd+16
                subpacketRegionEnd = (subpacketRegionStart+nSubpacketLength)-1 # length includes the first character
                print("Unknown number of subpackets to be read, using {} bits from {} to {}".format(nSubpacketLength,subpacketRegionStart,subpacketRegionEnd))
                self.endPosInBitStream = self.eatSubPacketsForNBits(inputBitStream,ptIDBEnd+16,nSubpacketLength)
                assert(self.endPosInBitStream == subpacketRegionEnd)

    def eatSubPacketsForNBits(self,inputBitStream,startingIndex,nBits):
        # Don't know how many subpackets there will be, but process next one until we has consumed enough bits...
        index = startingIndex
        while (index-startingIndex) < nBits:
            p = Packet(inputBitStream,index)
            index = p.getLastUsedBitIndex() + 1 # move on one bit for start of next packet...
            self.subPackets.append(p)
        return index-1 # -1 because we are reporting characters used.. (ie. p.getLastUsedBitIndex() )

    def eatNSubPackets(self,inputBitStream,startingIndex,nSubpackets):
        index = startingIndex
        for s in range(nSubpackets):
            p = Packet(inputBitStream,index)
            index = p.getLastUsedBitIndex() + 1 # advance by one
            self.subPackets.append(p)
        return index - 1 # report chars used, not next position

    def eatLiteralFromStream(self,inputBitStream,startingIndex):
        self.number=-1
        self.endPosInBitStream = -1
        index = startingIndex
        literalBitString = ""
        # Count forward groups of 5 bits until lead bit is a 0
        while inputBitStream[index] == '1':
            literalBitString += inputBitStream[index+1] #ignore leading 0
            literalBitString += inputBitStream[index+2]
            literalBitString += inputBitStream[index+3]
            literalBitString += inputBitStream[index+4]
            index = index + 5
        # Last group
        literalBitString += inputBitStream[index+1] #ignore leading 0
        literalBitString += inputBitStream[index+2]
        literalBitString += inputBitStream[index+3]
        literalBitString += inputBitStream[index+4]
        self.number = int(literalBitString,2)
        self.endPosInBitStream = index+4

    def getLastUsedBitIndex(self):
        #We also talk about how many bit have been used
        if len(self.subPackets) > 0:
            return self.subPackets[-1].getLastUsedBitIndex()
        else:
            return self.endPosInBitStream

    def sumVersion(self):

        sumVer = self.packetVersion
        
        if len(self.subPackets) > 0:
            for i in self.subPackets:
                sumVer = sumVer +i.sumVersion()

        return sumVer

def hexStringIntoBitString(line):
    
    struct=""
    for d in line.strip():
        if d == '0': struct +='0000'
        if d == '1': struct +='0001'
        if d == '2': struct +='0010'
        if d == '3': struct +='0011'
        if d == '4': struct +='0100'
        if d == '5': struct +='0101'
        if d == '6': struct +='0110'
        if d == '7': struct +='0111'
        if d == '8': struct +='1000'
        if d == '9': struct +='1001'
        if d == 'A': struct +='1010'
        if d == 'B': struct +='1011'
        if d == 'C': struct +='1100'
        if d == 'D': struct +='1101'
        if d == 'E': struct +='1110'
        if d == 'F': struct +='1111'

    return struct

def processInputFile(filePath):
    bitStream =""
    heights = ""
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            bitStream = hexStringIntoBitString(x)
    else:
        print("File "+filePath+" not found")
    return bitStream


def EatBits(bitString,packets,processed):

    # Make a new packet
    packets.append(Packet(bitString,processed))
    # This will make a packet with zero or more sub-packets
    # and use up some or all of the bitString
    processed = packets[-1].getLastUsedBitIndex()

    return processed

def GetPackets(bitString):
    print(bitString)
    packets = []

    targetToProcess = len(bitString) # ignore up to 6 final characters
    processed = 0

    while processed < targetToProcess:
        if not '1' in bitString[processed:targetToProcess]:
            print("Not attempt to process tail {}".format(bitString[processed:targetToProcess]))
            break
        processed = EatBits(bitString,packets,processed)
        processed = processed+1 # next char to process
        

    versionSum = sum(map(lambda x: x.sumVersion(),packets))
    print("Version sum is {}".format(versionSum))

    return packets

def mainTask():
    t1_start = perf_counter()  
    
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\16a\\tool_src\\input.txt"
    bitString = processInputFile(input_path)
    GetPackets(bitString)
    
    # literal with number 2021
    #GetPackets(hexStringIntoBitString("D2FE28"))
    
    # operator packet - two subpackets
    #GetPackets(hexStringIntoBitString("38006F45291200"))

    # operator packet - three subpackets
    #GetPackets(hexStringIntoBitString("EE00D40C823060"))

    # represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); 
    # this packet has a version sum of 16.
    #GetPackets(hexStringIntoBitString("8A004A801A8002F478"))

    #620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. 
    # This packet has a version sum of 12.
    #GetPackets(hexStringIntoBitString("620080001611562C8802118E34"))

    #C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID.
    # This packet has a version sum of 23.
    #GetPackets(hexStringIntoBitString("C0015000016115A2E0802F182340"))
    
    #A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; 
    # # it has a version sum of 31.
    #GetPackets(hexStringIntoBitString("A0016C880162017C3686B18A3D4780"))


    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()