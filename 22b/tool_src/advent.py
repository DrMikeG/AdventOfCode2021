import sys
import os
from time import perf_counter, process_time
import math
import itertools

def parseInstruction(line):

    #on x=10..12,y=10..12,z=10..12
    parts = line.strip().replace(".."," ").replace("="," ").replace(","," ").split()
    #print(parts)
    assert(len(parts)==10)
    asNumbers = [(1 if (parts[0]=="on") else 0) ,int(parts[2]),int(parts[3]),int(parts[5]),int(parts[6]),int(parts[8]),int(parts[9])]
    return asNumbers


def makeTuplesInRange(instruction):
    minC = -50
    maxC = 51

    tups = []

    for x in range(instruction[1], instruction[2]+1):
        for y in range( instruction[3], instruction[4]):
            for z in range( instruction[5], instruction[6]+1):
                tups.append( (x,y,z) )        
    return tups
                
def processInstruction(instruction,onCubes):
    # If on, turn on
    # If off, turn off in on
    

    if (instruction[0] == 1):
        x1 = instruction[1]
        x2 = instruction[2]+1
        y1 = instruction[3]
        y2 = instruction[4]+1
        z1 = instruction[5]
        z2 = instruction[6]+1  
        #coordsToTurnOn = makeTuplesInRange(instruction)
        #print("Turning on up to {} lights".format(len(coordsToTurnOn)))
        for turnOn in itertools.product(*[list(range(x1,x2)),list(range(y1,y2)),list(range(z1,z2))]):
            onCubes.add(turnOn)
    elif (instruction[0] == 0):
        x1 = instruction[1]
        x2 = instruction[2]
        y1 = instruction[3]
        y2 = instruction[4]
        z1 = instruction[5]
        z2 = instruction[6]
        onCubedCopy = onCubes.copy()
        #coordsToTurnOn = makeTuplesInRange(instruction)
        #print("Turning off up to {} lights".format(len(coordsToTurnOn)))
        #for ifOn in coordsToTurnOn:
        
        for lightOn in onCubedCopy:
            keepOn = True
            if lightOn[0] >= x1 and lightOn[0] <= x2:
                if lightOn[1] >= y1 and lightOn[1] <= y2:
                    if lightOn[2] >= z1 and lightOn[2] <= z2:
                        keepOn = False
            #if keepOn:
                #print("light {} is not in region {}..{},{}..{},{}..{}".format(lightOn,x1,x2,y1,y2,z1,z2))
            #else:
            if not keepOn:
                #print("light {} is in region {}..{},{}..{},{}..{} - turning off".format(lightOn,x1,x2,y1,y2,z1,z2))
                onCubes.remove(lightOn)
        

def mainTask():
    t1_start = perf_counter()  
    
    # [function(number) for number in numbers if condition(number)]
    #numbers = [12, 34, 1, 4, 4, 67, 37, 9, 0, 81]
    #result = [number for number in numbers if number > 5]
    #print(result)
    
    
    instructions = [ parseInstruction(number) for number in open(f'{sys.path[0]}/input_small2.txt', 'r')]
    #print(instructions)

    onCubes = set()

    for instruction in instructions:
        processInstruction(instruction,onCubes)
        print("There are {} lights on ".format(len(onCubes)))



    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()