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


def mainTask():
    t1_start = perf_counter()  
    
    input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\18a\\tool_src\\input.txt"
    lines = processInputFile(input_path)
    #print(lines)

    maxMag = 0

    for a in lines:
        for b in lines:
            if a != b:
                sumStr = SnailFishNumber.add(a,b)
                s = SnailFishNumber(None,sumStr)
                m = s.magnitude()
                if m > maxMag:
                    maxMag = m
                sumStr2 = SnailFishNumber.add(b,a)
                s = SnailFishNumber(None,sumStr2)
                m = s.magnitude()
                if m > maxMag:
                    maxMag = m


    print("Final magnitude {}".format(maxMag))


    # 3078 is too high

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()