import os
from time import perf_counter, process_time
import math


class SnailFishNumber:

    def __init__(self,parent = None, inputString = None):

        self.depth = 0
        if not parent == None:
            self.parent = parent
            self.depth  = parent.depth + 1

        self.leftPair = None
        self.leftNumber = -1
        self.leftIsPair = True
        
        self.rightPair = None
        self.rightNumber = -1
        self.rightIsPair = True

        if not inputString is None:
            assert(len(inputString) > 0)
            left,right = SnailFishNumber.splitString(inputString)

            if ',' in left:
                self.leftPair = SnailFishNumber(self,left)
                self.leftIsPair = True                
            else:
                self.leftNumber = int(left)
                self.leftIsPair = False

            if ',' in right:
                self.rightPair = SnailFishNumber(self,right)
                self.rightIsPair = True                
            else:
                self.rightNumber = int(right)
                self.rightIsPair = False

    def toString(self):
        left = ""
        if self.leftIsPair:
            left = self.leftPair.toString()
        else:
            left = str(self.leftNumber)
        right = ""
        if self.rightIsPair:
            right = self.rightPair.toString()
        else:
            right = str(self.rightNumber)
        return "["+left+","+right+"]"

    def magnitude(self):
        # 3.m(a)+2.m(b)
        a = 0
        if self.leftIsPair:
            a = self.leftPair.magnitude()
        else:
            a = self.leftNumber
        b = 0
        if self.rightIsPair:
            b = self.rightPair.magnitude()
        else:
            b = self.rightNumber
        return (3*a) + (2*b)


    def splitString(inputString):
        # move from start to pair the brackets until you reach a , at the top level
        # split the string at that index...
        openBracketCount = 0
        left = ""
        right = ""
        for i in range(len(inputString)):
            if inputString[i] == '[':
                openBracketCount += 1
            if inputString[i] == ']':
                openBracketCount -= 1
            if inputString[i] == ',' and openBracketCount == 1:
                left = inputString[1:i]
                right = inputString[i+1:-1]
                break
        assert(len(left) > 0)
        assert(len(right) > 0)
        return left,right        


