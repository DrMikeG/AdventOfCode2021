import os
from time import perf_counter

def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    # Line is 10 space separated signals 
    # followed by pipe
    # followed by 4 space separated numbers
    
    row = []
    for i in line.strip():
        row.append(int(i))
    struct.append(row)
    
def processInputFile(filePath):
    
    # First line is numbers (comma separated)
    # then boards come every 5 lines
    # 5 x 5 2 digit numbers

    heights = []
    
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,heights)
    else:
        print("File "+filePath+" not found")

    return heights

def countNumbers(struct):
    # 0 - 6 segments
    # 1 - 2 segments*
    # 2 - 5 segments
    # 3 - 5 segments
    # 4 - 4 segments*
    # 5 - 5 segments
    # 6 - 6 segments
    # 7 - 3 segments*
    # 8 - 7 segments*
    # 9 - 6 segments
    # The digits 1[2], 4[4], 7[3], and 8[7] each use a unique number of segments
    numbers = struct[1]
    count = 0
    for lines in numbers:
        for num in lines:
            if len(num) == 2: # 1
                print(num)
                count = count + 1   
            if len(num) == 4: # 4
                print(num)
                count = count + 1
            if len(num) == 3: # 7
                print(num)
                count = count + 1
            if len(num) == 7: # 8
                print(num)
                count = count + 1
    return count

def getDigit(num,signalOne,signalFour):
    if len(num) == 2: # 1
        return 1   
    if len(num) == 4: # 4
        return 4
    if len(num) == 3: # 7
        return 7
    if len(num) == 7: # 8
        return 8

    # if length is 6, number is 6 or 9 or 0
    #   9 contains 4
    #   0 only contains 1
    #   6 does not contain 1 or 4
    if len(num) == 6:
        # does num contain the two chars in signalOne?
        if countAsInBs(num,signalFour) == 4:
            return 9
        elif countAsInBs(num,signalOne) == 2:
            return 0
        else:
            return 6

    # Hard: What is 4?
    # if length is 5, number is 2 or 3 or 5
    #   3 contains 1
    #   2 has 2 values from digit 4
    #   5 has 3 values from digit 4
    #   
    if len(num) == 5:
        if signalOne[0] in num and signalOne[1] in num:
            return 3
        else:
            countN = countAsInBs(num,signalFour)
        if countN == 2:
            return 2
        elif countN == 3:
            return 5
    
    print(num)
    assert(False)
    return -1

def countAsInBs(aS,bS):
    count = 0
    for a in aS:
        if a in bS:
            count = count+ 1
    return count

def unscramble(signals,numbers):
    #print(signals)
    #print(numbers)

    foundOne = False
    foundFour = False
    signalOne = ''
    signalFour = ''
    assert(len(signals) == 10)
    for signal in signals:
        if len(signal) == 2:
            foundOne = True
            signalOne = signal
        if len(signal) == 4:
            foundFour = True
            signalFour = signal

    assert(foundOne)
    assert(foundFour)
    print("Digit 1 is signal {}".format(signalOne))
    print("Digit 4 is signal {}".format(signalFour))

    digit0 = getDigit(numbers[0],signalOne,signalFour)
    digit1 = getDigit(numbers[1],signalOne,signalFour)
    digit2 = getDigit(numbers[2],signalOne,signalFour)
    digit3 = getDigit(numbers[3],signalOne,signalFour)

    base10 = (digit0*1000) + (digit1*100) + (digit2*10) + (digit3) 

    print("{} [{},{},{},{}]".format(numbers,digit0,digit1,digit2,digit3))
# 1 = [2] ab
# 2 = [5] ?
# 3 = [5] ?
# 4 = [4] eafb
    
# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf

#  dddd
# e    a
# e    a
#  ffff
# g    b
# g    b
#  cccc
#
# 1 = [2] ab
# 2 = [5] ?
# 3 = [5] ?
# 4 = [4] eafb
# 5 = [5] ?
# 6 = [6] ?
# 7 = [3] dab
# 8 = [7] acedgfb
# 9 = [6] ? 

# Easy:

# if length is 7, number = 8
# if length is 2, number = 2
# if length is 3, number = 7
# if length is 4, number = 4

# Medium: What is 1?
# if length is 6, number is 6 or 9 or 0
#   9 contains 4
#   0 only contains 1
#   6 does not contain 1 or 4

# Hard: What is 4?
# if length is 5, number is 2 or 3 or 5
#   3 contains 1
#   2 has 2 values from digit 4
#   5 has 4 values from digit 4
#   
    return base10


def getHeight(x,y,heights):
    return heights[y][x]

def setHeight(x,y,heights,val):
    heights[y][x] = val


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
        #print("{},{} is not low point of {} with height {}".format(x,y,neighbours,midHeight))
    
    return 0

