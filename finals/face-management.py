#!/usr/bin/env python
import cv2
import requests
import argparse
import numpy as np
import os
import dlib
import web3
from random import randrange


def SetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--simple-add',
        type=str,
    )
    parser.add_argument(
        '--train',
        action='store_true',
    )
    parser.add_argument(
        '--list',
        action='store_true',
    )
    parser.add_argument(
        '--del',
        type=str,
    )
    parser.add_argument(
        '--deleteg',
        action='store_true',
    )

    args = parser.parse_args()
    return vars(args)


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

def GetPersons():
    req = GetList().json()
    persons = dict()
    for person in req:
        persons[person['name']] = person['personId']
    return persons

def CreateGroup():
    headers = {
        'Content-Type' : 'application/json',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    data = {
        'name' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId()
    req = requests.put(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    if (str(req) == '<Response [200]>'):
        return 'Success'
    else:
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
        if (len(result) == 4):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetOctetStream(image):
    ret, buf = cv2.imencode('.jpg', image)
    return buf.tobytes()

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
        data=buf,
    )
    return req.json()

def Detect(videoFrames):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        req = MakeDetectRequest(image)
        if (len(req) != 0):
            result.append(req[0]['faceId'])
    return result

def CreateFace(name):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
    }
    data = {
        'name':name,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    return req.json()

def MakeAddRequest(image, personId):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
        'Content-Type' : 'application/octet-stream',
    }
    params = {
        'personGroupId' : GetGroupId(),
        'personId' : personId,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons/' + personId + '/persistedFaces'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data = image,
    )
    return req.json()

def AddFaces(videoFrames, personId):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        currId = MakeAddRequest(image, personId)
        result.append(currId['persistedFaceId'])
    return result


def SimpleAdd(videoName):
    videoFrames = GetVideoFrames(videoName)
    ids = Detect(videoFrames)  ##IDS OF VIDEOGUY'S FACE
    if (len(ids) < 3):
        print('Video does not contain any face')
    else:
        CreateGroup()
        currId = CreateFace(str(randrange(10000000000, 100000000000)))['personId']
        ids = AddFaces(videoFrames, currId)
        print('5 frames extracted')
        print('PersonId: ' + currId)
        print('FaceIds')
        print('=======')
        for id in ids:
            print(id)


def MakeTrainRequest():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/train'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
    )
    if (str(req) == '<Response [202]>'):
        return 'Success'
    else:
        return req.json()

def Train():
    req = MakeTrainRequest()
    if (req == 'Success'):
        persons = GetPersons()
        coun = 0
        for i, j in persons.items():
            coun += 1
        print('Training task for ' + str(coun) + ' persons started')
    else:
        print('Something wrong')
        print(req)


def List():
    persons = GetPersons()
    for i, j in persons.items():
        print("Person's name is " + '"' + str(i) + '"' + "; person's id is " + '"' + j + '"')


def MakeDeletePersonRequest(personId):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
        'personId': personId,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons/' + personId
    req = requests.delete(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req

def DeletePerson(personId):
    req = MakeDeletePersonRequest(personId)
    print(str(req))
    if (str(req) == '<Response [200]>'):
        print('Person with id ' + '"' + personId + '"' + ' deleted')
    else:
        print('Something wrong')


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

def Identify(videoFrames):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    ids = Detect(videoFrames)
    data = {
        'faceIds' : ids,
        'personGroupId' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + '/identify'
    req = requests.post(
        baseUrl,
        headers=headers,
        json=data,
    )
    return req.json()

def Find(videoName):
    req = GetTrainingStatus()
    if (str(req) == "{'error': {'code': 'PersonGroupNotTrained', 'message': 'Person group not trained.'}}"):
        return 'Success'
    if (str(req).count("{'error': {'code': 'PersonGroupNotFound'") != 0):
        return 'Success'
    if (req.get('status') != None):
        if (req['status'] == 'succeeded'):
            videoFrames = GetVideoFrames(videoName)
            if (len(videoFrames) < 5):
                return 'Forbidden'
            else:
                result = Identify(videoFrames)
                candidates = dict()
                for id in result:
                    if (id != 'error'):
                        for candidate in id['candidates']:
                            if (candidates.get(candidate['personId']) == None):
                                candidates[candidate['personId']] = candidate['confidence']
                            else:
                                candidates[candidate['personId']] += candidate['confidence']
                    else:
                        candidates = dict()
                        break
                if (len(candidates) == 0):
                    return 'Success'
                else:
                    maxValue = 0
                    bestCandidate = ''
                    for i, j in candidates.items():
                        if (j > maxValue):
                            maxValue = j
                            bestCandidate = i
                    if (maxValue >= 2.5):
                        return 'Forbidden'
                    else:
                        return 'Success'
        else:
            return 'SystemProblem'
    else:
        return 'SystemProblem'

def SafetySimpleAdd(videoName):
    videoFrames = GetVideoFrames(videoName)
    ids = Detect(videoFrames)  ##IDS OF VIDEOGUY'S FACE
    if (len(ids) < 3):
        print('Video does not contain any face')
    else:
        req = Find(videoName)
        if (req == 'SystemProblem'):
            print('The system is not ready yet')
        if (req == 'Forbidden'):
            print('This person has already been added')
        if (req == 'Success'):
            CreateGroup()
            currId = CreateFace(str(randrange(10000000000, 100000000000)))['personId']
            ids = AddFaces(videoFrames, currId)
            print('5 frames extracted')
            print('PersonId: ' + currId)
            print('FaceIds')
            print('=======')
            for id in ids:
                print(id)


def DeleteGroup():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'presonGroupId' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId()
    req = requests.delete(
        baseUrl,
        params=params,
        headers=headers,
    )
    if (str(req) == '<Response [200]>'):
        return 'Success'
    else:
        return req


def main():
    args = SetArgs()

    if (args['simple_add'] != None):
        # SimpleAdd(args['simple_add'])
        SafetySimpleAdd(args['simple_add'])
    if (args['train'] == True):
        Train()
    if (args['list'] == True):
        List()
    if (args['del'] != None):
        DeletePerson(args['del'])
    if (args['deleteg'] == True):
        print(DeleteGroup())


if __name__ == '__main__':
    main()


