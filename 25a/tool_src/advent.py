import sys
import os
from time import perf_counter, process_time
import math
import itertools

def parseInstruction(line):
    line = line.strip()
    chars = []
    for c in line:
        chars.append(c)
    return chars

def printState(stepN,seaFloor):
    if stepN == 0:
        print("Initial state:")
    else:
        print("After {} steps:".format(stepN))
    for line in seaFloor:
        st = ""
        for c in line:
            st += c
        print(st)

def isEastSeaCucumber(x,y,seaFloor):
    return seaFloor[y][x] == '>'

def isSouthSeaCucumber(x,y,seaFloor):
    return seaFloor[y][x] == 'v'


def isEastSpace(x,y,maxX,maxY,seaFloor):
    s = x+1
    if s == maxX:
        s = 0
    return seaFloor[y][s] == '.'

def isSouthSpace(x,y,maxX,maxY,seaFloor):
    s = y+1
    if s == maxY:
        s = 0
    return seaFloor[s][x] == '.'

def moveEast(x,y,maxX,maxY,seaFloor):
    s = x+1
    if s == maxX:
        s = 0
    seaFloor[y][x] = "."
    assert(seaFloor[y][s] == ".")
    seaFloor[y][s] = ">"

def moveSouth(x,y,maxX,maxY,seaFloor):
    s = y+1
    if s == maxY:
        s = 0
    seaFloor[y][x] = "."
    assert(seaFloor[s][x] == ".")
    seaFloor[s][x] = "v"


def findMovement(seaFloor):
    
    maxX = len(seaFloor[0])
    maxY = len(seaFloor)
    movingTotal = 0
    movingEast = []
    # Movement east?
    for y in range(0,maxY):
        for x in range(0,maxX):
            if isEastSeaCucumber(x,y,seaFloor) and isEastSpace(x,y,maxX,maxY,seaFloor):
                #print("({},{}) should move east".format(x,y))
                movingEast.append((x,y))
                movingTotal = movingTotal + 1
    # Apply east movements...
    for x,y in movingEast:
        moveEast(x,y,maxX,maxY,seaFloor)

    # Movement south?
    movingSouth = []
    for y in range(0,maxY):
        for x in range(0,maxX):
            if isSouthSeaCucumber(x,y,seaFloor) and isSouthSpace(x,y,maxX,maxY,seaFloor):
                #print("({},{}) should move south".format(x,y))
                movingSouth.append((x,y))
                movingTotal = movingTotal + 1
    # Apply east movements...
    for x,y in movingSouth:
        moveSouth(x,y,maxX,maxY,seaFloor)
    return movingTotal > 0


def mainTask():
    t1_start = perf_counter()  
    
    
    seaFloor = [ parseInstruction(number) for number in open(f'{sys.path[0]}/input.txt', 'r')]
    printState(0,seaFloor)

    step = 0
    for step in range(1,1000):
        foundMovement = findMovement(seaFloor)
        #printState(step,seaFloor)
        if not foundMovement:
            break

    if not foundMovement:
        print("No movement on step {}".format(step))

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 
    

if __name__ == "__main__":
    mainTask()