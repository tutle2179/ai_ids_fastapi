from pydantic import BaseModel
print(" [schema.py] 이 파일이 FastAPI에 의해 로드됨")
class PacketData(BaseModel):
    duration: float
    protocol_type: float
    src_bytes: float
    dst_bytes: float
    flag: float
    land: float
    wrong_fragment: float
    urgent: float