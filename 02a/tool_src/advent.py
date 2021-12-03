import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    cmdValuePair = line.strip().split(" ",2)
    struct.append(cmdValuePair)
    
def processInputFile(filePath):
    
    struct = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,struct)
    else:
        print("File "+filePath+" not found")
    return struct

def processStruct(struct):
    
    forwardValue = 0
    depth = 0
    for cmd in struct:
        if cmd[0] == "forward":
            #print(cmd[1])
            forwardValue = forwardValue + int(cmd[1])
        if cmd[0] == "up":
            depth = depth - int(cmd[1])
        if cmd[0] == "down":
            depth = depth + int(cmd[1])

    print(forwardValue)
    print(depth)
    print(forwardValue*depth)

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\02a\\tool_src\\input.txt"
    struct = processInputFile(input_path)
    processStruct(struct)
    


if __name__ == "__main__":

    mainTask()