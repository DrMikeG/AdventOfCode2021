import sys
import os
from time import perf_counter, process_time
import math
from itertools import combinations

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

    for x in range( max(minC,instruction[1]), min(maxC,instruction[2]+1)):
        for y in range( max(minC,instruction[3]), min(maxC,instruction[4]+1)):
            for z in range( max(minC,instruction[5]), min(maxC,instruction[6]+1)):
                tups.append( (x,y,z) )        
    return tups
                
def processInstruction(instruction,onCubes):
    # If on, turn on
    # If off, turn off in on
    if (instruction[0] == 1):
        coordsToTurnOn = makeTuplesInRange(instruction)
        print("Turning on up to {} lights".format(len(coordsToTurnOn)))
        for ifOn in coordsToTurnOn:
            onCubes.add(ifOn)
    elif (instruction[0] == 0):
        coordsToTurnOn = makeTuplesInRange(instruction)
        print("Turning off up to {} lights".format(len(coordsToTurnOn)))
        for ifOn in coordsToTurnOn:
            if ifOn in onCubes:
                onCubes.remove(ifOn)

    


def mainTask():
    t1_start = perf_counter()  
    
    # [function(number) for number in numbers if condition(number)]
    #numbers = [12, 34, 1, 4, 4, 67, 37, 9, 0, 81]
    #result = [number for number in numbers if number > 5]
    #print(result)
    

    instructions = [ parseInstruction(number) for number in open(f'{sys.path[0]}/input.txt', 'r')]
    print(instructions)

    onCubes = set()

    for instruction in instructions:
        processInstruction(instruction,onCubes)
        print("There are {} lights on ".format(len(onCubes)))



    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()