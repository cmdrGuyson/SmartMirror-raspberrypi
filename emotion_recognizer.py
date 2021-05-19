import cv2.cv2 as cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# Location of model
model_location = '{0}\\models\\model.h5'.format(
    os.path.dirname(os.path.realpath(__file__)))

model = load_model(model_location)


class EmotionRecognizer:

    def __init__(self):
        self.expressions = ["happy", "sad", "neutral"]

    @staticmethod
    def preprocess(face):
        """
        Pre-process given face image
        """

        img = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (48, 48))

        # Convert to numpy array
        img = np.expand_dims(img, axis=-1)
        data = np.asarray(img, dtype="int32")

        # Normalize and expand dimensions
        img = data / 255.
        img = np.expand_dims(img, axis=2)
        return np.expand_dims(img, axis=0)

    def identify_emotion(self, face):
        img = EmotionRecognizer.preprocess(face)
        predicted_probability = model.predict(img)
        print(predicted_probability)
        predicted_label = np.argmax(predicted_probability[0])
        return self.expressions[predicted_label]
