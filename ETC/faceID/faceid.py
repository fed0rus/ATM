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
    parser.add_argument(
        '--deleteg',
        action='store_true',
    )
    parser.add_argument(
        '--del',
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '--list',
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
        if (len(result) == 4 or len(frames) < 5):
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
    return req.json()

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
    return req.json()

def CreateFace(name):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    data = {
        'name' : name,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    return req.json()

def DeleteFace(name):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),

    }
    data = {
        'name': name,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )

def GetFace(personId):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
        'personId' : personId,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons/' + personId
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()



# WTF? IT IS NOT SUPPORTED??
# But it is list's information without persons' information now
def GetList():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()


#TODO
def AddFaces():
    return None



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
            persons = dict()
            if (os.path.isfile('persons.txt') == False):
                currId = CreateFace(personName)
                persons[personName] = currId['personId']
                AddFaces()
                f = open('persons.txt', 'w')
                f.write(str(persons))
                f.close()
            else:
                f = open('persons.txt', 'r')
                persons = eval(f.read())
                f.close()
                if (persons.get(personName) == None):
                    currId = CreateFace(personName)
                    persons[personName] = currId['personId']
                    AddFaces()
                else:
                    AddFaces()
                f = open('persons.txt', 'w')
                f.write(str(persons))
                f.close()
    if (args['del'] != None):
        personName = args['del'][0]
        persons = dict()
        if (os.path.isfile('persons.txt') == False):
            f = open('persons.txt', 'w')
            f.write(str(persons))
            f.close()
            print('No person with name "' + str(personName) + '"')
        else:
            f = open('persons.txt', 'r')
            persons = eval(f.read())
            f.close()
            if (persons.get(personName) == None):
                print('No person with name "' + str(personName) + '"')
            else:
                DeleteFace(persons[personName])
                print('Person with id ' + str(persons[personName]) + ' deleted')
                persons.pop(personName, None)
            f = open('persons.txt', 'w')
            f.write(str(persons))
            f.close()
    if (args['list'] == True):
        req = GetList()
        print(req)


    if (args['create'] == True):
        req = CreateGroup()
        print(req)
    if (args['deleteg'] == True):
        req = DeleteGroup()
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
