import cv2
import imutils

from api import detect

WIDTH = 1000


def detect_all(video):
    faces_images = []

    cap = cv2.VideoCapture(video)
    success, frame = cap.read()
    count = 0

    while success:
        if count % 5 == 0:
            frame = imutils.resize(frame, width=WIDTH)

            face_api_response = detect(frame)

            if face_api_response is not None:
                faces_images.append(frame)

                if len(faces_images) == 5:
                    return faces_images

        count += 1
        success, frame = cap.read()

    return None
