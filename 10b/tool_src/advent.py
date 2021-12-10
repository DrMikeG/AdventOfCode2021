import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

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

def indexOfChar(str):
    if str == "(": return 0
    if str == "[": return 1
    if str == "{": return 2
    if str == "<": return 3
    if str == ")": return 0
    if str == "]": return 1
    if str == "}": return 2
    if str == ">": return 3
    assert(False)
    return -100

def bClosesA(bracketA,bracketB):
    assert(len(bracketA) == 1)
    assert(len(bracketB) == 1)
    if bracketA =='[' and bracketB ==']': return True
    if bracketA =='(' and bracketB ==')': return True
    if bracketA =='{' and bracketB =='}': return True
    if bracketA =='<' and bracketB =='>': return True
    return False

def removeNeighbourPairs(line):
    str3= line.replace("<>","")
    str3= str3.replace("()","")
    str3= str3.replace("{}","")
    str3= str3.replace("[]","")
    return str3

def firstIncorrectClosingOnLine(line):
    for i in line:
        if isClosingBracket(i):
            return i
    assert(False)


def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\10b\\tool_src\\input.txt"
    struct = processInputFile(input_path)

    bracketCount = [0,0,0,0]

    scores = []

    for lineToParse in struct:
        print(lineToParse)

        currentLength = len(lineToParse)
        lineToParse = removeNeighbourPairs(lineToParse)
        newLength = len(lineToParse)
        while(newLength < currentLength):
            currentLength = len(lineToParse)
            lineToParse = removeNeighbourPairs(lineToParse)
            #print(lineToParse)
            newLength = len(lineToParse)

        print("Finished shrinking")
        if isOnlyOpeningBrackets(lineToParse):
            print("Line {} is just incomplete".format(lineToParse))
            lineScore = 0
            for i in lineToParse[::-1]:
                # go backwards
                lineScore = lineScore * 5
                lineScore = lineScore+score(i)
            print("line score {}".format(lineScore))
            scores.append(lineScore)
        
    scores.sort()
    print(scores)
    print( scores[int(len(scores)/2)])

if __name__ == "__main__":

    mainTask()