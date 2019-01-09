data = eval(input())
xeloE = 252.
yeloE = 331.
xntE = 520.
yntE = 634.
xeroE = 782.
yeroE = 321.
for i in range(len(data)):
    dx = data[i]['faceRectangle']['left']
    dy = data[i]['faceRectangle']['top']
    kx = 1000 / (data[i]['faceRectangle']['width'])
    ky = 1000 / (data[i]['faceRectangle']['height'])
    for j, k in data[i]['faceLandmarks'].items():
        data[i]['faceLandmarks'][j]['x'] = kx * (data[i]['faceLandmarks'][j]['x'] - dx)
        data[i]['faceLandmarks'][j]['y'] = ky * (data[i]['faceLandmarks'][j]['y'] - dy)
        if (j == 'eyeLeftOuter'):
            xelo = k['x']
            yelo = k['y']
        if (j == 'eyeRightOuter'):
            xero = k['x']
            yero = k['y']
        if (j == 'noseTip'):
            xnt = k['x']
            ynt = k['y']
    a2 = ((xeloE - xntE) * (xnt - xero) - (xntE - xeroE) * (xelo - xnt)) / ((xnt - xero) * (yelo - ynt) - (xelo - xnt) * (ynt - yero))
    a1 = ((xeloE - xntE) - a2 * (yelo - ynt)) / (xelo - xnt)
    a0 = xeloE - xelo * a1 - yelo * a2
    b2 = ((yeloE - yntE) * (xnt - xero) - (yntE - yeroE) * (xelo - xnt)) / ((xnt - xero) * (yelo - ynt) - (xelo - xnt) * (ynt - yero))
    b1 = ((yeloE - yntE) - b2 * (yelo - ynt)) / (xelo - xnt)
    b0 = yeloE - xelo * b1 - yelo * b2
    for j, k in data[i]['faceLandmarks'].items():
        xs = data[i]['faceLandmarks'][j]['x']
        ys = data[i]['faceLandmarks'][j]['y']
        x, y = xs, ys
        xs = a0 + x*a1 + y*a2
        ys = b0 + x*b1 + y*b2
        data[i]['faceLandmarks'][j]['x'] = xs
        data[i]['faceLandmarks'][j]['y'] = ys
delta = [0, 0, 0]
for i in range(3):
    for j, k in data[i]['faceLandmarks'].items():
        delta[i] += (data[i]['faceLandmarks'][j]['x'] - data[3]['faceLandmarks'][j]['x'])**2 + (data[i]['faceLandmarks'][j]['y'] - data[3]['faceLandmarks'][j]['y'])**2
print(delta.index(min(delta)))

