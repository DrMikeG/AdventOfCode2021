
import sys

#input_path = "C:\\Users\\gibbens\\Documents\\Arduino\\AdventOfCode2021\\20a\\tool_src\\input_small.txt"

algorithm, _, *image = open(f'{sys.path[0]}/input_small_hard.txt', 'r').read().split('\n')
algorithm = [int(ch == '#') for ch in algorithm]

def step(pixels, infinite_bit):
    # Find the minimum and maximum lit pixels coordinates in x and y
    min_i, max_i = min(p[0] for p in pixels), max(p[0] for p in pixels)
    min_j, max_j = min(p[1] for p in pixels), max(p[1] for p in pixels)

    enhanced_pixels = set()

    for i in range(min_i - 1, max_i + 2):
        for j in range(min_j - 1, max_j + 2):
            index = 0
            for di in range(i - 1, i + 2):
                for dj in range(j - 1, j + 2):
                    index = index << 1 | (
                        int((di, dj) in pixels)
                        if (min_i <= di <= max_i and min_j <= dj <= max_j)
                        else infinite_bit
                    )

            if (algorithm[index]):
                enhanced_pixels.add((i, j))

    return enhanced_pixels

def printGrid(pixels):
    
    min_i, max_i = min(p[0] for p in pixels), max(p[0] for p in pixels)
    min_j, max_j = min(p[1] for p in pixels), max(p[1] for p in pixels)
    for i in range(min_i, max_i+1):
        row = ""
        for j in range(min_j, max_j+1):
            if (i,j) in pixels:
                row += "#"
            else:
                row += "."
        print(row)
    print("")

# Gather the coordinates of every on pixel
pixels = set(
    (i, j)
    for i, row in enumerate(image)
    for j, ch in enumerate(row)
    if ch == '#'
)
printGrid(pixels)

max_iterations = 2


for i in range(max_iterations):
    pixels = step(pixels, i & 1 & algorithm[0])
    printGrid(pixels)

print(len(pixels))

