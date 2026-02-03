import mlflow
import joblib
from sklearn.svm import SVC
from feature_engineering import generate_embeddings

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("FaceNet-Recognition")

X, y = generate_embeddings("data/raw")

with mlflow.start_run():
    model = SVC(kernel="linear", probability=True)
    model.fit(X, y)

    joblib.dump(model, "models/classifier.pkl")
    mlflow.log_artifact("models/classifier.pkl")
