import requests
import cv2
import numpy as np
import os
from random import randrange


video_url = 'https://drive.google.com/uc?authuser=0&id=1ge9ldpf57E7u_8zA_-9DZ6a3JEuzzvDr&export=download' #DOWNLOAD LINK

vcap = cv2.VideoCapture(video_url)

frame = None
frameback = None
cnt = 0
frames = []

def delta(a, b, d):
    if (a + d >= b and a - d <= b):
        return True
    return False
k = 1
while (True):
    ret, frame = vcap.read()
    if frame is None:
        break
    if not (np.array_equal(frameback, None)):
        if k == 1:
            k = 0
        else:
            f = 1
            for i in range(len(frame) // 2, len(frame) // 2 + 10):
                if (f == 0):
                    break
                for j in range(len(frame[i]) // 2, len(frame[i]) // 2 + 10):
                    if (f == 0):
                        break
                    for k in range(len(frame[i][j])):
                        if not delta(frame[i][j][k], frameback[i][j][k], 10):
                            cnt += 1
                            f = 0
                            break
    frameback = frame.copy()
vcap.release()
print(cnt)