class Packet:

    def __init__(self,inputBitStream,startingIndex,depth):
        
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
        self.depth = depth

        print("Stream position {} started new packet version {} typeID {} depth {}".format(startingIndex,self.packetVersion,self.typeID,depth))

        if self.typeID == 4:
            #Literal value packets encode a single binary number
            self.subPackets = []
            self.number=-1
            self.eatLiteralFromStream(inputBitStream,ptIDBEnd)
            print("Literal value {} - at depth {} uses up to bit {}".format(self.number,self.depth,self.endPosInBitStream))
        
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
                self.endPosInBitStream = self.eatNSubPackets(inputBitStream,ptIDBEnd+12,nSubpackets,depth+1)
            else:
                assert(self.lengthType == 15)
                nSubPacketLengthString = inputBitStream[ptIDBEnd+1:ptIDBEnd+16]
                assert(len(nSubPacketLengthString) == 15)
                nSubpacketLength = int(nSubPacketLengthString,2)
                subpacketRegionStart = ptIDBEnd+16
                subpacketRegionEnd = (subpacketRegionStart+nSubpacketLength)-1 # length includes the first character
                print("Unknown number of subpackets to be read, using {} bits from {} to {}".format(nSubpacketLength,subpacketRegionStart,subpacketRegionEnd))
                self.endPosInBitStream = self.eatSubPacketsForNBits(inputBitStream,ptIDBEnd+16,nSubpacketLength,depth+1)
                assert(self.endPosInBitStream == subpacketRegionEnd)

    def eatSubPacketsForNBits(self,inputBitStream,startingIndex,nBits,depth):
        # Don't know how many subpackets there will be, but process next one until we has consumed enough bits...
        index = startingIndex
        while (index-startingIndex) < nBits:
            p = Packet(inputBitStream,index,depth)
            index = p.getLastUsedBitIndex() + 1 # move on one bit for start of next packet...
            self.subPackets.append(p)
        return index-1 # -1 because we are reporting characters used.. (ie. p.getLastUsedBitIndex() )

    def eatNSubPackets(self,inputBitStream,startingIndex,nSubpackets,depth):
        index = startingIndex
        for s in range(nSubpackets):
            p = Packet(inputBitStream,index,depth)
            index = p.getLastUsedBitIndex() + 1 # advance by one
            self.subPackets.append(p)
        return index - 1 # report chars used, not next position

    def eatLiteralFromStream(self,inputBitStream,startingIndex):
        self.number=-1
        self.endPosInBitStream = -1
        index = startingIndex
        literalBitString = ""
        # This is the only bit not tested in any of my test cases!
        # Count forward groups of 5 bits until lead bit is a 0

        # Trying to get string out of bytes,

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
    
    def evaluate(self):
        evalSub =[]
        evalSub.extend(map(lambda x: x.evaluate(),self.subPackets))
        if self.typeID == 0:
            #Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
            return sum(evalSub)
        elif self.typeID == 1:
            #Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
            product = 0
            if len(evalSub) > 0:
                product = 1
            for i in evalSub:
                product = product * i
            return product
        elif self.typeID == 2:
            #Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
            return min(evalSub)
        elif self.typeID == 3:
            #Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
            return max(evalSub)                
        elif self.typeID == 4:
            # literal
            return self.number
        elif self.typeID == 5:
            #Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0.
            # These packets always have exactly two sub-packets
            assert(len(evalSub)==2)
            if evalSub[0] > evalSub[1]: 
                return 1
            else:
                return 0
        elif self.typeID == 6:
            # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. 
            # These packets always have exactly two sub-packets.
            assert(len(evalSub)==2)
            if evalSub[0] < evalSub[1]:
                return 1
            else:
                return 0
        elif self.typeID == 7:
            # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0.
            # These packets always have exactly two sub-packets.
            assert(len(evalSub)==2)
            if evalSub[0]== evalSub[1]:
                return 1
            else:
                return 0
        else:
            assert(False)
            return -1

    def toString(self):
        evalSub =[]
        evalSub.extend(map(lambda x: x.toString(),self.subPackets))
        if self.typeID == 0:
            #Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
            sum = "("
            for i in evalSub:
                sum = (sum + i +" + ")
            return sum[:len(sum)-3] + ")"
        elif self.typeID == 1:
            #Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
            product = "("
            for i in evalSub:
                product = (product + i + " * ")
            return product[:len(product) - 3] +")"
        elif self.typeID == 2:
            #Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
            #return "min[".join(map(str,evalSub)) +"]"
            return "min"+str(evalSub).replace("'",'')+""
            #return "1/0"
        elif self.typeID == 3:
            #Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
            return "max"+str(evalSub).replace("'",'')+""
            #return "1/0"
        elif self.typeID == 4:
            # literal
            return str(self.number)
        elif self.typeID == 5:
            #Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0.
            # These packets always have exactly two sub-packets
            return "("+ evalSub[0] +">"+ evalSub[1]+")"
            #return "1/0"
                
        elif self.typeID == 6:
            # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. 
            # These packets always have exactly two sub-packets.
            assert(len(evalSub)==2)
            return "("+ evalSub[0] +"<"+ evalSub[1]+")"
            #return "1/0"

        elif self.typeID == 7:
            # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0.
            # These packets always have exactly two sub-packets.
            assert(len(evalSub)==2)
            return "("+ evalSub[0] +"=="+ evalSub[1]+")"
            #return "1/0"
        else:
            assert(False)
            return ""

            

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
    packets.append(Packet(bitString,processed,0))
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
        
    assert(len(packets) == 1)
    versionSum = packets[0].sumVersion()
    print("Version sum is {}".format(versionSum))

    toString = packets[0].toString()
    print("Packet eval is {}".format(toString))

    answer = packets[0].evaluate()
    print("Evaluated answer is {}".format(answer))

    return answer

def mainTask():
    t1_start = perf_counter()  
    
    #assert(GetPackets(hexStringIntoBitString("D2FE28")) == 2021)
    
    #assert(GetPackets("1101001011111110101111111000101000") == 518117)

    #C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    #assert(GetPackets(hexStringIntoBitString("C200B40A82")) == 3)
    # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    #assert(GetPackets(hexStringIntoBitString("04005AC33890")) == 54)
    # 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    #assert(GetPackets(hexStringIntoBitString("880086C3E88112")) == 7)
    # CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    #assert(GetPackets(hexStringIntoBitString("CE00C43D881120")) == 9)
    # D8005AC2A8F0 produces 1, because 5 is less than 15.
    #assert(GetPackets(hexStringIntoBitString("D8005AC2A8F0")) == 1)
    # F600BC2D8F produces 0, because 5 is not greater than 15.
    #assert(GetPackets(hexStringIntoBitString("F600BC2D8F")) == 0)
    # 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    #assert(GetPackets(hexStringIntoBitString("9C005AC2F8F0")) == 0)
    # 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
    #assert(GetPackets(hexStringIntoBitString("9C0141080250320F1802104A08")) == 1)

    # A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; 
    #assert(GetPackets(hexStringIntoBitString("A0016C880162017C3686B18A3D4780")) == 1)

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\16a\\tool_src\\input.txt"
    bitString = processInputFile(input_path)
    GetPackets(bitString)
    

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()