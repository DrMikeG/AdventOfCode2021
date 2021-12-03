import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    struct.append(line.strip())
    
def processInputFile(filePath):
    
    struct = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,struct)
    else:
        print("File "+filePath+" not found")
    return struct

def filterToAndShortedInputToMostCommonLeadingBit(struct,index):
    
    nChars = len(struct[0])
    print("processing all digits in column "+str(index))
    oneCount = 0
    zeroCount = 0
    keepWithLeadingBit = '1'
    for num in struct:
        if num[index] == '1':
            oneCount = oneCount + 1
        if num[index] == '0':
            zeroCount = zeroCount + 1
    
    if (oneCount >= zeroCount):
        print("Keep numbers with leading digit of 1")
        keepWithLeadingBit = '1'
    else:
        print("Keep numbers with leading digit of 0")
        keepWithLeadingBit = '0'

    newStruct = []
    for num in struct:
        if num[index] == keepWithLeadingBit:
            newStruct.append(num)

    return newStruct

def filterToAndShortedInputToLeastCommonLeadingBit(struct,index):
    
    nChars = len(struct[0])
    print("processing all digits in column "+str(index))
    oneCount = 0
    zeroCount = 0
    keepWithLeadingBit = '1'
    for num in struct:
        if num[index] == '1':
            oneCount = oneCount + 1
        if num[index] == '0':
            zeroCount = zeroCount + 1
    
    if (oneCount >= zeroCount):
        print("Keep numbers with leading digit of 1")
        keepWithLeadingBit = '1'
    else:
        print("Keep numbers with leading digit of 0")
        keepWithLeadingBit = '0'

    newStruct = []
    for num in struct:
        if num[index] != keepWithLeadingBit:
            newStruct.append(num)

    return newStruct


def processStruct(struct):
    
    nChars = len(struct[0])

    countsOfOnes = []
    countsOfZeros = []

    mostCommon = ""
    leastCommon = ""

    for index in range(nChars):
        print("processing all digits in column "+str(index))
        oneCount = 0
        zeroCount = 0
        for num in struct:
            if num[index] == '1':
                oneCount = oneCount + 1
            if num[index] == '0':
                zeroCount = zeroCount + 1
        countsOfOnes.append(oneCount)
        countsOfZeros.append(zeroCount)
        if (oneCount > zeroCount):
            mostCommon = mostCommon + "1"
            leastCommon = leastCommon + "0"
        else:
            mostCommon = mostCommon + "0"
            leastCommon = leastCommon + "1"

    print(countsOfOnes)
    print(countsOfZeros)

    mc = int(mostCommon, 2)
    lc = int(leastCommon, 2)
    print("Most common "+str(mostCommon)+" "+str(mc))
    print("Least common "+str(leastCommon)+" "+str(lc))
    print(mc*lc)
    


def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\03b\\tool_src\\input.txt"
    struct = processInputFile(input_path)
    processStruct(struct)
    
    ogr = 0
    c02 = 0

    newStruct = struct
    index = 0
    while len(newStruct) > 1:
        newStruct = filterToAndShortedInputToMostCommonLeadingBit(newStruct,index)
        print(newStruct)
        index = index + 1
    
    if len(newStruct) == 1:
        ogr = int(newStruct[0],2)
        print(str(ogr))

    newStruct2 = struct
    index2 = 0
    while len(newStruct2) > 1:
        newStruct2 = filterToAndShortedInputToLeastCommonLeadingBit(newStruct2,index2)
        print(newStruct2)
        index2 = index2 + 1
    
    if len(newStruct2) == 1:
        c02 = int(newStruct2[0],2)
        print(str(c02))

    print(str(ogr*c02))


if __name__ == "__main__":

    mainTask()