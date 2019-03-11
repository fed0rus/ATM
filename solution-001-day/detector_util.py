import cv2

from output_util import print_error


class FileLike:
    def __init__(self, image):
        self.image = image

    def read(self):
        return self.image


def image_to_jpeg(image):
    status, encoded_image = cv2.imencode('.jpeg', image)
    if not status:
        print_error('Failed to encode frame into jpeg')
    return encoded_image.tostring()
