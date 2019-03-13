import json
import requests
import cv2
import numpy as np
import os
from random import randrange



def GetKey():
    with open('faceapi.json') as f:
        privateKey = eval(f.read())['key']
    return privateKey

def GetGroupId():
    with open('faceapi.json') as f:
        groupId = eval(f.read())['groupId']
    return groupId

def GetBaseUrl():
    with open('faceapi.json') as f:
        serviceUrl = eval(f.read())['serviceUrl']
    return serviceUrl

def MakeDetectRequest(buf):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId': True,
        'returnFaceRectangle': False,
    }
    baseUrl = GetBaseUrl() + 'detect/'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data=buf,
    )
    return req.json()

def GetOctetStream(image):
    ret, buf = cv2.imencode('.jpg', image)
    return buf.tobytes()

def Detect(videoFrames):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        req = MakeDetectRequest(image)
        if (len(req) != 0):
            result.append(req[0]['faceId'])
    return result

def Identify(videoFrames):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    ids = Detect(videoFrames)
    data = {
        'faceIds': ids,
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + '/identify'
    req = requests.post(
        baseUrl,
        headers=headers,
        json=data,
    )
    return req.json()

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
    if (len(frames) < 5):
        return result
    for i in range(0, len(frames), len(frames) // 4):
        if (len(result) == 4 or len(frames) < 5):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetTrainingStatus():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/training'
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()

def GetList():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.get(
        baseUrl,
        headers=headers,
    )
    return req

def CreateFile(id):
    f = open('person.json', 'w')
    f.write('{"id": "' + id + '"}')
    f.close()

def DeleteFile():
    if (os.path.isfile('person.json')):
        os.remove('person.json')

def GetPersonsData():
    req = GetList()
    if (str(req) == '<Response [200]>'):
        req = GetList().json()
        persons = []
        for person in req:
            persons.append({
                'personId':person['personId'],
                'name':person['name'],
                'userData':person['userData']
            })
        return persons
    else:
        return 'The group does not exist'

def Find(videoName):
    videoFrames = GetVideoFrames(videoName)
    persons = GetPersonsData()
    if (len(videoFrames) < 5):
        print('The video does not follow requirements')
        DeleteFile()
        return None
    res = Detect(videoFrames)
    if (len(res) < 5):
        print('The video does not follow requirements')
        DeleteFile()
        return None
    if (persons == 'The group does not exist'):
        print('The service is not ready')
        DeleteFile()
        return None
    f = 1
    for person in persons:
        if (person['userData'] != 'trained'):
            f = 0
    if (f == 0):
        print('The service is not ready')
        DeleteFile()
        return None
    else:
        result = Identify(videoFrames)
        if (len(result) < 5):
            print('The video does not follow requirements')
            DeleteFile()
            return None
        candidates = dict()
        for frame in result:
            for candidate in frame['candidates']:
                currPersonId = candidate['personId']
                currConfidence = candidate['confidence']
                if (candidates.get(currPersonId) == None):
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] = currConfidence
                else:
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] += currConfidence
                    else:
                        candidates[currPersonId] = -100000
        if (len(candidates) == 0):
            print('The person was not found')
            DeleteFile()
            return None
        maxConfidence = 0
        bestCandidate = ''
        for candidate, confidence in candidates.items():
            if (confidence >= 2.5):
                if (maxConfidence < confidence):
                    bestCandidate = candidate
                    maxConfidence = confidence
        if (maxConfidence < 2.5):
            print('The person was not found')
            DeleteFile()
            return None
        else:
            print(bestCandidate + ' identified')
            CreateFile(bestCandidate)
            return None

def SetActions():
    f = open('actions.json', 'w')
    actions = [
        'Yaw',
        'Roll',
        'CloseLeftEye',
        'CloseRightEye',
        'OpenMouth',
    ]
    coun = randrange(3, 5)
    finalActions = []
    for i in range(coun):
        a = randrange(len(actions))
        currAction = actions[a]
        actions.remove(currAction)
        if currAction == 'Yaw':
            b = randrange(2)
            if (b == 0):
                currAction = 'YawLeft'
            else:
                currAction = 'YawRight'
        elif currAction == 'Roll':
            b = randrange(2)
            if (b == 0):
                currAction = 'RollLeft'
            else:
                currAction = 'RollRight'
        finalActions.append(currAction)
    di = dict()
    di['actions'] = []
    for action in finalActions:
        di['actions'].append(action)
    f.write(str(di))
    f.close()
