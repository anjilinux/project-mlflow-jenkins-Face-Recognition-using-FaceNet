from sklearn.metrics import accuracy_score
import joblib

model = joblib.load("models/classifier.pkl")

def evaluate(X_test, y_test):
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
