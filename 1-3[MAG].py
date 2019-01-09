data = eval(input())
xeloE = 252.
yeloE = 331.
xntE = 520.
yntE = 634.
xeroE = 782.
yeroE = 321.
for i in range(len(data)):
    for j, k in data[i]['faceLandmarks'].items():
        if (j == 'eyeLeftOuter'):
            xelo = k['x']
            yelo = k['y']
        elif (j == 'eyeRightOuter'):
            xero = k['x']
            yero = k['y']
        elif (j == 'noseTip'):
            xnt = k['x']
            ynt = k['y']
        else:
            xs = k['x']
            ys = k['y']
a2 = ((xeloE - xntE) * (xnt - xero) - (xntE - xeroE) * (xelo - xnt)) / ((xnt - xero) * (yelo - ynt) - (xelo - xnt) * (ynt - yero))
a1 = ((xeloE - xntE) - a2 * (yelo - ynt)) / (xelo - xnt)
a0 = xeloE - xelo * a1 - yelo * a2
b2 = ((yeloE - yntE) * (xnt - xero) - (yntE - yeroE) * (xelo - xnt)) / ((xnt - xero) * (yelo - ynt) - (xelo - xnt) * (ynt - yero))
b1 = ((yeloE - yntE) - b2 * (yelo - ynt)) / (xelo - xnt)
b0 = yeloE - xelo * b1 - yelo * b2
x, y = xs, ys
xs, ys = a0 + x*a1 + y*a2, b0 + x*b1 + y*b2

print(int(xs), int(ys))
