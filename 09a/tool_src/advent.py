import os
from time import perf_counter

def processLineOfInputIntoStruct(line,struct):
    # Line is 10 space separated signals 
    # followed by pipe
    # followed by 4 space separated numbers
    row = []
    for i in line.strip():
        row.append(int(i))
    struct.append(row)
    
def processInputFile(filePath):
    heights = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,heights)
    else:
        print("File "+filePath+" not found")
    return heights


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

def riskLevel(x,y,gridXMax,gridYMax,heights):
    
    midHeight = getHeight(x,y,heights)

    neighbours = GetValidNeighbours(x,y,gridXMax,gridYMax,heights)
    minNeighbour = min(neighbours)
    
    if (minNeighbour > midHeight):   
        # Is lower, so return risk as 1 + midHeight
        #print("{},{} is low point of {} with height {} risk level {}".format(x,y,neighbours,midHeight,1+midHeight))
        return 1+midHeight
    #else:
    #    print("{},{} is not low point of {} with height {}".format(x,y,neighbours,midHeight))
    
    return 0

def mainTask():
    t1_start = perf_counter()  
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\09a\\tool_src\\input.txt"
    heights = processInputFile(input_path)
    
    gridXMax = len(heights[0])
    gridYMax = len(heights)

    print("Grid is {} by {}".format(gridXMax,gridYMax))

    risk = 0
    for x in range(gridXMax):
        for y in range(gridYMax):
            risk = risk + riskLevel(x,y,gridXMax,gridYMax,heights)

    print(risk)
    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 
if __name__ == "__main__":
    mainTask()