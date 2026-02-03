import os
import numpy as np
from preprocessing import extract_face, get_embedding


def generate_embeddings(data_dir):
    X, y = [], []

    for label in os.listdir(data_dir):
        label_path = os.path.join(data_dir, label)

        if not os.path.isdir(label_path):
            continue

        for img in os.listdir(label_path):
            if not img.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            img_path = os.path.join(label_path, img)
            face = extract_face(img_path)
            emb = get_embedding(face)

            X.append(emb)
            y.append(label)

    return np.array(X), np.array(y)
