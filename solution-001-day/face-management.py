from argparse import ArgumentParser

from api import create_person, add_face, create_group_if_not_exists
from output_util import print_error
from video_detector import detect_all

parser = ArgumentParser(prog='Faces management')

parser.add_argument('--simple-add',
                    nargs=1,
                    metavar='VIDEO',
                    help='Adds 5 faces from video')

args = parser.parse_args()

if args.simple_add:
    video = args.simple_add[0]

    faces = detect_all(video)
    if faces is None:
        print_error('Video does not contain any face')

    create_group_if_not_exists()

    print('%d frames extracted' % len(faces))

    person_id = create_person('1')

    print('PersonId: %s' % person_id)
    print('FaceIds')
    print('=======')

    for face in faces:
        print(add_face(face, person_id))
