from config import get
import cognitive_face as cf
from detector_util import FileLike, image_to_jpeg
from output_util import print_error

KEY = get('faceapi.key')
cf.Key.set(KEY)

BASE_URL = get('faceapi.serviceUrl')
cf.BaseUrl.set(BASE_URL)

GROUP_ID = get('faceapi.groupId')


def create_group_if_not_exists():
    try:
        cf.person_group.create(GROUP_ID)
    except cf.CognitiveFaceException:
        pass


def detect(image):
    faces = cf.face.detect(FileLike(image_to_jpeg(image)), True, True, 'headPose')
    if len(faces) == 1:
        return faces[0]

    return None


def create_person(name, data=None):
    try:
        response = cf.person.create(GROUP_ID, name, data)
        return response['personId']
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print_error('The group does not exist')


def add_face(image, person_id):
    return cf.person.add_face(FileLike(image_to_jpeg(image)), GROUP_ID, person_id)['persistedFaceId']
