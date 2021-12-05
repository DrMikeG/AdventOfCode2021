import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    lineS = line.strip()
    if len(lineS) > 0 :
        struct.append(lineS)
    
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

def filterToAndShortedInputToMostCommonLeadingBit(struct,index):
    
    nChars = len(struct[0])
    print("processing all digits in column "+str(index))
    oneCount = 0
    zeroCount = 0
    keepWithLeadingBit = '1'
    for num in struct:
        if num[index] == '1':
            oneCount = oneCount + 1
        if num[index] == '0':
            zeroCount = zeroCount + 1
    
    if (oneCount >= zeroCount):
        print("Keep numbers with leading digit of 1")
        keepWithLeadingBit = '1'
    else:
        print("Keep numbers with leading digit of 0")
        keepWithLeadingBit = '0'

    newStruct = []
    for num in struct:
        if num[index] == keepWithLeadingBit:
            newStruct.append(num)

    return newStruct

def filterToAndShortedInputToLeastCommonLeadingBit(struct,index):
    
    nChars = len(struct[0])
    print("processing all digits in column "+str(index))
    oneCount = 0
    zeroCount = 0
    keepWithLeadingBit = '1'
    for num in struct:
        if num[index] == '1':
            oneCount = oneCount + 1
        if num[index] == '0':
            zeroCount = zeroCount + 1
    
    if (oneCount >= zeroCount):
        print("Keep numbers with leading digit of 1")
        keepWithLeadingBit = '1'
    else:
        print("Keep numbers with leading digit of 0")
        keepWithLeadingBit = '0'

    newStruct = []
    for num in struct:
        if num[index] != keepWithLeadingBit:
            newStruct.append(num)

    return newStruct


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

    winningTurns = min(boardScores)
    bestBoardN = boardScores.index(winningTurns)
    

    print("Best board is board {} winning after {} turns".format(bestBoardN,winningTurns))

    sumU = sumUndrawnNumbers(boards[bestBoardN],turnBoards[bestBoardN],winningTurns)

    invd = { v:k for k,v in turnMap.items() }
    numberJustCalled = invd[winningTurns]
    print("Final score is {} X {} = {}".format(sumU,numberJustCalled,(sumU*numberJustCalled)))


def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\04a\\tool_src\\input.txt"
    struct = processInputFile(input_path)
    turnMap, boards = processStructIntoMapAndBoards(struct)
    turnBoards = processBoardsWithMap(turnMap, boards)
    findWiningBoard(boards,turnBoards,turnMap)

if __name__ == "__main__":

    mainTask()