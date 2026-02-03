from fastapi import FastAPI, UploadFile, HTTPException
import cv2
import numpy as np
import joblib
import os

from preprocessing import extract_face, get_embedding

app = FastAPI(title="Face Recognition API")

MODEL_PATH = "models/classifier.pkl"
model = None


@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("❌ Model file not found")

    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")

    img_bytes = await file.read()
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    try:
        face = extract_face(img)
        emb = get_embedding(face)
        pred = model.predict([emb])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"identity": pred}
