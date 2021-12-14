import os
from time import perf_counter
import math

def processLineOfInputIntoStruct(line,struct):
    # each line is just a line
    struct.append(line.strip())
    
def processInputFile(filePath):
    lines = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,lines)
    else:
        print("File "+filePath+" not found")
    return lines


def processLinesInToTemplateAndMap(lines,map):
    #first line is template
    template = lines[0]
    print("Starting protein template is {}".format(template))

    for line in lines[2:]:
        a,b = line.replace("->",",").split(",",2)
        map[a.strip()] = b.strip()

    print(map)
    return template

def zeroLetterCounts(map,letterCounts):
    for key in map:
        for c in key:
            letterCounts[c] = 0
        for c in map[key]:
            letterCounts[c] = 0

def recursivelyExpandPairForNSteps(inputPair,map,letterCounts,nSteps):

    if nSteps==0:
        #Count letters of pair and return
        #print("Counting first of final pair [{}]{}".format(inputPair[0],inputPair[1]))
        letterCounts[inputPair[0]] = letterCounts[inputPair[0]] + 1
    else:
        # Do another step of expansion for this pair
        insert = map[inputPair]
        pairLeft = inputPair[0]+insert
        pairRight = insert+inputPair[1]
        recursivelyExpandPairForNSteps(pairLeft,map,letterCounts,nSteps-1)
        recursivelyExpandPairForNSteps(pairRight,map,letterCounts,nSteps-1)

def mainTask():
    t1_start = perf_counter()  
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\14a\\tool_src\\input.txt"
    lines = processInputFile(input_path)

    map = {}    
    template = processLinesInToTemplateAndMap(lines,map)

    letterCounts = {}
    zeroLetterCounts(map,letterCounts)
    print(letterCounts)

    steps = 10
    # for every pair in template
    iMax = len(template)-1
    for i in range(iMax):
        pair = template[i:i+2]
        print("Process pair {}".format(pair))
        recursivelyExpandPairForNSteps(pair,map,letterCounts,steps)

    #recursivelyExpandPairForNSteps("NN",map,letterCounts,steps)
    #recursivelyExpandPairForNSteps("NN",map,letterCounts,steps)
    #recursivelyExpandPairForNSteps("NC",map,letterCounts,steps)
    #recursivelyExpandPairForNSteps("CB",map,letterCounts,steps)
    finalLetterInTemplate = template[-1]
    print("final letter is {}".format(finalLetterInTemplate))
    letterCounts[finalLetterInTemplate] = letterCounts[finalLetterInTemplate] + 1
    print(letterCounts)

    count = 0
    minVal = -1
    minKey = 'A'
    maxVal = -1
    maxKey = 'A'
    for k in letterCounts:
        count = count + letterCounts[k]
        if letterCounts[k] > maxVal or maxVal == -1:
            maxVal = letterCounts[k]
            maxKey = k
        if letterCounts[k] < minVal or minVal == -1:
            minVal = letterCounts[k]
            minKey = k
    print(count)

    print("Most common letter is {} appearing {} times".format(maxKey,maxVal))
    print("Least common letter is {} appearing {} times".format(minKey,minVal))
    print("Answer is {} - {} = {}".format(maxVal,minVal,maxVal-minVal))

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()