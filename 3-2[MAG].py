import requests
import cv2
import numpy as np
import os
from random import randrange


video_url = 'https://drive.google.com/uc?id=1uoNgKON6DXGtZABZGgukStOvBSNGOQxM&export=download'

vcap = cv2.VideoCapture(video_url)

def delta(a, b, d):
    if (a + d >= b and a - d <= b):
        return True
    return False

frame = None
k = 1
faces = []
while (True):
    ret, frame = vcap.read()
    if frame is None:
        break
    if k == 1:
        k = 0
    else:
        was = 0
        for ii in range(len(faces)):
            f = 1
            for i in range(0, len(frame), len(frame) // 20):
                if (f == 0):
                    break
                for j in range(0, len(frame[i]), len(frame[i]) // 20):
                    if (f == 0):
                        break
                    for k in range(len(frame[i][j])):
                        if not delta(faces[ii][i][j][k], frame[i][j][k], 20):
                            f = 0
            if (f == 1):
                was = 1
        if (was == 0):
            faces.append(frame)

print(len(faces))
