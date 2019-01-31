import sys
from math import floor
def geometricMeanFilter():
    reductedRaster = copyRaster(masterRaster)
    for x in range(h):
        for y in range(w):
            for k in range(3):
                if 0 < x < h - 1 and 0 < y < w - 1:
                    geometricMean = (masterRaster[x][y][k] * masterRaster[x - 1][y][k] * masterRaster[x + 1][y][k] * masterRaster[x - 1][y - 1][k] * masterRaster[x][y - 1][k] * masterRaster[x + 1][y - 1][k] * masterRaster[x-1][y + 1][k] * masterRaster[x][y + 1][k] * masterRaster[x + 1][y + 1][k]) ** (1. / 9)
                    reductedRaster[x][y][k] = geometricMean
    return reductedRaster

def medianFilter():
    reductedRaster = copyRaster(masterRaster)
    for i in range(h):
        for j in range(w):
            for k in range(3):
                if 0 < i < h - 1 and 0 < j < w - 1:
                    median = [masterRaster[i][j][k], masterRaster[i][j-1][k], masterRaster[i][j+1][k], masterRaster[i-1][j][k], masterRaster[i-1][j-1][k], masterRaster[i-1][j+1][k], masterRaster[i+1][j][k], masterRaster[i+1][j-1][k], masterRaster[i+1][j+1][k]]
                    median.sort()
                    placed = median[4]
                    reductedRaster[i][j][k] = placed
    return reductedRaster

def arithmeticMean(reductedRaster):
    bleachedRaster = copyRaster(reductedRaster)
    for i in range(h):
        for j in range(w):
            bleachedRaster[i][j] = (reductedRaster[i][j][0] + reductedRaster[i][j][1] + reductedRaster[i][j][2]) / 3.
    return bleachedRaster

def weightedAverage(reductedRaster):
    bleachedRaster = copyRaster(reductedRaster)
    for i in range(h):
        for j in range(w):
            bleachedRaster[i][j] = reductedRaster[i][j][0] * 0.299 + reductedRaster[i][j][1] * 0.587 + reductedRaster[i][j][2] * 0.114
    return bleachedRaster

def nearestNeutral(reductedRaster):
    bleachedRaster = copyRaster(reductedRaster)
    for i in range(h):
        for j in range(w):
            bleachedRaster[i][j] = (max(reductedRaster[i][j][0], reductedRaster[i][j][1], reductedRaster[i][j][2]) + min(reductedRaster[i][j][0], reductedRaster[i][j][1], reductedRaster[i][j][2])) / 2.
    return bleachedRaster

def brightest(reductedRaster):
    bleachedRaster = copyRaster(reductedRaster)
    for i in range(h):
        for j in range(w):
            bleachedRaster[i][j] = max(reductedRaster[i][j][0], reductedRaster[i][j][1], reductedRaster[i][j][2])
    return bleachedRaster

def copyRaster(master):
    copied = [[[0, 0, 0] for j in range(w)] for i in range(h)]
    for i in range(h):
        for j in range(w):
            for k in range(3):
                copied[i][j][k] = master[i][j][k]
    return copied


# Initializing raster
global w, h
w, h = [int(k) for k in input().split()]
global masterRaster
masterRaster = [[[0 for i in range(3)] for j in range(w)] for k in range(h)]
line = [str(i) for i in input().split()][::-1]
for i in range(h):
    for j in range(w):
        pixel = line.pop()
        R = int(pixel[:2], 16)
        G = int(pixel[2:4], 16)
        B = int(pixel[4:], 16)
        masterRaster[i][j] = [R, G, B]
noiseReductionType = int(input())
bleachType = int(input())
# Shaking the raster
if noiseReductionType == 1: # Using the geometric mean filter
    reductedRaster = geometricMeanFilter()
    if bleachType == 1:
        bleachedRaster = arithmeticMean(reductedRaster)
    elif bleachType == 2:
        bleachedRaster = weightedAverage(reductedRaster)
    elif bleachType == 3:
        bleachedRaster = nearestNeutral(reductedRaster)
    else:
        bleachedRaster = brightest(reductedRaster)
else:
    reductedRaster = medianFilter()
    if bleachType == 1:
        bleachedRaster = arithmeticMean(reductedRaster)
    elif bleachType == 2:
        bleachedRaster = weightedAverage(reductedRaster)
    elif bleachType == 3:
        bleachedRaster = nearestNeutral(reductedRaster)
    else:
        bleachedRaster = brightest(reductedRaster)
# Choose the best
maxBrightness = -1
minBrightness = 256
for i in range(h):
    for j in range(w):
        maxBrightness = max(bleachedRaster[i][j], maxBrightness)
        minBrightness = min(bleachedRaster[i][j], minBrightness)
print(floor(minBrightness), floor(maxBrightness))
