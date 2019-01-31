w, h = [int(i) for i in input().split()]
image = [[[0, 0, 0] for i in range(w)] for j in range(h)]

for i in range(h):
    inp = [x for x in input().split()]
    for j in range(w):
        image[i][j][0] = int(inp[j][:2], 16)
        image[i][j][1] = int(inp[j][2:4], 16)
        image[i][j][2] = int(inp[j][4:], 16)
"""NOISE"""
def geom_average_filter(image):
    global w, h
    newimage = [[[0, 0, 0] for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j][0] = image[i][j][0]
            newimage[i][j][1] = image[i][j][1]
            newimage[i][j][2] = image[i][j][2]
    for i in range(3, h - 3):
        for j in range(3, w - 3):
            multR = 1
            multG = 1
            multB = 1
            for x in range(-3, 4, 1):
                for y in range(-3, 4, 1):
                    multR *= image[i + x][j + y][0]
                    multG *= image[i + x][j + y][1]
                    multB *= image[i + x][j + y][2]
            newimage[i][j][0] = multR ** (1 / 49)
            newimage[i][j][1] = multG ** (1 / 49)
            newimage[i][j][2] = multB ** (1 / 49)
    return newimage

def median_filter(image):
    global w, h
    newimage = [[[0, 0, 0] for i in range(w)] for j in range(h)]
    for i in range(h):
        for j in range(w):
            newimage[i][j][0] = image[i][j][0]
            newimage[i][j][1] = image[i][j][1]
            newimage[i][j][2] = image[i][j][2]
    for i in range(3, h - 3):
        for j in range(3, w - 3):
            arrR = []
            arrG = []
            arrB = []
            for x in range(-3, 4, 1):
                for y in range(-3, 4, 1):
                    arrR.append(image[i + x][j + y][0])
                    arrG.append(image[i + x][j + y][1])
                    arrB.append(image[i + x][j + y][2])
            arrR.sort()
            arrG.sort()
            arrB.sort()
            newimage[i][j][0] = arrR[24]
            newimage[i][j][1] = arrG[24]
            newimage[i][j][2] = arrB[24]
    return newimage
f = 2
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


d = 1
if (d == 1):
    image = arithmetical_average(image)
elif (d == 2):
    image = weight_average(image)
elif (d == 3):
    image = nearest_point(image)
else:
    image = value_of_brightness(image)
"""GREYING"""

imageOfVectors = [[[0, 0] for i in range(w - 2)] for j in range(h - 2)]
for i in range(1, h - 1):
    for j in range(1, w - 1):
        imageOfVectors[i - 1][j - 1][0] = image[i][j + 1] - image[i][j - 1]
        imageOfVectors[i - 1][j - 1][1] = image[i + 1][j] - image[i - 1][j]
s = [[0 for i in range(len(imageOfVectors))] for j in range(len(imageOfVectors[0]))]

magnitude = [[0 for i in range(h - 2)] for j in range(w - 2)]
angle = [[0 for i in range(h - 2)] for j in range(w - 2)]
for i in range(h - 2):
    for j in range(w - 2):
        magnitude[i][j] = (imageOfVectors[i][j][0]**2 + imageOfVectors[i][j][1]**2)**(0.5)
        if (imageOfVectors[i][j][0] > 3 or imageOfVectors[i][j][0] < -3):
            angle[i][j] = (imageOfVectors[i][j][1] / imageOfVectors[i][j][0])
        else:
            if (-3 < imageOfVectors[i][j][1] < 3):
                angle[i][j] = None
            else:
                angle[i][j] = 2


for i in range(len(imageOfVectors)):
    for j in range(len(imageOfVectors[i])):
        if (angle[i][j] == None or magnitude[i][j] < 11):
            s[i][j] = '0'
        elif ((-1) < angle[i][j] < 1):
            s[i][j] = '-'
        else:
            s[i][j] = '|'

sch1 = 0
sch2 = 0

for i in range(len(s) - 1):
    for j in range(len(s[i]) - 1):
        if ((s[i][j] == '0' and s[i][j + 1] == '-') or (s[i][j] == '-' and s[i][j + 1] == '0')):
            sch1 += 1
        elif ((s[i][j] == '0' and s[i + 1][j] == '|') or (s[i][j] == '|' and s[i + 1][j] == '0')):
            sch2 += 1
            
            

if (sch1==0 and sch2==0):
    print(0)
elif (sch2 == 0):
    print(2)
elif (sch1 == 0):
    print(1)
elif (sch1 / (h * w) >= 0.01 and sch1 / (h * w) <= 0.046 or sch1/sch2>2):
    print(1)
elif (sch2 / (h * w) >= 0.01 and sch2 / (h * w) <= 0.046 or sch2/sch1>2):
    print(2)
else:
    print(0)
