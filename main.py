from fastapi import FastAPI, UploadFile
import cv2, numpy as np, joblib
from src.preprocessing import extract_face, get_embedding

app = FastAPI()
model = joblib.load("models/classifier.pkl")

@app.post("/predict")
async def predict(file: UploadFile):
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), 1)
    face = cv2.resize(img, (160,160))
    emb = get_embedding(face)
    pred = model.predict([emb])[0]
    return {"identity": pred}
