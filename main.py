from fastapi import FastAPI, UploadFile
import cv2
import numpy as np
import joblib
from preprocessing import get_embedding  # your preprocessing helper

app = FastAPI()

# Load trained model
model = joblib.load("models/classifier.pkl")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Face Recognition API is running"}

# Predict endpoint
@app.post("/predict")
async def predict(file: UploadFile):
    # Read uploaded image
    img_bytes = await file.read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Preprocess face
    face = cv2.resize(img, (160, 160))
    emb = get_embedding(face)

    # Predict identity
    pred = model.predict([emb])[0]

    return {"identity": pred}
