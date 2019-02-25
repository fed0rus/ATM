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
    parser.add_argument(
        '--train',
        action='store_true',
    )
    parser.add_argument(
        '--identify',
        type=str,
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
    for i in range(0, len(frames), len(frames) // 4):
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
    if (str(req) == '<Response [200]>'):
        return 'Success'
    else:
        return req

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

def Train():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/train'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
    )

def GetTrainingStatus():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId' : GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/training'
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()

def GetVideoFramesForId(videoName):
    vcap = cv2.VideoCapture(videoName)
    result = []
    frames = []
    while (True):
        ret, frame = vcap.read()
        if (frame is None):
            break
        else:
            frames.append(frame)
    for i in range(0, len(frames), len(frames) // 2):
        if (len(result) == 2):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

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


def main():
    args = SetArgs()
    # create names-id storage (if it isn't existing)
    if (os.path.isfile('persons.txt') == False):
        f = open('persons.txt', 'w')
        f.write('{}')
        f.close()

    if (args['name'] != None):
        personName = args['name'][0]
        videoName = args['name'][1]
        videoFrames = GetVideoFrames(videoName)
        ids = Detect(videoFrames)       ##IDS OF VIDEOGUY'S FACE
        if (len(ids) != 5):
            print('Video does not contain any face')
        else:
            persons = dict()
            f = open('persons.txt', 'r')
            persons = eval(f.read())
            f.close()
            if (persons.get(personName) == None):
                currId = CreateFace(personName)
                persons[personName] = currId['personId']
                ids = AddFaces(videoFrames, persons[personName])
                print('5 frames extracted')
                print('PersonId: ' + persons[personName])
                print('FaceIds')
                print('=======')
                for id in ids:
                    print(id)
            else:
                ids = AddFaces(videoFrames, persons[personName])
                print('5 frames extracted')
                print('PersonId: ' + persons[personName])
                print('FaceIds')
                print('=======')
                for id in ids:
                    print(id)
            f = open('persons.txt', 'w')
            f.write(str(persons))
            f.close()
    if (args['del'] != None):
        personName = args['del'][0]
        persons = dict()
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
    if (args['train'] == True):
        req = Train()
        f = open('persons.txt', 'r')
        persons = eval(f.read())
        f.close()
        coun = 0
        for i, j in persons.items():
            coun += 1
        print('Training task for ' + str(coun) + ' persons started')
        f = open('persons.txt', 'w')
        f.write(str(persons))
        f.close()
    if (args['identify'] != None):
        req = GetTrainingStatus()
        if (req['status'] == 'succeeded'):
            videoName = args['identify']
            videoFrames = GetVideoFramesForId(videoName)
            result = Identify(videoFrames)
            candidates = dict()
            for id in result:
                for candidate in id['candidates']:
                    if candidate['confidence'] < 0.5:
                        if (candidates.get(candidate['personId']) != None):
                            candidates.pop(candidate['personId'], None)
                    else:
                        if (candidates.get(candidate['personId']) == None):
                            candidates[candidate['personId']] = candidate['confidence']
                        else:
                            candidates[candidate['personId']] += candidate['confidence']
            if (len(candidates) == 0):
                print('The person cannot be identified')
            else:
                maxValue = 0
                bestCandidate = ''
                for i, j in candidates.items():
                    if (j > maxValue):
                        maxValue = j
                        bestCandidate = i
                candidateName = ''
                f = open('persons.txt', 'r')
                persons = eval(f.read())
                f.close()
                for person, id in persons.items():
                    if (id == bestCandidate):
                        candidateName = person
                print('The person is "' + candidateName + '"')
                f = open('persons.txt', 'w')
                f.write(str(persons))
                f.close()
        else:
            print('The system is not ready yet')

    ###################################
    # methods only for me
    if (args['create'] == True):
        req = CreateGroup()
        print(req)
    if (args['deleteg'] == True):
        req = DeleteGroup()
        f = open('persons.txt', 'w')
        f.write('{}')
        f.close()
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
    ###################################

if (__name__ == '__main__'):
    main()
