import os

def processLineOfInputIntoStruct(line,struct):
    struct.append(line.strip())
    
def processInputFile(filePath):
    readlines = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,readlines)
    else:
        print("File "+filePath+" not found")
    return readlines

def score(str):
    assert(len(str)==1)
    if str == "(": return 1
    if str == "[": return 2
    if str == "{": return 3
    if str == "<": return 4
    
    assert(False)
    return -1

def isClosingBracket(str):
    if str == ")": return True
    if str == "]": return True
    if str == "}": return True
    if str == ">": return True
    return False

def isOnlyOpeningBrackets(str):
    for i in str:
        if isClosingBracket(i):
            return False
    return True

def removeNeighbourPairs(line):
    str3= line.replace("<>","")
    str3= str3.replace("()","")
    str3= str3.replace("{}","")
    str3= str3.replace("[]","")
    return str3

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\10b\\tool_src\\input.txt"
    struct = processInputFile(input_path)

    bracketCount = [0,0,0,0]
    scores = []

    for lineToParse in struct:
        print(lineToParse)
        # shrink strings by removing 'empty' pairs of brackets e.g. ()
        currentLength = len(lineToParse)
        lineToParse = removeNeighbourPairs(lineToParse)
        newLength = len(lineToParse)
        # keep trying to shrink string until length doesn't change
        while(newLength < currentLength):
            currentLength = len(lineToParse)
            lineToParse = removeNeighbourPairs(lineToParse)
            newLength = len(lineToParse)
        print("Finished shrinking")
        
        if isOnlyOpeningBrackets(lineToParse):
            print("Line {} is just incomplete".format(lineToParse))
            lineScore = 0
            for i in lineToParse[::-1]:
                lineScore = lineScore * 5
                lineScore = lineScore+score(i)
            scores.append(lineScore)
        
    scores.sort()
    print(scores)
    print( scores[int(len(scores)/2)])

if __name__ == "__main__":
    mainTask()