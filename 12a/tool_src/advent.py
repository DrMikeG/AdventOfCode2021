import os
from time import perf_counter

def processLineOfInputIntoStruct(line,struct):
    # each line is key-key
    ab = line.strip().split("-",2)
    struct.append(ab)
    
def processInputFile(filePath):
    heights = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,heights)
    else:
        print("File "+filePath+" not found")
    return heights


def setHeight(x,y,heights,z):
    heights[y][x] =z

def getHeight(x,y,heights):
    return heights[y][x]

def isValidPosition(x,y,gridXMax,gridYMax):
    if x < 0: return False
    if y < 0: return False
    if x >= gridXMax: return False
    if y >= gridYMax: return False
    return True

def isLower(midHeight,x,y,gridXMax,gridYMax,heights):
    # If the neighbour is valid and higher, return False
    # else return true
    if isValidPosition(x,y,gridXMax,gridYMax):
        pos = getHeight(x,y,heights)
        if pos >= midHeight:
            return False
    
    return True

def GetValidNeighbours(x,y,gridXMax,gridYMax,heights):
    up   = [x,y-1]
    down = [x,y+1]
    left = [x-1,y]
    right = [x+1,y]

    neighbours = []

    if isValidPosition(up[0],up[1],gridXMax,gridYMax):
        neighbours.append(getHeight(up[0],up[1],heights))
    if isValidPosition(down[0],down[1],gridXMax,gridYMax):
        neighbours.append(getHeight(down[0],down[1],heights))
    if isValidPosition(left[0],left[1],gridXMax,gridYMax):
        neighbours.append(getHeight(left[0],left[1],heights))
    if isValidPosition(right[0],right[1],gridXMax,gridYMax):
        neighbours.append(getHeight(right[0],right[1],heights))

    return neighbours

def incrementNeighbours(gridXMax,gridYMax,heights,pos):
    posX = pos[0]
    posY = pos[1]

    #print("Incrementing neigbours of position {}".format(pos))
    setOff=[]

    for yOff in range(-1,2):
        for xOff in range(-1,2):
            newX = posX + xOff
            newY = posY + yOff
            if (isValidPosition(newX,newY,gridXMax,gridYMax)):
                newEnergy =getHeight(newX,newY,heights) + 1
                setHeight(newX,newY,heights,newEnergy)
                if newEnergy == 10:
                    setOff.append([newX,newY])
                    #print("Neigbour {} of position {} has new energy level of 9 and will flash".format([newX,newY],pos))
    return setOff

def printGrid(gridXMax,gridYMax,heights):
    for xs in heights:
        line = ""
        for ys in xs:
            if ys > 9:
                line = line + '*'
            else:
                line = line + str(ys)
        print(line)    

def printFlashes(gridXMax,gridYMax,flashes):
    for y in range(gridYMax):
        line = ""
        for x in range(gridXMax):
            if [x,y] in flashes:
                line = line + "*"
            else:
                line = line + "."
        print(line)

def increaseAllEnergyBy1AndReportPositionsOver9(gridXMax,gridYMax,heights):
    #print("Increasing energy of all octopus by 1")
    positions = []
    for y in range(gridYMax):
        for x in range(gridXMax):
            newEnergy = getHeight(x,y,heights)+1
            setHeight(x,y,heights,newEnergy)
            if newEnergy > 9:
                positions.append([x,y])
                #print("Octopus {} will now flash".format([x,y]))
    #print("{} flashes to start step".format(len(positions)))
    #printFlashes(gridXMax,gridYMax,positions)
    return positions

def increaseNeighboursOfFlashesEnergyBy1AndAndReportNewPositionsOver9(newFlashes,gridXMax,gridYMax,heights):
    # Everything in firstFlashes has just become 9
    # Don't worry about anything else that was already 9
    # Any neighbours of newFlashes are increased by 1
    # return positions of any number was are increased to 9
    #print("There were {} new flashes, checking their neighbours".format(len(newFlashes)))
    allNew9s = []
    for pos in newFlashes:
        new9s = incrementNeighbours(gridXMax,gridYMax,heights,pos)
        #printGrid(gridXMax,gridYMax,heights)
        for a in new9s:
            allNew9s.append(a)

    return allNew9s

def countAllOver9sAndSetToZero(gridXMax,gridYMax,heights):
    count = 0
    #printGrid(gridXMax,gridYMax,heights)
    for y in range(gridYMax):
        for x in range(gridXMax):
            if getHeight(x,y,heights) > 9:
                count = count + 1
                setHeight(x,y,heights,0)        
    #print("Set {} position to 0".format(count))
    #printGrid(gridXMax,gridYMax,heights)
    return count

def performASingleStep(gridXMax,gridYMax,heights):
    
    firstFlashes = increaseAllEnergyBy1AndReportPositionsOver9(gridXMax,gridYMax,heights)
    #printGrid(gridXMax,gridYMax,heights)

    # Increment neighbours of all values that are now 9
    newFlashes = increaseNeighboursOfFlashesEnergyBy1AndAndReportNewPositionsOver9(firstFlashes,gridXMax,gridYMax,heights)
    #printGrid(gridXMax,gridYMax,heights)

    while len(newFlashes) > 0:
        newFlashes = increaseNeighboursOfFlashesEnergyBy1AndAndReportNewPositionsOver9(newFlashes,gridXMax,gridYMax,heights)

    allFlashesInStep = countAllOver9sAndSetToZero(gridXMax,gridYMax,heights)

    return allFlashesInStep

def isEntireGrid0(heights):
    for ys in heights:
        for xs in ys:
            if xs > 0:
                return False
    return True

def makeMap(pairs):
    keyset = set()
    for ab in pairs:
        keyset.add(ab[0])
        keyset.add(ab[1])
    
    print("all keys {}".format(keyset))
    caveMap = {}
    for k in keyset:
        caveMap[k] = []
        for ab in pairs:
            if ab[0] == k :
                caveMap[k].append(ab[1])
            if ab[1] == k :
                caveMap[k].append(ab[0])
    print("caveMap {}".format(caveMap))
    return caveMap

def allPathsEnd(paths):
    for path in paths:
        if not path[-1] == "end":
            return False
    return True

def addAndDuplicateUnfinishedPaths(paths,caveMap):

    newPaths = []

    nPaths = len(paths)
    for p in range(nPaths):
        path = paths[p]
        pathEnd = path[-1]
        if not pathEnd == "end":       
            if pathEnd in caveMap:     
                nextSteps = caveMap[pathEnd]
                for nextStep in nextSteps:
                    if not nextStep in path or nextStep.isupper():
                        newPath = path.copy()
                        newPath.append(nextStep)
                        newPaths.append(newPath)
        else:
            newPaths.append(path)
    paths.clear()
    paths.extend(newPaths)
    print("Number of paths is {}".format(len(paths)))

def mainTask():
    t1_start = perf_counter()  
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\12a\\tool_src\\input.txt"
    pairs = processInputFile(input_path)
    
    print(pairs)

    caveMap = makeMap(pairs)

    paths = [["start"]]

    while not allPathsEnd(paths):
        addAndDuplicateUnfinishedPaths(paths,caveMap)
        #print(paths)

    print(paths)
    print(len(paths))


    #print(totalFlashes)
    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()