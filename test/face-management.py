#!/usr/bin/env python
import cv2
import requests
import argparse
import numpy as np
import os
import dlib
from random import randrange
from imutils import face_utils
import imutils
import math


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
    parser.add_argument(
        '--add',
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '--rotate',
        type=str,
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

def GetPersonsIDs():
    req = GetList()
    if (str(req) == '<Response [200]>'):
        req = GetList().json()
        persons = dict()
        for person in req:
            persons[person['name']] = person['personId']
        return persons
    else:
        return 'The group does not exist'

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
        'returnFaceAttributes':'headPose',
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
        req = Find(videoName)
        if (req == 'Forbidden'):
            print('The same person already exists')
            return
        CreateGroup()
        currId = CreateFace(str(randrange(10000000000, 100000000000)))['personId']
        ids = AddFaces(videoFrames, currId)
        print('5 frames extracted')
        print('PersonId: ' + currId)
        print('FaceIds')
        print('=======')
        for id in ids:
            print(id)
        ChangeToNotTrained()


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

def ChangeUserData(personId, personName, newUserData):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
        'personId': personId,
    }
    data = {
        'name':personName,
        'userData':newUserData,
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons/' + personId
    req = requests.patch(
        baseUrl,
        params=params,
        headers=headers,
        json=data,
    )
    return req

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
    return req

def ChangeToTrained():
    persons = GetPersonsData()
    for person in persons:
        req = ChangeUserData(person['personId'], person['name'], 'trained')

def ChangeToNotTrained():
    persons = GetPersonsData()
    for person in persons:
        req = ChangeUserData(person['personId'], person['name'], 'nottrained')

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
    ChangeToTrained()
    return req

def GetGroupTrainedStatus():
    persons = GetPersonsData()
    if (persons == 'The group does not exist'):
        print(persons)
    else:
        f = 1
        for person in persons:
            if (person['userData'] != 'trained'):
                f = 0
        if (f == 0):
            return 'The group have not trained'
        else:
            return 'The group have already trained'

def Train():
    req = GetTrainingStatus()
    if (str(req) == '<Response [404]>'):
        req = req.json()
        if (req['error']['code'] == 'PersonGroupNotFound'):
            print('There is nothing to train')
            return None
        if (req['error']['code'] == 'PersonGroupNotTrained'):
            pass

    persons = GetPersonsData()
    if (len(persons) == 0):
        print('There is nothing to train')
        return None

    req = GetGroupTrainedStatus()
    if (req == 'The group does not exist'):
        print('There is nothing to train')
        return None
    elif (req == 'The group have not trained'):
        pass
    elif (req == 'The group have already trained'):
        print('Already trained')
        return None



    req = MakeTrainRequest()
    if (str(req) == '<Response [202]>'):
        print('Training successfully started')
        return None
    else:
        print('ERROR')
        return None


def List():
    persons = GetPersonsIDs()
    if (persons == 'The group does not exist'):
        print(persons)
    else:
        if (len(persons) == 0):
            print('No persons found')
        else:
            print('Persons IDs:')
            for i, j in persons.items():
                print(j)


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
    if (str(req) == '<Response [200]>'):
        print('Person deleted')
        ChangeToNotTrained()
    elif (str(req) == '<Response [404]>'):
        req = req.json()
        if (req['error']['code'] == 'PersonGroupNotFound'):
            print("The group does not exist")
        elif (req['error']['code'] == 'PersonNotFound'):
            print("The person does not exist")


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
    req = req.json()
    if (str(req).count("{'error': {'code': 'PersonGroupNotTrained', ")):
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


def MakeExtendedDetectRequest(buf):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId':True,
        'returnFaceLandmarks':True,
        'returnFaceAttributes':'headPose',
    }
    baseUrl = GetBaseUrl() + 'detect/'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data=buf,
    )
    return req

def ExtendedDetect(frame):
    image = GetOctetStream(frame)
    req = MakeExtendedDetectRequest(image)
    if (str(req) == '<Response [200]>'):
        req = req.json()
        if (len(req) == 1):
            return req[0]
        else:
            return None
    else:
        return None


def GetHeadPoseInformationMS(frame, result):
    req = ExtendedDetect(frame)
    if (req != None):
        result['yaw'] = req['faceAttributes']['headPose']['yaw']
        result['roll'] = req['faceAttributes']['headPose']['roll']

