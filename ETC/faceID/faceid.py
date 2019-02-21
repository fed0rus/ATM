import cv2
import requests
import argparse



def SetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name',
        nargs='+',
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
    for i in range(0, len(frames), len(frames) // 5):
        if (len(result) == 4):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetOctetStream(image):
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    #TODO: imencode's params
    ret, buf = cv2.imencode('', image)

def MakeRequest(func):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId':True,
    }
    baseUrl = GetBaseUrl() + func
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
        req = MakeRequest('detect/')
        result.append(req[0]['faceId'])
    return result




def main():
    # privateKey = GetKey()
    # groupId = GetGroupId()
    args = SetArgs()
    # baseUrl = GetBaseUrl()
    if ('name' != None):
        personName = args['name'][0]
        videoName = args['name'][1]
        videoFrames = GetVideoFrames(videoName)

        ids = Detect(videoFrames)
        print(ids)


if (__name__ == '__main__'):
    main()
