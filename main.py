from fastapi import FastAPI, UploadFile
import cv2
import numpy as np
import joblib
from preprocessing import extract_face, get_embedding

app = FastAPI()

model = None  # 👈 important


@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("models/classifier.pkl")
    print("✅ Model loaded")


@app.post("/predict")
async def predict(file: UploadFile):
    img = cv2.imdecode(
        np.frombuffer(await file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )

    face = cv2.resize(img, (160, 160))
    emb = get_embedding(face)

    pred = model.predict([emb])[0]
    return {"identity": pred}


@app.get("/health")
def health():
    return {"status": "ok"}
