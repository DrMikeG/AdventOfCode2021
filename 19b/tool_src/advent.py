import os
import sys
# pip install numpy
import numpy as np

from time import perf_counter, process_time
import math

def processInputFile(filePath):
    lines = []
    if os.path.exists(filePath):
        f = open(filePath, "r")
        for x in f:
            lines.append(x.strip())
    else:
        print("File "+filePath+" not found")
    return lines

def processLine(line,scans):

    if len(scans) == 0:        
        scan = []
        scans.append(scan)
    else:
        scan = scans[-1]

    if ',' in line:
        x,y,z = line.strip().split(",",3)
        scan.append((x,y,z))
    else:        
        scan = []
        scans.append(scan)

def convertToNp(scans):
    
    nps = []
    for scan in scans:
        npScan = np.empty([3, len(scan)])
        for s in scan:
            np.append(npScan,[s[0],s[1],s[2]])
        nps.append(npScan)

    return nps

def generateFourRotations(dir,npScan):
    # This is a scan facing direction X
    # generate and return it's four rotations about 
    rotatedScans = []
    axis = (0,0,1)
    if dir == 0 or dir == 2: # fwd or backwards
        axis = (0,0,1) # next rotate about Z
    elif dir == 1 or dir == 3: # left or right
        axis = (1,0,0) # next rotate about X
    elif dir == 4 or dir == 5: # up or down
        axis = (0,1,0) # next rotate about Y
    rotatedScans.append(np.rot90(npScan,0,axis))
    rotatedScans.append(np.rot90(npScan,1,axis))
    rotatedScans.append(np.rot90(npScan,2,axis))
    rotatedScans.append(np.rot90(npScan,3,axis))
    return rotatedScans

def faceDifferentWayAndGenerateFourRotations(npScan):
    # This is a scan, facing direction 0
    rotatedScans = []
    
    # 0-3 are rotations in (0,1,0) (Y / up)
    rotatedScans.extend(generateFourRotations(0,np.rot90(npScan,0,(0,1,0))))
    rotatedScans.extend(generateFourRotations(1,np.rot90(npScan,1,(0,1,0))))
    rotatedScans.extend(generateFourRotations(2,np.rot90(npScan,2,(0,1,0))))
    rotatedScans.extend(generateFourRotations(3,np.rot90(npScan,3,(0,1,0))))
    # 4 & 5 are rotations about (1,0,0) (X / right)
    rotatedScans.extend(generateFourRotations(4,np.rot90(npScan,1,(1,0,0))))
    rotatedScans.extend(generateFourRotations(5,np.rot90(npScan,-1,(1,0,0))))

    assert(len(rotatedScans) == 24)


def mainTask():
    t1_start = perf_counter()  

    scans = []
    
    [processLine(line,scans) for line in open(f'{sys.path[0]}/input_small.txt', 'r')]
    print("Loaded {} scans with up with {} readings".format(len(scans), max([len(scan) for scan in scans])))

    npScans = convertToNp(scans)
    
    #each scanner could be in any of 24 different orientations
    
    allRotatedNpScans = []
    for scan in npScans:
        allRotatedNpScans.append(faceDifferentWayAndGenerateFourRotations(scan))



    #m = np.array([[1,2],[3,4]], int)
    #m.add([5,6])
    #print(m)
    #m = np.rot90(m)
    #print(m)
    #m = np.rot90(m, 2)
    #print(m)

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()