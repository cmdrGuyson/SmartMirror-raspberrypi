import os

BASE_PATH = '{0}/test_data'.format(
    os.path.dirname(os.path.realpath(__file__)))


def get_emotion_data(emotion):
    data = []
    for i in range(1, 4):
        data.append(f"{BASE_PATH}/fer/{emotion}/{i}.jpg")
    return data


def get_face_recognition_data(user):
    data = []
    for i in range(1, 4):
        data.append(f"{BASE_PATH}/fr/{user}/{i}.jpg")
    return data


def get_face_recognition_setup_data(user):
    data = []
    for i in range(1, 11):
        data.append(f"{BASE_PATH}/setup_fr/{user}/{i}.jpg")
    return data
