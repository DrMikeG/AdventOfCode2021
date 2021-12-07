import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    # Line is just csv
    allNumbersInFile = []
    lineTuple = line.strip().split(",")
    for str in lineTuple:
        allNumbersInFile.append(int(str))

    for num in allNumbersInFile:
        struct.append(num)

    
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

def fuelCost(struct,position):
    cost = 0
    for num in struct:
        steps = abs(num - position)
        fuel = 0
        for i in range(steps+1):
            fuel = fuel + i
        cost = cost + fuel
    return cost

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\07a\\tool_src\\input.txt"
    struct = processInputFile(input_path)

    minPos = min(struct)
    maxPos = max(struct)

    print("Min {} max {} ".format(minPos,maxPos))

    minFuel = -1
    minPos = -1
    for pos in range(minPos,maxPos):
        cost = fuelCost(struct,pos)
        print("Position {} cost {}".format(pos,cost))
        if minFuel == -1 or cost < minFuel:
            minPos = pos
            minFuel = cost

    print("Move crabs to {} at fuel cost {}".format(minPos,minFuel))


if __name__ == "__main__":

    mainTask()