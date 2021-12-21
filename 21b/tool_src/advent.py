import os
from time import perf_counter, process_time
import math


class SnailFishNumber:

    def __init__(self,parent = None, inputString = None):

        self.depth = 0
        self.parent = None
        if not parent == None:
            self.parent = parent
            self.depth  = parent.depth + 1

        self.leftPair = None
        self.leftNumber = -1
        self.leftIsPair = True
        
        self.rightPair = None
        self.rightNumber = -1
        self.rightIsPair = True

        if not inputString is None:
            assert(len(inputString) > 0)
            left,right = SnailFishNumber.splitString(inputString)

            if ',' in left:
                self.leftPair = SnailFishNumber(self,left)
                self.leftIsPair = True                
            else:
                self.leftNumber = int(left)
                self.leftIsPair = False

            if ',' in right:
                self.rightPair = SnailFishNumber(self,right)
                self.rightIsPair = True                
            else:
                self.rightNumber = int(right)
                self.rightIsPair = False

    def getRoot(self):
        if self.parent == None:
            return self
        else:
            return self.parent.getRoot()

    def toString(self):
        left = ""
        if self.leftIsPair:
            left = self.leftPair.toString()
        else:
            left = str(self.leftNumber)
        right = ""
        if self.rightIsPair:
            right = self.rightPair.toString()
        else:
            right = str(self.rightNumber)
        return "["+left+","+right+"]"

    def magnitude(self):
        # 3.m(a)+2.m(b)
        a = 0
        if self.leftIsPair:
            a = self.leftPair.magnitude()
        else:
            a = self.leftNumber
        b = 0
        if self.rightIsPair:
            b = self.rightPair.magnitude()
        else:
            b = self.rightNumber
        return (3*a) + (2*b)


    def incrementRightmostLeaf(self,inc):
        if not self.rightIsPair:
            #print("incrementing {} in {} to {}".format(self.rightNumber,self.toString(),self.rightNumber + inc))
            self.rightNumber = self.rightNumber + inc
        else:
            self.rightPair.incrementRightmostLeaf(inc)

    def incrementLeftmostLeaf(self,inc):
        if not self.leftIsPair:
            #print("incrementing {} in {} to {}".format(self.leftNumber,self.toString(),self.leftNumber + inc))
            self.leftNumber = self.leftNumber + inc
        else:
            self.leftPair.incrementLeftmostLeaf(inc)


    def getParentWithLeftBranchYouCanAddTo(self):
        c = self
        p = self.parent
        #print("c = {} p = {}".format(c.toString(),p.toString()))
        while p.leftPair == c:
            c = p
            p = p.parent            
            if p == None:
                return None
            #print("c = {} p = {}".format(c.toString(),p.toString()))
        #print("Wanted node {}".format(p.toString()))
        return p

    def getParentWithRightBranchYouCanAddTo(self):
        c = self
        p = self.parent
        #print("c = {} p = {}".format(c.toString(),p.toString()))
        while p.rightPair == c:
            c = p
            p = p.parent            
            if p == None:
                return None
            #print("c = {} p = {}".format(c.toString(),p.toString()))
        #print("Wanted node {}".format(p.toString()))
        return p

    def explode(self):
        assert(not self.leftIsPair)
        assert(not self.rightIsPair)
        #print("explode {} left value {} right value {}".format(self.toString(),self.leftNumber,self.rightNumber))

        assert(not self.parent == None)
        # increment number to the left in the original string
        # go up, until you can go left, go left, then go all the way right...
        leftStart = self.getParentWithLeftBranchYouCanAddTo()
        if not leftStart == None:
            if leftStart.leftIsPair:
                leftStart.leftPair.incrementRightmostLeaf(self.leftNumber)
            else:
                leftStart.leftNumber = leftStart.leftNumber + self.leftNumber
        else:
            print("Cannot explode left from {}".format(self.toString()))

        # increment number to the right in the original string
        # go up, until you can go right, go right, then go all the way left...
        rightStart = self.getParentWithRightBranchYouCanAddTo()
        if not rightStart == None:
            if rightStart.rightIsPair:
                rightStart.rightPair.incrementLeftmostLeaf(self.rightNumber)
            else:
                rightStart.rightNumber = rightStart.rightNumber + self.rightNumber
        else:
            print("Cannot explode right from {}".format(self.toString()))

    
        # Replace this pair with 0 in parent
        assert(not self.parent == None)
        if self.parent.leftPair == self:
            self.parent.leftIsPair = False
            self.parent.leftNumber = 0
        else:
            assert(self.parent.rightPair == self)
            self.parent.rightIsPair = False
            self.parent.rightNumber = 0


    def triggerFirstExplosion(self):
        if self.depth > 3 and not self.leftIsPair and not self.rightIsPair:
            self.explode()
            return True
        else:
            if self.leftIsPair:
                foundLeft = self.leftPair.triggerFirstExplosion()
                if foundLeft:
                    return True
            if self.rightIsPair:
                foundRight = self.rightPair.triggerFirstExplosion()
                if foundRight:
                    return True
        return False

    def triggerFirstSplit(self):
        if not self.leftIsPair and self.leftNumber > 9:
            #print("Split left {}".format(self.toString()))
            self.leftIsPair = True
            h = (self.leftNumber // 2)
            l = (self.leftNumber // 2) + self.leftNumber % 2
            newStr = "["+ str(h) +","+str(l)+"]"
            self.leftPair = SnailFishNumber(self,newStr)
            return True
        # Left-most not shallowest.
        if self.leftIsPair and self.leftPair.triggerFirstSplit():
            return True

        if not self.rightIsPair and self.rightNumber > 9:
            #print("Split right {}".format(self.toString()))
            self.rightIsPair = True
            h = (self.rightNumber // 2)
            l = (self.rightNumber // 2) + self.rightNumber % 2
            newStr = "["+ str(h) +","+str(l)+"]"
            self.rightPair = SnailFishNumber(self,newStr)
            return True
        
        if self.rightIsPair and self.rightPair.triggerFirstSplit():
            return True
        
        return False

    def reduce(self):

        while True:
            exploded = False
            split = False
            depths = []

            exploded = self.triggerFirstExplosion()
            if not exploded:
                split = self.triggerFirstSplit()            
            if not exploded and not split:
                #print("{} {}".format(self.toString(),"End"))
                break
            else:
                action = "Exploded"
                if split:
                    action = "Split"
                self.getDepths(depths)
                #print("{} {} {}".format(self.toString(),action,depths))

    def getDepths(self,depths):
        if self.leftIsPair:
            self.leftPair.getDepths(depths)
        if self.rightIsPair:
            self.rightPair.getDepths(depths)
        if not self.rightIsPair or not self.leftIsPair:
            depths.append(self.depth)
        


    def splitString(inputString):
        # move from start to pair the brackets until you reach a , at the top level
        # split the string at that index...
        openBracketCount = 0
        left = ""
        right = ""
        for i in range(len(inputString)):
            if inputString[i] == '[':
                openBracketCount += 1
            if inputString[i] == ']':
                openBracketCount -= 1
            if inputString[i] == ',' and openBracketCount == 1:
                left = inputString[1:i]
                right = inputString[i+1:-1]
                break
        assert(len(left) > 0)
        assert(len(right) > 0)
        return left,right        

    def add(currentString,nextString):
        #print("Adding {} + {}".format(currentString,nextString))
        newString = "["+currentString+","+nextString+"]"
        sf = SnailFishNumber(None,newString)
        sf.reduce()
        return sf.toString()


def processInputFile(filePath):
    lines = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            lines.append(x.strip())
    else:
        print("File "+filePath+" not found")
    return lines


def sumOfThreeRoles(dice):
    roll1 = dice[0] + 1
    roll2 = dice[0] + 2
    roll3 = dice[0] + 3
    r = roll1+roll2+roll3
    print("{}+{}+{} = ({})".format(roll1,roll2,roll3,r))
    dice[0] = roll3
    dice[1]= r


def sumOfNextThreeValues(diceRolls,n):
    return diceRolls[n]+diceRolls[n+1]+diceRolls[n+2]

def playGame(diceRolls):
    p1Start = 4-1 # 0-9
    p2Start = 8-1 # 0-9
    p1Score = 0
    p2Score = 0
    p1Square = p1Start
    p2Square = p2Start

    # There are a limited number of rolls in diceRolls

    winningScore = 21

    available = len(diceRolls)
    diceRolled = 0
    while p1Score < winningScore and p2Score < winningScore:
        # player 1 turn

        if (diceRolled + 3) >= available:
            break

        roll = sumOfNextThreeValues(diceRolls,diceRolled)
        diceRolled = diceRolled + 3
        #print("The number of squares we will move forward is {}".format(roll))
        #ignoringLaps = (roll % 10)
        #print("Loops around the board don't matter, so it's really only {} steps around the board".format(ignoringLaps))
        p1Square = (p1Square + roll) % 10
        #print("Moves player forward to board cell {} which is labelled {}".format(p1Square,p1Square+1))
        p1Score = p1Score + (p1Square+1)
        #print("Player 1 rolls {} and moves to space {} for a total score of {}".format(roll,p1Square+1,p1Score))

        if p1Score >= winningScore or p2Score >= winningScore:
            break

        # player 2 turn

        if (diceRolled + 3) >= available:
            break

        roll = sumOfNextThreeValues(diceRolls,diceRolled)
        diceRolled = diceRolled + 3
        #print("The number of squares we will move forward is {}".format(roll))
        #ignoringLaps = (roll % 10)
        #print("Loops around the board don't matter, so it's really only {} steps around the board".format(ignoringLaps))
        p2Square = (p2Square + roll) % 10
        #print("Moves player forward to board cell {} which is labelled {}".format(p2Square,p2Square+1))
        p2Score = p2Score + (p2Square+1)
        #print("Player 2 rolls {} and moves to space {} for a total score of {}".format(roll,p2Square+1,p2Score))

    if p1Score >= winningScore or p2Score >= winningScore:
        if p2Score > p1Score:
            #print("Player 2 wins with score of {} with game dice {}".format(p2Score,diceRolls))
            return 2
        else:
            #print("Player 1 wins with score of {} with game dice {}".format(p1Score,diceRolls))
            return 1

    return 0

def rollDiceAndSeeIfSomeoneHasWon(diceRolledSoFar,outcomes):

    #print("depth {} input {}".format(len(diceRolledSoFar),diceRolledSoFar))

    diceRolledSoFar.append(1)
    outcomeFor1 = playGame(diceRolledSoFar)
    if outcomeFor1 == 2:
        outcomes[2] = outcomes[2]+1
    elif outcomeFor1 == 1:
        outcomes[1] = outcomes[1]+1
    elif 0 == outcomeFor1:
        #No one won yet, recurse again for 1
        rollDiceAndSeeIfSomeoneHasWon(diceRolledSoFar,outcomes)
        
    diceRolledSoFar.pop() # pop 1
    diceRolledSoFar.append(2)
    outcomeFor2 = playGame(diceRolledSoFar)
    if outcomeFor2 == 2:
        outcomes[2] = outcomes[2]+1
    elif outcomeFor2 == 1:
        outcomes[1] = outcomes[1]+1
    elif 0 == outcomeFor2:
        #No one won yet, recurse again for 2
        rollDiceAndSeeIfSomeoneHasWon(diceRolledSoFar,outcomes)
    
    diceRolledSoFar.pop() # pop 2
    diceRolledSoFar.append(3)
    outcomeFor3 = playGame(diceRolledSoFar)
    if outcomeFor3 == 2:
        outcomes[2] = outcomes[2]+1
    elif outcomeFor3 == 1:
        outcomes[1] = outcomes[1]+1
    elif 0 == outcomeFor3:
        #No one won yet, recurse again for 3
        rollDiceAndSeeIfSomeoneHasWon(diceRolledSoFar,outcomes)
    diceRolledSoFar.pop() # pop3

    #print(outcomes)

def mainTask():
    t1_start = perf_counter()  
    
    deterministicDice = [0,0]

    p1Start = 4-1 # 0-9
    p2Start = 8-1 # 0-9
    #Player 1 starting position marked: 4
    #Player 2 starting position marked: 8
    p1Score = 0
    p2Score = 0
    p1Square = p1Start
    p2Square = p2Start

    diceRolls = []
    outcomes = [0,0,0]
    
    rollDiceAndSeeIfSomeoneHasWon(diceRolls,outcomes)

    print(outcomes)

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()