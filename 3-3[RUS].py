import math

# Reading parameters
epsilon = 3
height = float(input())
coords = {}
letters = ['A', 'B', 'C', 'D', 'E']
for i in letters:
    coords[i] = [float(k) for k in input().split()]

# Creating all possible vectors

vectors = {}
for i in letters:
    for j in letters:
        if i == j:
            continue
        vectorCoords = [coords[j][0] - coords[i][0], coords[j][1] - coords[i][1]]
        vectors[i + j] = vectorCoords

# Extracting base points

found = False
for i in vectors:
    for j in vectors:
        if i == j:
            continue
        if (abs(vectors[i][0] - vectors[j][0]) <= epsilon) and (abs(vectors[i][1] - vectors[j][1]) <= epsilon):
            basePoints = [i[0], i[1], j[0], j[1]]
            found = True
            break
    if found:
        break

# Guessing the H point

for k in letters:
    if k not in basePoints:
        heightCoords = [coords[k][0], coords[k][1]]
        break

# Calculating centroid of the base

#             ********** <- anotherPoint
#             *       **
#             *      * *
#             *     *  *
#             *    *   *
#             *   *    *
#             *  *     *
#             * *      *
# onePoint -> **********

onePoint = coords[basePoints[0]]
anotherPoint = coords[basePoints[3]]
centroidPoint = [(onePoint[0] + anotherPoint[0]) / 2, (onePoint[1] + anotherPoint[1]) / 2]

# Calculating distance between centroid and height

x = heightCoords[0] - centroidPoint[0]
y = heightCoords[1] - centroidPoint[1]
heightProjection = math.hypot(x, y)

# Calculating the angle

alpha = math.asin(float(heightProjection / height))

# Returning answer

print(alpha)

''' test
125
0 0
100 0
0 50
50 125
100 50
'''