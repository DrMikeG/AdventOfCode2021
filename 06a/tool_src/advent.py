import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    # Line is just csv
    lineTuple = line.strip().split(",")
    for str in lineTuple:
        struct.append(int(str))
    
    
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

def processStructIntoMapAndBoards(struct):
    
    # You only actually care about the last number to be drawn for a row a column
    # i.e max turn
    # build a look-up from number to turn drawn
    # are all numbers drawn?
    # store both rows a 

    turnMap = {}
    line1 = struct[0]
    numbersDrawn = line1.split(',')
    for turn in range(len(numbersDrawn)):
        turnMap[int(numbersDrawn[turn])] = turn
    print(turnMap)
    
    nBoards = int((len(struct) - 1) / 5)
    print("Making "+str(nBoards)+" boards")
    
    nLinesInBoard = 5

    boards = []
    for boardI in range(nBoards):
        board = []
        # For each row in this board
        for boardRowI in range(nLinesInBoard):
            rowInStruct = 1 +  (boardI * nLinesInBoard) + boardRowI
            lineNumbersStrs = struct[rowInStruct].split()
            lineNumbers = [int(item) for item in lineNumbersStrs]
            assert len(lineNumbers) == 5
            board.append(lineNumbers)
        # Make the columns
        for boardColI in range(nLinesInBoard):
            column = []
            for rowI in range(nLinesInBoard):
                column.append(board[rowI][boardColI])
            board.append(column)
        #print(board)
        boards.append(board)

    return turnMap, boards

def processBoardsWithMap(turnMap, boards):
    # Replace every number with the turn it is draw, or 100 if never drawn

    turnBoards = []

    nBoards = len(boards)
    for boardI in range(nBoards):
        turnBoard = []
        nRowColCount = len(boards[boardI])
        for rowI in range(nRowColCount):
            turnRow = []
            nNumbers = len(boards[boardI][rowI])
            for i in range(nNumbers):
                number = boards[boardI][rowI][i]
                if number in turnMap:
                    #boards[boardI][rowI][i] = turnMap[number]
                    turnRow.append(turnMap[number])
                else:
                    #boards[boardI][rowI][i] = 100
                    turnRow.append(100)
            turnBoard.append(turnRow)
        turnBoards.append(turnBoard)

    #print(boards)
    return turnBoards

def maxTurnsInLines(board):
    nRowColCount = len(board)
    maxInRow = []
    # For each row    
    for row in board:
        maxInRow.append(max(row))
    # return the best row and its index for this board
    return min(maxInRow),maxInRow.index(min(maxInRow))


def sumUndrawnNumbers(board,turnBoard,winningNTurns):
    #All undrawn numbers are all numbers of the first half of the board lists (rows) that are greater than winningTurns
    sum = 0
    nRows = int(len(board)/2)
    for r in range(nRows):
        nVals = len(turnBoard[r])
        for n in range(nVals):
            if turnBoard[r][n] > winningNTurns:
                sum = sum + board[r][n]
    return sum

def findWiningBoard(boards,turnBoards,turnMap):
    print(boards)
    print(turnBoards)
    # For each line, find the max turn
    # For each board, find the min line

    boardScores = []
    boardTurnsTaken = []
    for board in turnBoards:    
        best, rowN = maxTurnsInLines(board)
        print("Board {} finished in {} with line {}".format(turnBoards.index(board),best,rowN))
        boardScores.append(best)

    winningTurns = max(boardScores)
    bestBoardN = boardScores.index(winningTurns)
    

    print("Best board is board {} winning after {} turns".format(bestBoardN,winningTurns))

    sumU = sumUndrawnNumbers(boards[bestBoardN],turnBoards[bestBoardN],winningTurns)

    invd = { v:k for k,v in turnMap.items() }
    numberJustCalled = invd[winningTurns]
    print("Final score is {} X {} = {}".format(sumU,numberJustCalled,(sumU*numberJustCalled)))

def findMaxXY(struct):
    # x1,y1,x2,y2
    maxX = 0
    maxY = 0
    for line in struct:
        if line[0] > maxX: maxX = line[0]
        if line[2] > maxX: maxX = line[2]
        if line[1] > maxY: maxY = line[1]
        if line[3] > maxY: maxY = line[3]
    return maxX,maxY


def populateGrid(struct):
    maxX,maxY = findMaxXY(struct)
    grid = []    
    for _ in range(maxY+1):
        gridLine = []
        for _ in range(maxX+1):
            gridLine.append(0)
        grid.append(gridLine)   
    return grid

def addLineToGrid(grid,line):
    #x1,y1,x2,y2
    # only plot horizontal or vertical
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]

    if x1 == x2:
        # Vertical
        if y2 > y1:
            for y in range(y1,y2+1):
                grid[y][x1] = grid[y][x1] + 1
        else:
            for y in range(y2,y1+1):
                grid[y][x1] = grid[y][x1] + 1
    elif y1 == y2:
        # Horizontal
        if x2 > x1:
            for x in range(x1,x2+1):
                grid[y1][x] = grid[y1][x] + 1
        else:
            for x in range(x2,x1+1):
                grid[y1][x] = grid[y1][x] + 1
    else:
        # Diagonal
        xStep = 1
        yStep = 1
        if x1 > x2: xStep = -1
        if y1 > y2: yStep = -1
        nSteps = abs(x1-x2)
        for s in range(nSteps+1):
            grid[y1+(s*yStep)][x1+(s*xStep)] = grid[y1+(s*yStep)][x1+(s*xStep)] + 1

def printGrid(grid):
    for line in grid:
        print(line)

def countValuesLargerThan2(grid):
    count = 0
    for line in grid:
        for value in line:
            if value > 1:
                count = count + 1
    return count

def runFishDay(struct,day):
    #reduce all values in struct by one
    #all values that go negative become 6 and append 8 to struct
    toAdd = []
    for i in range(len(struct)):
        struct[i] = struct[i] - 1
        if struct[i] == -1:
            struct[i] = 6
            toAdd.append(8)
    for v in toAdd:
        struct.append(v)
    
    print("After {} days: {}".format(day,struct))

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\06a\\tool_src\\input.txt"
    struct = processInputFile(input_path)

    for day in range(80):
        runFishDay(struct,day)    

    print(len(struct))

if __name__ == "__main__":

    mainTask()