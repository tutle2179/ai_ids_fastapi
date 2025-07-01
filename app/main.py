from fastapi import FastAPI
from app.schema import PacketData
from app.model import predict_intrusion
import inspect
import app.schema

print(" PacketData 클래스 실제 경로:", inspect.getfile(app.schema))
print(" PacketData 클래스 내용:", app.schema.PacketData.schema())

app = FastAPI(
    title="AI 기반 침입 탐지 API",
    description="트래픽 데이터를 분석하여 실시간으로 공격 여부를 예측합니다.",
    version="1.0"
)

@app.post("/predict")
async def predict(data: PacketData):
    result = predict_intrusion(data.dict())  # ← dict로 변환해서 넘겨줘야 model.py에서 키로 접근 가능
    return result