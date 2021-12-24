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


def mainTask():
    t1_start = perf_counter()  

    scans = []
    
    [processLine(line,scans) for line in open(f'{sys.path[0]}/input_small.txt', 'r')]
    print("Loaded {} scans with up with {} readings".format(len(scans), max([len(scan) for scan in scans])))

    m = np.array([[1,2],[3,4]], int)
    np.append(m,[5,6])

    a = np.array([1, 2, 3])
    newArray = np.append (a, [10, 11, 12])
    print(newArray)

    print(m)
    m = np.rot90(m)
    print(m)
    m = np.rot90(m, 2)
    print(m)

    t1_stop = perf_counter() 
    print("Elapsed time for main is {}".format(t1_stop-t1_start)) 

if __name__ == "__main__":
    mainTask()