def findBasinMemberPositions(basin,gridXMax,gridYMax,heights):
    positions = []
    for x in range(gridXMax):
        for y in range(gridYMax):
            if ( getHeight(x,y,heights) == basin ):
                positions.append([x,y])
    return positions

def lowestNeighbourPosition(x,y,gridXMax,gridYMax,heights):
    # return value and position of lowestNeihbour
    ret   = {'any': False, 'x': 0, 'y': 0, 'value': 9 }
    up    = [x,y-1]
    down  = [x,y+1]
    left  = [x-1,y]
    right = [x+1,y]

    if isValidPosition(up[0],up[1],gridXMax,gridYMax):
        val = getHeight(up[0],up[1],heights)
        if val < 9 and val < ret['value']:
            ret['value'] = val
            ret['x'] = up[0]
            ret['y'] = up[1]
            ret['any'] = True

    if isValidPosition(down[0],down[1],gridXMax,gridYMax):
        val = getHeight(down[0],down[1],heights)
        if val < 9 and val < ret['value']:
            ret['value'] = val
            ret['x'] = down[0]
            ret['y'] = down[1]
            ret['any'] = True
    if isValidPosition(left[0],left[1],gridXMax,gridYMax):
        val = getHeight(left[0],left[1],heights)
        if val < 9 and val < ret['value']:
            ret['value'] = val
            ret['x'] = left[0]
            ret['y'] = left[1]
            ret['any'] = True
    if isValidPosition(right[0],right[1],gridXMax,gridYMax):
        val = getHeight(right[0],right[1],heights)
        if val < 9 and val < ret['value']:
            ret['value'] = val
            ret['x'] = right[0]
            ret['y'] = right[1]
            ret['any'] = True
    return ret


def expandBasin(basin,gridXMax,gridYMax,heights):
    # look at all neighbours of current members of basin
    # find the minimum value and add it to the basin
    # if expanded, return true
    # if all neigbours are 9, then return false

    basinPositions = findBasinMemberPositions(basin,gridXMax,gridYMax,heights)
    assert(len(basinPositions) > 0)

    lowestValue = 9
    lowestPosition = [0,0]
    foundAnOption = False

    for pos in basinPositions:
        thisPosNeighbourAnalysis = lowestNeighbourPosition(pos[0],pos[1],gridXMax,gridYMax,heights)
        if thisPosNeighbourAnalysis['any'] == True:
            foundAnOption = True
            if thisPosNeighbourAnalysis['value'] < lowestValue:
                lowestPosition[0] = thisPosNeighbourAnalysis['x']
                lowestPosition[1] = thisPosNeighbourAnalysis['y']
    
    if foundAnOption:
        setHeight(lowestPosition[0],lowestPosition[1],heights,basin)
    
    return foundAnOption

def allNumbersAre9orMove(heights):
    for xs in heights:
        if min(xs) < 9:
            return False
    return True

def printHeights(heights):
    print()
    for xs in heights:     
        row = ""
        for ys in xs:
            y = ys
            if ys > 9:
                y = ys - 97
                row = row +chr(ys)+' '
            else:
                row = row +'{0:01d} '.format(ys)
        print(row)

def mainTask():
    t1_start = perf_counter()  
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\09b\\tool_src\\input.txt"
    heights = processInputFile(input_path)
    
    gridXMax = len(heights[0])
    gridYMax = len(heights)

    print("Grid is {} by {}".format(gridXMax,gridYMax))

    #for i in range(97,110):
        #char = chr(i)
        #print(char)

    lowPoints = []

    for x in range(gridXMax):
        for y in range(gridYMax):
            if riskLevel(x,y,gridXMax,gridYMax,heights) > 0:
                # x y is a lowpoint
                lowPoints.append([x,y])

    nBasin = len(lowPoints)

    print("\nFound {} low points {}\n".format(nBasin,lowPoints))

    # Set the low points to be the bottom of unique basins
    for i in range(nBasin):
        coord = lowPoints[i]
        char = i+97
        setHeight(coord[0],coord[1],heights,char)

    #printHeights(heights)

    expanded = True
    while(expanded):
        expanded = False
        for i in range(nBasin):
            expandedI = expandBasin(i+97,gridXMax,gridYMax,heights)
            if expandedI:
                expanded = True
                #printHeights(heights)

    # No more expansion possible
    assert( allNumbersAre9orMove(heights) )

    basinSizes = []

    for i in range(nBasin):
        pos = findBasinMemberPositions(i+97,gridXMax,gridYMax,heights)
        #print("Basin {} has {} members".format(chr(i+97),len(pos)))
        basinSizes.append( (chr(i+97), len(pos)) )
    
    #print(basinSizes)
    basinSizes.sort(reverse=True, key=lambda a: a[1])
    #print(basinSizes)

    print(basinSizes[0][1]*basinSizes[1][1]*basinSizes[2][1])
    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":

    mainTask()