import joblib
import numpy as np
import os

# 모델 및 스케일러 불러오기
model_path = os.path.join("models", "ids_model.pkl")
scaler_path = os.path.join("models", "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

def predict_intrusion(features: list) -> dict:
    features_array = np.array(features).reshape(1, -1)
    scaled = scaler.transform(features_array)
    prediction = model.predict(scaled)[0]
    proba = model.predict_proba(scaled)[0].max()
    
    result = "normal" if prediction == 0 else "attack"
    return {
        "result": result,
        "confidence": round(float(proba), 4)
    }
