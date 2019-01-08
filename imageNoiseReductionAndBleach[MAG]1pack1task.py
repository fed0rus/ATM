w, h = [int(i) for i in input().split()]
image = [[[0, 0, 0] for i in range(w)] for j in range(h)]
inp = [x for x in input().split()]
for i in range(h):
    for j in range(w):
        image[i][j][0] = int(inp[w * i + j][:2], 16)
        image[i][j][1] = int(inp[w * i + j][2:4], 16)
        image[i][j][2] = int(inp[w * i + j][4:], 16)


"""NOISE"""
def geom_average_filter(image):
    global w, h
    newimage = [[[0, 0, 0] for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j][0] = image[i][j][0]
            newimage[i][j][1] = image[i][j][1]
            newimage[i][j][2] = image[i][j][2]
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            multR = 1
            multG = 1
            multB = 1
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    multR *= image[i + x][j + y][0]
                    multG *= image[i + x][j + y][1]
                    multB *= image[i + x][j + y][2]
            newimage[i][j][0] = multR ** (1 / 9)
            newimage[i][j][1] = multG ** (1 / 9)
            newimage[i][j][2] = multB ** (1 / 9)
    return newimage

def median_filter(image):
    global w, h
    newimage = [[[0, 0, 0] for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j][0] = image[i][j][0]
            newimage[i][j][1] = image[i][j][1]
            newimage[i][j][2] = image[i][j][2]
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            arrR = []
            arrG = []
            arrB = []
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    arrR.append(image[i + x][j + y][0])
                    arrG.append(image[i + x][j + y][1])
                    arrB.append(image[i + x][j + y][2])
            arrR.sort()
            arrG.sort()
            arrB.sort()
            newimage[i][j][0] = arrR[4]
            newimage[i][j][1] = arrG[4]
            newimage[i][j][2] = arrB[4]
    return newimage
f = int(input())
if (f == 1):
    image = geom_average_filter(image)
else:
    image = median_filter(image)
"""NOISE"""


"""GREYING"""
def arithmetical_average(image):
    global h, w
    newimage = [[0 for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j] = (image[i][j][0] + image[i][j][1] + image[i][j][2]) / 3
    return newimage

def weight_average(image):
    global h, w
    newimage = [[0 for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j] = 0.299 * image[i][j][0] + 0.587 * image[i][j][1] + 0.114 * image[i][j][2]
    return newimage

def nearest_point(image):
    global h, w
    newimage = [[0 for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j] = (max(image[i][j][0], image[i][j][1], image[i][j][2]) + min(image[i][j][0], image[i][j][1], image[i][j][2])) / 2
    return newimage

def value_of_brightness(image):
    global h, w
    newimage = [[0 for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j] = max(image[i][j][0], image[i][j][1], image[i][j][2])
    return newimage


d = int(input())
if (d == 1):
    image = arithmetical_average(image)
elif (d == 2):
    image = weight_average(image)
elif (d == 3):
    image = nearest_point(image)
else:
    image = value_of_brightness(image)
"""GREYING"""

ma = image[0][0]
mi = image[0][0]
for i in range(h):
    for j in range(w):
        ma = max(ma, image[i][j])
        mi = min(mi, image[i][j])
print(int(mi), int(ma))