# https://www.pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup.jpg

def GetShape(frame):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    face_rects = detector(frame, 0)
    if (len(face_rects) == 0):
        return None
    shape = predictor(frame, face_rects[0])
    shape = face_utils.shape_to_np(shape)
    return shape

# https://github.com/lincolnhard/head-pose-estimation/blob/master/video_test_shape.py
# https://github.com/jerryhouuu/Face-Yaw-Roll-Pitch-from-Pose-Estimation-using-OpenCV/blob/master/pose_estimation.py


K = [6.5308391993466671e+002, 0.0, 3.1950000000000000e+002,
     0.0, 6.5308391993466671e+002, 2.3950000000000000e+002,
     0.0, 0.0, 1.0]
D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e+000]

cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                         [1.330353, 7.122144, 6.903745],
                         [-1.330353, 7.122144, 6.903745],
                         [-6.825897, 6.760612, 4.402142],
                         [5.311432, 5.485328, 3.987654],
                         [1.789930, 5.393625, 4.413414],
                         [-1.789930, 5.393625, 4.413414],
                         [-5.311432, 5.485328, 3.987654],
                         [2.005628, 1.409845, 6.165652],
                         [-2.005628, 1.409845, 6.165652],
                         [2.774015, -2.080775, 5.048531],
                         [-2.774015, -2.080775, 5.048531],
                         [0.000000, -3.116408, 6.097667],
                         [0.000000, -7.415691, 4.070434]])

reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]


def GetHeadPoseInformation(shape, result):
    if (shape is None):
        return None

    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])

    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)


    result['yaw'] = euler_angle[1, 0] * (-1)
    result['roll'] = euler_angle[2, 0]
#    1 0 : yaw right : positive
#    2 0 : roll right : negative


def Distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

lStart = 42
lEnd = 48
rStart = 36
rEnd = 42
mStart = 60
mEnd = 68
eyeThresh = 0.2        # 0.197
mouthTresh = 0.29

def GetClosedOpenedInformation(shape, result):
    leftEye = shape[lStart:lEnd]
    A = Distance(
        leftEye[1][0],
        leftEye[1][1],
        leftEye[5][0],
        leftEye[5][1],
    )
    B = Distance(
        leftEye[2][0],
        leftEye[2][1],
        leftEye[4][0],
        leftEye[4][1],
    )
    C = Distance(
        leftEye[0][0],
        leftEye[0][1],
        leftEye[3][0],
        leftEye[3][1],
    )
    ratioLeftEye = (A + B) / (2. * C)
    rightEye = shape[rStart:rEnd]
    A = Distance(
        rightEye[1][0],
        rightEye[1][1],
        rightEye[5][0],
        rightEye[5][1],
    )
    B = Distance(
        rightEye[2][0],
        rightEye[2][1],
        rightEye[4][0],
        rightEye[4][1],
    )
    C = Distance(
        rightEye[0][0],
        rightEye[0][1],
        rightEye[3][0],
        rightEye[3][1],
    )
    ratioRightEye = (A + B) / (2. * C)
    if (ratioLeftEye < eyeThresh):
        result['leftEye'] = 'closed'
    else:
        result['leftEye'] = 'opened'
    if (ratioRightEye < eyeThresh):
        result['rightEye'] = 'closed'
    else:
        result['rightEye'] = 'opened'
    # if (ratioRightEye < eyeThresh and ratioLeftEye < eyeThresh):
    #     result['leftEye'] = 'closed'
    #     result['rightEye'] = 'closed'
    # elif (ratioLeftEye < eyeThresh):
    #     result['leftEye'] = 'closed'
    #     result['rightEye'] = 'opened'
    # elif (ratioRightEye < eyeThresh):
    #     result['leftEye'] = 'opened'
    #     result['rightEye'] = 'closed'
    # else:
    #     result['leftEye'] = 'opened'
    #     result['rightEye'] = 'opened'

    # pythondlib face-management.py --add base.mp4 roll.mp4 yaw.mp4 mouth.mp4 eyes.mp4

    mouth = shape[mStart:mEnd]
    A = Distance(
        mouth[1][0],
        mouth[1][1],
        mouth[7][0],
        mouth[7][1],
    )
    B = Distance(
        mouth[2][0],
        mouth[2][1],
        mouth[6][0],
        mouth[6][1],
    )
    C = Distance(
        mouth[3][0],
        mouth[3][1],
        mouth[5][0],
        mouth[5][1],
    )
    D = Distance(
        mouth[0][0],
        mouth[0][1],
        mouth[4][0],
        mouth[4][1],
    )
    ratioMouth = (A + B + C) / (3. * D)
    if (ratioMouth < mouthTresh):
        result['mouth'] = 'closed'
    else:
        result['mouth'] = 'opened'

