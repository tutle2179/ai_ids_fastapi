from fastapi import FastAPI
from app.schema import PacketData
from app.model import predict_intrusion

app = FastAPI(
    title="AI 기반 침입 탐지 API",
    description="트래픽 데이터를 분석하여 실시간으로 공격 여부를 예측합니다.",
    version="1.0"
)

@app.post("/predict")
async def predict(data: PacketData):
    result = predict_intrusion(data.features)
    return result