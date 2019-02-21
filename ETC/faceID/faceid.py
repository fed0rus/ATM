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










def main():
    privateKey = GetKey()
    groupId = GetGroupId()
    args = SetArgs()
    baseUrl = GetBaseUrl()
    if ('name' != None):
        print(args['name'])



if (__name__ == '__main__'):
    main()
