import os
from time import perf_counter
import math

def makeTarget(x1,x2,y1,y2):
    target = []
    if x1 < x2:
        target.append(x1)
        target.append(x2)
    else:
        target.append(x2)
        target.append(x1)

    if y1 > y2:
        target.append(y1)
        target.append(y2)
    else:
        target.append(y2)
        target.append(y1)
    
    print("Made target region {}..{}, {}..{}".format(target[0],target[1],target[2],target[3]))
    
    return target

def isInTarget(target,x,y):

    if x >= target[0]:
        if x <= target[1]:
            if y >= target[3]:
                if y <= target[2]:
                    return True    
    return False

def shotCouldStillHitTarget(target,x,y,x_velocity):

    if isInTarget(target,x,y):
        return True

    # is shot long?
    isShotLong = False
    x1 = target[0]
    x2 = target[1]
    if x1 < 0 and x2 < 0:
        # shooting backwards
        isShotLong = x < x1
    
    if x1 > 0 and x2 > 0:
        # shooting forwards
        isShotLong = x > x2

    if x1 < 0 and x2 > 0:
        # target crosses zero
        if x > x2:
            isShotLong = True
        elif x < x1: 
            isShotLong = True
    
    if isShotLong:
        return False
    
    # X can be before the target area, or directly over the target area, dropping vertically
    y1 = target[2]
    y2 = target[3]
    if x_velocity == 0:
        if y > y2 and y > y1:
            # are we above the target?
            if x >= x1 and x <= x2:
                return True
            else:
                return False
        else:
            # fell below target
            return False    

    return True


def getTrajectory(forward,upward,target):
    assert(forward >= 0)
    #The probe's x,y position starts at 0,0.
    steps = []
    xPos = 0
    yPos = 0
    stepVelocityX = forward
    stepVelocityY = upward
    steps.append((xPos,yPos))
    #print("Step ({},{})".format(xPos,yPos))
    while shotCouldStillHitTarget(target,xPos,yPos,stepVelocityX):
        

        if isInTarget(target,xPos,yPos):
            break

        # The probe's x position increases by its x velocity.
        xPos = xPos + stepVelocityX
        # The probe's y position increases by its y velocity.
        yPos = yPos + stepVelocityY
        # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, 
        if stepVelocityX > 0:
            stepVelocityX = stepVelocityX - 1
        # increases by 1 if it is less than 0, or does not change if it is already 0.
        if stepVelocityX < 0:
            stepVelocityX = stepVelocityX + 1        
        # Due to gravity, the probe's y velocity decreases by 1.
        stepVelocityY = stepVelocityY - 1

        steps.append((xPos,yPos))
        #print("Step ({},{})".format(xPos,yPos))
        #assert(len(steps) < 10000)
        #if (len(steps) > 10):
        #    return steps
    return steps

def doesAnyStepHitTarget(steps,target):
    for step in steps:
        if isInTarget(target,step[0],step[1]):
            #print("step {} hit target".format(step))
            return True
    
    #print("no steps hit target")
    return False

def printTrajectoryAndReturnMaxY(steps,target):
    maxStepY = 0
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    for step in steps: 
        if step[0] > maxX:
            maxX = step[0]
        if step[0] < minX:
            minX = step[0]
        if step[1] > maxY:
            maxY = step[1]
        if step[1] < minY:
            minY = step[1]
        if step[1] > maxStepY:
            maxStepY = step[1]

    #print("Trajectory max heigh achieved {}".format(maxStepY))

    if target[0]-1 < minX:
        minX =target[0]-1
    if target[1]+1 > maxX:
        maxX =target[1]+1
    if target[3]-1 < minY:
        minY =target[3]-1
    if target[2]+1 > maxY:
        maxY =target[2]+1
    
    for y in range(maxY,minY,-1):
        row = ""
        for x in range(minX,maxX+1):
            if (x,y) == (0,0):
                row += "S"
            elif (x,y) in steps:
                row += "#"
            elif isInTarget(target,x,y):
                row += "T"
            else:
                row += "."
    #    print(row)
    return maxStepY


def mainTask():
    t1_start = perf_counter()  
    
    
    targetSample = makeTarget(20,30,-10,-5)
    
    #stepsSample = getTrajectory(7,2,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(6,3,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(9,0,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(17,-4,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(5,4,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(6,4,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    #stepsSample = getTrajectory(6,10,targetSample)
    #maxYSample = printTrajectoryAndReturnMaxY(stepsSample,targetSample)

    target = makeTarget(128,160,-142,-88)
    #steps = getTrajectory(16,70,target)
    #maxY = printTrajectoryAndReturnMaxY(steps,target)

    #target = makeTarget(20,30,-10,-5)
    countValidInput = 0
    globalMaxY = 0
    for xInitial in range(0,2500):
        for yInitial in range(-5000,5000):
            steps = getTrajectory(xInitial,yInitial,target)
            hitsTarget = doesAnyStepHitTarget(steps,target)
            if hitsTarget == True:          
                countValidInput = countValidInput +1
                #maxY = printTrajectoryAndReturnMaxY(steps,target)
                #print("Starting velocities {},{} does hit target after {} steps with max height {}".format(xInitial,yInitial,len(steps),maxY))
                #if maxY > globalMaxY:
                    #globalMaxY = maxY
            #else:
                #print("Starting velocities {},{} does not hit target".format(xInitial,yInitial))

    # 244 is too low
    # 248 is too low
    # 279 is too low
    # 675 ?
    # 2994 ?
    

    print("Total valid inputs found {}".format(countValidInput))

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()