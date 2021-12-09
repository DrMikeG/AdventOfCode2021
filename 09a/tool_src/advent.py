import os


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
        print("{},{} is low point of {} with height {} risk level {}".format(x,y,neighbours,midHeight,1+midHeight))
        return 1+midHeight
    else:
        print("{},{} is not low point of {} with height {}".format(x,y,neighbours,midHeight))
    
    return 0

def mainTask():

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

if __name__ == "__main__":

    mainTask()