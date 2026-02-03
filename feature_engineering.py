import os
import numpy as np
from preprocessing import extract_face, get_embedding

def generate_embeddings(data_dir):
    X, y = [], []

    for label in os.listdir(data_dir):
        for img in os.listdir(os.path.join(data_dir, label)):
            face = extract_face(os.path.join(data_dir, label, img))
            emb = get_embedding(face)
            X.append(emb)
            y.append(label)

    return np.array(X), np.array(y)
