import os
import joblib
import mlflow
from sklearn.svm import SVC
from feature_engineering import generate_embeddings


def main():
    os.makedirs("models", exist_ok=True)

    mlflow.set_tracking_uri("http://localhost:5555")
    mlflow.set_experiment("FaceNet-Recognition")

    X, y = generate_embeddings("data/raw")

    with mlflow.start_run():
        model = SVC(kernel="linear", probability=True)
        model.fit(X, y)

        model_path = "models/classifier.pkl"
        joblib.dump(model, model_path)

        mlflow.log_artifact(model_path)
        mlflow.log_param("kernel", "linear")
        mlflow.log_metric("samples", len(X))


if __name__ == "__main__":
    main()
