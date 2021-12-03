

import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    #rulePassword = line.split(":",2)
    #ruleLetterMinMax = rulePassword[0].split(" ",2)
    #ruleMinMax = ruleLetterMinMax[0].split("-",2)
    struct.append(line.strip())
    #struct.append((ruleLetterMinMax[1].strip(),int(ruleMinMax[0].strip()),int(ruleMinMax[1].strip()),rulePassword[1].strip()))

def processInputFile(filePath):
    
    struct = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,struct)
    return struct

def processStruct(struct):
    
    
    windowedValues = []
    
    increases = 0
    a = int(struct[0])
    b = int(struct[1])
    for c in struct[2:]:
        d = a+b+int(c)
        print(d)
        windowedValues.append(d)
        a = b
        b = int(c)

    last = windowedValues[0]
    for c in windowedValues:
        if c > last:
            increases = increases+1
        last = c
    print(increases)

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\01b\\tool_src\\input.txt"
    struct = processInputFile(input_path)
    processStruct(struct)
    


if __name__ == "__main__":

    mainTask()