def GetInformation(frame, result, coun):
    if (coun == 0):
        GetHeadPoseInformationMS(frame, result)
        detect = dlib.get_frontal_face_detector()
        predict = dlib.shape_predictor('/opt/shape_predictor_68_face_landmarks.dat')
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subject = detect(gray, 0)
        if (len(subject) != 1):
            return
        subject = subject[0]
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        GetClosedOpenedInformation(shape, result)
    elif (1 <= coun <= 2):
        GetHeadPoseInformationMS(frame, result)
    else:
        detect = dlib.get_frontal_face_detector()
        predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subject = detect(gray, 0)
        if (len(subject) != 1):
            return
        subject = subject[0]
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        GetClosedOpenedInformation(shape, result)



def GetExtendedPersonData(frame, coun):
    # data = ExtendedDetect(frame)
    data = []
    if (data == None):
        return None
    else:
        result = dict()
        GetInformation(frame, result, coun)
        if (len(result) < 1):
            return None
        else:
            return result


def Add(sendingFrames, videoName):
    req = Find(videoName)
    if (req == 'Forbidden'):
        print('The same person already exists')
        return
    CreateGroup()
    currId = CreateFace(str(randrange(10000000000, 100000000000)))['personId']
    ids = AddFaces(sendingFrames, currId)
    print(len(sendingFrames), end='')
    print(' frames extracted')
    print('PersonId: ' + currId)
    print('FaceIds')
    print('=======')
    for id in ids:
        print(id)
    ChangeToNotTrained()

