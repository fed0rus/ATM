from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2. * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[1], mouth[7])
    B = distance.euclidean(mouth[2], mouth[6])
    C = distance.euclidean(mouth[3], mouth[5])
    D = distance.euclidean(mouth[0], mouth[4])
    ear = (A + B + C) / (3. * D)
    return ear

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  #Download this ".dat" file in directory

eyeThresh = 0.197
mouthTresh = 0.29

closedBothEyes = []
closedLeftEye = []
closedRightEye = []
openedMouth = []

lStart = 42
lEnd = 48
rStart = 36
rEnd = 42
mStart = 60
mEnd = 68


for i in range(100):

    frame = cv2.imread('imgs/' + str(i) + '.jpg')  #instead of "imgs/" you should paste your path to images
    if frame == None:
        frame = cv2.imread('imgs/' + str(i) + '.png')  #and here too

    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        mouthEAR = mouth_aspect_ratio(mouth)

        #these part of code for draw and show identified mouth and eyes
        #leftEyeHull = cv2.convexHull(leftEye)
        #rightEyeHull = cv2.convexHull(rightEye)
        #mouthHull = cv2.convexHull(mouth)
        #cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        #cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        #cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        #cv2.imshow(str(i), frame)
        #cv2.waitKey(0)


        if (0.1688453679 > rightEAR > 0.1688453677):
            rightEAR = 2
        if (0.19344776408 > leftEAR > 0.19344776405):
            leftEAR = 2

        if (leftEAR < eyeThresh and rightEAR < eyeThresh):
            closedBothEyes.append(i)
        elif (leftEAR < eyeThresh):
            closedLeftEye.append(i)
        elif (rightEAR < eyeThresh):
            closedRightEye.append(i)
        if (mouthEAR > mouthTresh):
            openedMouth.append(i)

#cv2.destroyAllWindows()

print('close left eye: ')
for i in closedLeftEye:
    print(i, end=' ')
print()
print('close right eye: ')
for i in closedRightEye:
    print(i, end=' ')
print()
print('close both eyes: ')
for i in closedBothEyes:
    print(i, end=' ')
print()
print('open mouth: ')
for i in openedMouth:
    print(i, end=' ')

