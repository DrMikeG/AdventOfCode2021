import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    # Line is just csv
    allNumbersInFile = []
    lineTuple = line.strip().split(",")
    for str in lineTuple:
        allNumbersInFile.append(int(str))

    for i in range(9):
        struct.append(0)

    for i in range(9):
        for num in allNumbersInFile:
            if num == i:
                struct[i] = struct[i] + 1

    
def processInputFile(filePath):
    
    # First line is numbers (comma separated)
    # then boards come every 5 lines
    # 5 x 5 2 digit numbers

    readLines = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,readLines)
    else:
        print("File "+filePath+" not found")

    return readLines

def runFishDay(struct,day):
    #reduce all values in struct by one
    #all values that go negative become 6 and append 8 to struct
    toAdd = 0
    toAdd = struct[0]
    for i in range(8):
        struct[i] = struct[i+1]
    # fishes move back to 6
    struct[6] = struct[6] + toAdd
    # new fishes added at 8
    struct[8] = toAdd
    
    #print("After {} days: {}".format(day,struct))

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\06a\\tool_src\\input.txt"
    struct = processInputFile(input_path)

    for day in range(256):
        print(day,struct)
        runFishDay(struct,day)    

    print(sum(struct))

if __name__ == "__main__":

    mainTask()