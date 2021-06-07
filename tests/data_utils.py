import os

BASE_PATH = '{0}/test_data'.format(
    os.path.dirname(os.path.realpath(__file__)))


def get_emotion_data(emotion):
    data = []
    for i in range(1, 4):
        data.append(f"{BASE_PATH}/fer/{emotion}/{i}.jpg")
    return data
