import cv2
import numpy as np
from keras_facenet import FaceNet

embedder = FaceNet()

def extract_face(image_path, size=(160,160)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(img, size)
    return face

def get_embedding(face):
    face = np.expand_dims(face, axis=0)
    return embedder.embeddings(face)[0]
