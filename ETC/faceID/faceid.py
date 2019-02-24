import cv2
import requests
import argparse
import numpy as np
import os

def SetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name',
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '--create',
        action='store_true',
    )
    parser.add_argument(
        '--rw',
        action='store_true',
    )

    args = parser.parse_args()
    return vars(args)



def GetKey():
    with open('msfaceapi.json') as f:
        privateKey = eval(f.read())['key']
    return privateKey

def GetGroupId():
    with open('faceid.json') as f:
        groupId = eval(f.read())['groupId']
    return groupId

def GetBaseUrl():
    return 'https://eastasia.api.cognitive.microsoft.com/face/v1.0/'

def GetVideoFrames(videoName):
    vcap = cv2.VideoCapture(videoName)
    result = []
    frames = []
    while (True):
        ret, frame = vcap.read()
        if (frame is None):
            break
        else:
            frames.append(frame)
    for i in range(0, len(frames), len(frames) // 5):
        if (len(result) == 4):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetOctetStream(image):
    ret, buf = cv2.imencode('.jpg', image)
    return buf

def MakeDetectRequest(buf):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId':True,
        'returnFaceRectangle':False,
    }
    baseUrl = GetBaseUrl() + 'detect/'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data=buf.tobytes(),
    )
    return req.json()

def Detect(videoFrames):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        req = MakeRequest(image)
        if (len(req) != 0):
            result.append(req[0]['faceId'])
    return result

def CreateGroup():
    headers = {
        'Content-Type' : 'application/json',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    data = {
        'name' : 'myexample',
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId()
    req = requests.put(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    return req.json()


def main():
    args = SetArgs()
    if (args['name'] != None):
        personName = args['name'][0]
        videoName = args['name'][1]
        videoFrames = GetVideoFrames(videoName)
        ids = Detect(videoFrames)       ##IDS OF VIDEOGUY'S FACE
        if (len(ids) != 5):
            print('Video does not contain any face')
        else:
            #TODO: Face add
            pass


    if (args['create'] == True):
        req = CreateGroup()
        print(req)

    # WRITING
    if (args['rw'] == True):
        if (os.path.isfile('persons.txt')):
            f = open('persons.txt', 'r')
            data = f.read()
            f.close()
            f = open('persons.txt', 'w')
            f.write(data + 'lol2nd\n')
            f.close()
        else:
            f = open('persons.txt', 'w')
            data = f.write('lol\n')
            f.close()

if (__name__ == '__main__'):
    main()