def SafetyAdd(videoNames):
    videosData = []
    videosChosen = []
    coun = 0
    for videoName in videoNames:
        vcap = cv2.VideoCapture(videoName)
        frames = []
        while (True):
            ret, frame = vcap.read()
            if (frame is None):
                break
            else:
                frames.append(frame)
        # print(vcap.get(cv2.CAP_PROP_POS_MSEC))    #duration
        # print(len(frames))                        #number of frames
        chosen = []
        if (coun == 0):
            for i in range(0, len(frames), len(frames) // 5):
                chosen.append(frames[i])
            coun += 1
        elif (coun == 3):
            for i in range(0, len(frames), len(frames) // 3):
                chosen.append(frames[i])
            coun += 1
        elif (coun == 4):
            for i in range(0, len(frames), len(frames) // 4):
                chosen.append(frames[i])
            coun += 1
        else:
            for i in range(0, len(frames), len(frames) // 15):
                chosen.append(frames[i])
            coun += 1

        data = []
        lastchosen = []
        for frame in chosen:
            currData = GetExtendedPersonData(frame, coun - 1)
            if (currData != None):
                data.append(currData)
                lastchosen.append(frame)
        videosData.append(data)
        videosChosen.append(lastchosen)


    finalSendingFrames = []
    for iii in range(len(videosChosen)):
        currVideo = videosChosen[iii]
        currVideoData = videosData[iii]
        if (iii == 0):
            # Base
            sendingFrames = []
            coun = 0
            for i in range(len(currVideo)):
                currFrame = currVideo[i]
                currFrameData = currVideoData[i]
                if (-5 < currFrameData['roll'] < 5 and -5 < currFrameData['yaw'] < 5 and currFrameData['mouth'] == 'closed' and currFrameData['leftEye'] == 'opened' and currFrameData['rightEye'] == 'opened'):
                    sendingFrames.append(currFrame)
                else:
                    coun += 1
            if (coun > 1):
                print('Base video does not follow requirements')
                return
            elif (len(sendingFrames) < 5):
                print('Base video does not follow requirements')
                return
            else:
                while (len(sendingFrames) > 5):
                    sendingFrames.pop()
                for fr in sendingFrames:
                    finalSendingFrames.append(fr)
        elif (iii == 1):
            # Roll
            sendingFrames = []
            flags = [0, 0, 0, 0, 0]
            for i in range(len(currVideo)):
                currFrame = currVideo[i]
                currFrameData = currVideoData[i]
                if (flags[0] == 0 and 25 < currFrameData['roll'] < 35):
                    flags[0] = 1
                    sendingFrames.append(currFrame)
                if (flags[1] == 0 and 10 < currFrameData['roll'] < 20):
                    flags[1] = 1
                    sendingFrames.append(currFrame)
                if (flags[2] == 0 and -5 < currFrameData['roll'] < 5):
                    flags[2] = 1
                    sendingFrames.append(currFrame)
                if (flags[3] == 0 and -20 < currFrameData['roll'] < -10):
                    flags[3] = 1
                    sendingFrames.append(currFrame)
                if (flags[4] == 0 and -35 < currFrameData['roll'] < -25):
                    flags[4] = 1
                    sendingFrames.append(currFrame)
            if (len(sendingFrames) < 5):
                print('Roll video does not follow requirements')
                return None
            else:
                for fr in sendingFrames:
                    finalSendingFrames.append(fr)
        elif (iii == 2):
            # Yaw
            sendingFrames = []
            flags = [0, 0, 0, 0, 0]
            for i in range(len(currVideo)):
                currFrame = currVideo[i]
                currFrameData = currVideoData[i]
                if (flags[0] == 0 and 15 < currFrameData['yaw'] < 25):
                    flags[0] = 1
                    sendingFrames.append(currFrame)
                if (flags[1] == 0 and 5 < currFrameData['yaw'] < 15):
                    flags[1] = 1
                    sendingFrames.append(currFrame)
                if (flags[2] == 0 and -5 < currFrameData['yaw'] < 5):
                    flags[2] = 1
                    sendingFrames.append(currFrame)
                if (flags[3] == 0 and -15 < currFrameData['yaw'] < -5):
                    flags[3] = 1
                    sendingFrames.append(currFrame)
                if (flags[4] == 0 and -25 < currFrameData['yaw'] < -15):
                    flags[4] = 1
                    sendingFrames.append(currFrame)
            if (len(sendingFrames) < 5):
                print('Yaw video does not follow requirements')
                return None
            else:
                for fr in sendingFrames:
                    finalSendingFrames.append(fr)
        elif (iii == 3):
            # Mouth
            sendingFrames = []
            for i in range(len(currVideo)):
                currFrame = currVideo[i]
                currFrameData = currVideoData[i]
                if (currFrameData['mouth'] == 'opened'):
                    sendingFrames.append(currFrame)
            if (len(sendingFrames) < 1):
                print('Video to detect open mouth does not follow requirements')
                return
            else:
                finalSendingFrames.append(sendingFrames[0])
        else:
            # Eyes
            flags = [0, 0]
            sendingFrames = []
            for i in range(len(currVideo)):
                currFrame = currVideo[i]
                currFrameData = currVideoData[i]
                if (flags[0] == 0 and currFrameData['leftEye'] == 'closed' and currFrameData['rightEye'] == 'opened'):
                    sendingFrames.append(currFrame)
                    flags[0] = 1
                if (flags[1] == 0 and currFrameData['rightEye'] == 'closed' and currFrameData['leftEye'] == 'opened'):
                    sendingFrames.append(currFrame)
                    flags[1] = 1
            if (len(sendingFrames) == 2):
                for fr in sendingFrames:
                    finalSendingFrames.append(fr)
            else:
                print('Video to detect closed eyes does not follow requirements')
                return
    Add(finalSendingFrames, videoNames[0])


# pythondlib face-management.py --add rollright.mp4 rollleft.mp4 yawright.mp4 yawleft.mp4 righteye.mp4 lefteye.mp4 mouth.mp4

# yaw right : negative
# yaw left : positive
# roll right : negative
# roll left : positive

def main():
    args = SetArgs()

    if (args['simple_add'] != None):
        SimpleAdd(args['simple_add'])
    if (args['add'] != None):
        SafetyAdd(args['add'])
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


# Mouth : Good
# Eyes : +- when we see on the both eyes and when our decision depend on another eyes
# yaw&roll : Good, but degrees lower, than in the task
