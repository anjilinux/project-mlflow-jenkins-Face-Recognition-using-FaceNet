import joblib
import numpy as np

def test_model_load():
    model = joblib.load("models/classifier.pkl")
    assert model is not None

def test_prediction_shape():
    model = joblib.load("models/classifier.pkl")
    dummy = np.random.rand(1,512)
    pred = model.predict(dummy)
    assert len(pred) == 1
