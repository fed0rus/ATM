#!/usr/bin/env python
import cv2
import requests
import argparse
import numpy as np
import os


def SetArgs():
    parser = argparse.ArgumentParser()

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
    return 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'











def main():
    args = SetArgs()

if __name__ == '__main__':
    main()
