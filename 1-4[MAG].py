faces = eval(input())
fl = 'faceLandmarks'
fr = 'faceRectangle'

for i in range(len(faces)):
    dx, dy = faces[i][fl]['noseTip']['x'], faces[i][fl]['noseTip']['y']
    for j, k in faces[i][fl].items():
        faces[i][fl][j]['x'] -= dx
        faces[i][fl][j]['y'] -= dy

    xs, ys = faces[i][fl]['eyeLeftOuter']['x'], faces[i][fl]['eyeLeftOuter']['y']
    xe, ye = 0, (-1) * (xs**2 + ys**2)**0.5
    sina = (xs * ye - xe * ys) / (2 * ye**2)
    cosa = (xs * xe + ys * ye) / (2 * ye**2)
    for j, k in faces[i][fl].items():
        xc, yc = faces[i][fl][j]['x'], faces[i][fl][j]['y']
        faces[i][fl][j]['x'] = xc * cosa - yc * sina
        faces[i][fl][j]['y'] = xc * sina + yc * cosa

for i in range(len(faces)):
    dx, dy = 10000, 10000
    maxx, maxy = -10000, -10000
    for j, k in faces[i][fl].items():
        maxx = max(maxx, faces[i][fl][j]['x'])
        dx = min(dx, faces[i][fl][j]['x'])
        maxy = max(maxy, faces[i][fl][j]['y'])
        dy = min(dy, faces[i][fl][j]['y'])
    maxx -= dx
    maxy -= dy
    for j, k in faces[i][fl].items():
        faces[i][fl][j]['x'] -= dx
        faces[i][fl][j]['y'] -= dy
    coeffx = 1000 / maxx
    coeffy = 1000 / maxy
    for j, k in faces[i][fl].items():
        faces[i][fl][j]['x'] *= coeffx
        faces[i][fl][j]['y'] *= coeffy



delta = [0, 0, 0]
for i in range(len(faces) - 1):
    for j, k in faces[i][fl].items():
        x0, y0 = faces[i][fl][j]['x'], faces[i][fl][j]['y']
        x1, y1 = faces[3][fl][j]['x'], faces[3][fl][j]['y']
        delta[i] += ((x1 - x0)**2 + (y1 - y0)**2)**0.5
print(delta.index(min(delta)))
