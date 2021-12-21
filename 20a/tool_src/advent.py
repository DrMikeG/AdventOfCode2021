import os
from time import perf_counter
import math

from collections import defaultdict
import heapq as heap

def processLineOfInputIntoStruct(line,struct):
    # each line is lots of single digit numbers
    if len(line.strip()) > 0:
        row = []
        for d in line.strip():
            if d == '#':
                row.append(1)
            else:
                row.append(0)
        struct.append(row)
    
def getAlgorithm(line,algorithm):
    assert(len(algorithm) == 0)
    for i in line.strip():
        if i == '#':
            algorithm.append(1)
        else:
            algorithm.append(0)

def processInputFile(filePath):
    heights = []
    algorithm = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            if len(algorithm) == 0:
                getAlgorithm(x,algorithm)
            else:
                processLineOfInputIntoStruct(x,heights)
    else:
        print("File "+filePath+" not found")
    return algorithm,heights


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

def nextStepIsUniqueOrFirstDuplicate(nextStep,path):
    
    # This wouldn't be a duplicate anyway
    if not nextStep in path:
        return True

    # Check if this is the first duplicate
    allLowerList = []
    allLowerSet = set()
    for p in path:
        if p.islower() :#and not p == 'start':
            allLowerList.append(p)
            allLowerSet.add(p)

    noDuplicates = len(allLowerList) == len(allLowerSet)
    if noDuplicates:
        return True

    return False

def isValidNextStep(path,nextStep):
    if nextStep == "start":
        return False
    if nextStep == "end":
        return True
    if nextStep.isupper():        
        return True
    if nextStep.islower() and nextStepIsUniqueOrFirstDuplicate(nextStep,path):
        return True
    else:
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
                    if isValidNextStep(path,nextStep):
                        newPath = path.copy()
                        newPath.append(nextStep)
                        newPaths.append(newPath)
        else:
            newPaths.append(path)
    paths.clear()
    paths.extend(newPaths)
    print("Number of paths is {}".format(len(paths)))

def printPaths(paths):
    strs = set()
    for p in paths:
        _str = ""
        for s in p:
            _str = _str + str(s) +","
        strs.add(_str)
    for p in strs:
        print(p)

def foldInX(gridXMax,gridYMax,coords,foldLine):
    print("Fold horizontally up at {}".format(foldLine))
    # Horizontal fold (but not neccerssarily in the middle)
    # Foldline-1 becomes new bottom
    # Your distance below the fold-line becomes you distance above
    
    # Are there any dots on the foldline?
    for coord in coords:
        assert( not coord[1] == foldLine)

    newCoords =[]
    for coord in coords:
        if coord[1] > foldLine:
            distanceFromFold = (coord[1]-foldLine)
            newCoord = [coord[0],foldLine-distanceFromFold]
            if not newCoord in newCoords:
                newCoords.append(newCoord)
        else:
            if not coord in newCoords:
                newCoords.append(coord)

    newGridYMax = foldLine
    print("Grid size changes from {} x {} to {} x {}".format(gridXMax,gridYMax,gridXMax,newGridYMax))
    return gridXMax,newGridYMax,newCoords

def foldInY(gridXMax,gridYMax,coords,foldLine):
    print("Fold vertically left at {}".format(foldLine))
    # Horizontal fold
    # Distance from right becomes distance from top

    for coord in coords:
        assert( not coord[0] == foldLine)

    newCoords =[]
    for coord in coords:
        if coord[0] > foldLine:
            distanceFromFold = (coord[0]-foldLine)
            newCoord = [foldLine-distanceFromFold,coord[1]]
            if not newCoord in newCoords:
                newCoords.append(newCoord)
        else:
            if not coord in newCoords:
                newCoords.append(coord)

    newGridXMax = foldLine
    print("Grid size changes from {} x {} to {} x {}".format(gridXMax,gridYMax,newGridXMax,gridYMax))

    return newGridXMax,gridYMax,newCoords


def printGrid(graph):
    gridXMax=len(graph[0])
    gridYMax=len(graph)
    print("Printing grid {} x {}".format(gridXMax,gridYMax))
    for y in range(gridYMax):
        line = ""
        for x in range(gridXMax):
            h = getHeight(x,y,graph)
            if h == 0:
                line=line +'.'
            elif h == 1:
                line=line +'#'
        print(line)    

def gridNeighbours(gridXMax,gridYMax,graph, node):
    # The neighbours of this node are up-down-left-right (when valid)
    # the weight is the entry cost from graph
    nodeX = node[0]
    nodeY = node[1]
    neighbours = []
    # Up
    if isValidPosition(nodeX,nodeY-1,gridXMax,gridYMax):
        weight = getHeight(nodeX,nodeY-1,graph)
        neighbours.append(((nodeX,nodeY-1),weight))
    # Down
    if isValidPosition(nodeX,nodeY+1,gridXMax,gridYMax):
        weight = getHeight(nodeX,nodeY+1,graph)
        neighbours.append(((nodeX,nodeY+1),weight))
    # Left
    if isValidPosition(nodeX-1,nodeY,gridXMax,gridYMax):
        weight = getHeight(nodeX-1,nodeY,graph)
        neighbours.append(((nodeX-1,nodeY),weight))
    # Right
    if isValidPosition(nodeX+1,nodeY,gridXMax,gridYMax):
        weight = getHeight(nodeX+1,nodeY,graph)
        neighbours.append(((nodeX+1,nodeY),weight))

    return neighbours

def makeNewGrid(oldGrid,gridXMax,gridYMax,algorithm,zeroValue):
    newGrid = []
    for y in range(-1,gridYMax+1):
        outputRow = []
        for x in range(-1,gridXMax+1):
            # consider pixels
            #print("Calculating output pixel ({},{})".format(x,y))
            binaryStr = ""
            for y_off in range(-1,2):
                for x_off in range(-1,2):
                    xa = x+x_off
                    ya = y+y_off
                    
                    if isValidPosition(xa,ya,gridXMax,gridYMax):
                        h = getHeight(xa,ya,oldGrid)
                        #print("Original grid pixel ({},{}) is {}".format(xa,ya,h))
                    else:
                        #print("Original grid pixel ({},{}) is out of range so using 0".format(xa,ya))
                        h = zeroValue
                    binaryStr += str(h)
            assert(len(binaryStr) == 9)        
            val = int(binaryStr,2)
            outputPixel = algorithm[val]
            #print("binary string {} has value {} index into algorithm as {}".format(binaryStr,val,algorithm[val]))
            outputRow.append(outputPixel)
        assert(len(outputRow) == gridXMax+2)
        newGrid.append(outputRow)

    return newGrid

def countList(grid):
    countList =0
    for line in grid:
        for d in line:
            if d == 1:
                countList = countList + 1
    return countList

def mainTask():
    t1_start = perf_counter()  
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\20a\\tool_src\\input.txt"
    algorithm,grid = processInputFile(input_path)
        
    print("Algorithm length = {}".format(len(algorithm)))

    for i in range(2):
        gridXMax=len(grid[0])
        gridYMax=len(grid)
        #printGrid(grid)
        grid = makeNewGrid(grid,gridXMax,gridYMax,algorithm,(i % 2))
        printGrid(grid)
        print("Lit in output image {}".format(countList(grid)))

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()