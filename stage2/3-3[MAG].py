from math import asin
h = int(input())
x, y = [], []
for i in range(5):
    a, b = [int(i) for i in input().split()]
    x.append(a)
    y.append(b)
x1, x2, y1, y2 = sorted(x)[0], sorted(x)[1], y[x.index(sorted(x)[0])], y[x.index(sorted(x)[1])]
if (y1 > y2):
    x1, x2, y1, y2 = x2, x1, y2, y1
x3, x4, y3, y4 = sorted(x)[-1], sorted(x)[-2], y[x.index(sorted(x)[-1])], y[x.index(sorted(x)[-2])]
if (y3 < y4):
    x3, x4, y3, y4 = x4, x3, y4, y3
x.remove(x1)
x.remove(x2)
x.remove(x3)
x.remove(x4)
y.remove(y1)
y.remove(y2)
y.remove(y3)
y.remove(y4)

x5, y5 = x[0], y[0]

A1 = y1 - y3
B1 = x3 - x1
C1 = x1 * y3 - x3 * y1
A2 = y2 - y4
B2 = x4 - x2
C2 = x2 * y4 - x4 * y2
xp = (B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1)
yp = (C1 * A2 - C2 * A1) / (A1 * B2 - A2 * B1)
l1 = ((xp - x5)**2 + (yp - y5)**2)**0.5
print(asin(l1 / h))
