from pydantic import BaseModel
from typing import List

class PacketData(BaseModel):
    features: List[float]  # 총 41개의 숫자 값