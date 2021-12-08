import os


def isCharacterN(stringValue,characterIndex,wantedChar):
    return stringValue[characterIndex-1] == wantedChar

def processLineOfInputIntoStruct(line,struct):
    # Line is 10 space separated signals 
    # followed by pipe
    # followed by 4 space separated numbers
    
    signalsNumbs = line.strip().split("|",2)
    
    assert(len(signalsNumbs) == 2)
    lineSignals = signalsNumbs[0].strip().split()
    struct[0].append(lineSignals)

    lineNums = signalsNumbs[1].strip().split()
    struct[1].append(lineNums)
    
def processInputFile(filePath):
    
    # First line is numbers (comma separated)
    # then boards come every 5 lines
    # 5 x 5 2 digit numbers

    readLines = []
    signals = []
    numbers = []
    readLines.append(signals)
    readLines.append(numbers)
    
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            processLineOfInputIntoStruct(x,readLines)
    else:
        print("File "+filePath+" not found")

    return readLines

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
            if len(num) == 2: # 2
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

def mainTask():

    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\08a\\tool_src\\input.txt"
    struct = processInputFile(input_path)
    count = countNumbers(struct)
    print(count)

if __name__ == "__main__":

    mainTask()