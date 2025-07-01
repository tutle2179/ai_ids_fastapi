import joblib
import numpy as np
import os


# 모델 및 스케일러 전역에서 1번만 로딩
model_path = os.path.join("models", "ids_model.pkl")
scaler_path = os.path.join("models", "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

print("[DEBUG]  모델 로딩됨: ", model)
print("[DEBUG]  스케일러가 기대하는 feature 수:", scaler.n_features_in_)

def predict_intrusion(packet: dict) -> dict:
    try:
        feature_order = [
            "duration", "protocol_type", "src_bytes", "dst_bytes",
            "flag", "land", "wrong_fragment", "urgent"
        ]
        values = [packet[feature] for feature in feature_order]

        print("[DEBUG]  입력값:", values)

        array = np.array(values).reshape(1, -1)
        print("[DEBUG]  array:", array)

        scaled = scaler.transform(array)
        print("[DEBUG]  scaled:", scaled)

        prediction = model.predict(scaled)[0]
        proba = model.predict_proba(scaled)[0].max()

        print("[DEBUG]  예측:", prediction)
        print("[DEBUG]  확률:", proba)

        result = "normal" if prediction == 0 else "attack"
        return {
            "prediction": result,
            "confidence": round(float(proba), 4)
        }

    except Exception as e:
        print("[ model.py] 예측 중 오류 발생:", e)
        import traceback
        traceback.print_exc()
        return {
            "prediction": None,
            "confidence": 0.0
        }
