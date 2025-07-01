import scapy.all as scapy
import requests
import json
import csv
import os
from datetime import datetime

API_URL = "http://localhost:8010/predict"
LOG_FILE = "packet_logs.csv"
print("🔗 요청 전송 대상 URL:", API_URL)

# 로그 파일 없으면 헤더 생성
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "duration", "protocol_type", "src_bytes",
            "dst_bytes", "flag", "land", "wrong_fragment", "urgent", "prediction"
        ])

# 패킷에서 특징 추출
def extract_features(packet):
    if packet.haslayer(scapy.IP):
        ip_layer = packet[scapy.IP]
        proto = ip_layer.proto
        length = len(packet)

        data = [
            0,         # duration
            proto,     # protocol_type
            length,    # src_bytes
            0,         # dst_bytes
            0,         # flag
            0,         # land
            0,         # wrong_fragment
            0          # urgent
        ]
        return data
    return None

# 결과 로그 파일에 기록
def log_to_csv(data, prediction):
    with open(LOG_FILE, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data + [prediction])

# 예측 요청
def send_to_api(features):
    try:
        feature_keys = ["duration", "protocol_type", "src_bytes", "dst_bytes",
                        "flag", "land", "wrong_fragment", "urgent"]
        payload = dict(zip(feature_keys, features))  # ✅ 리스트 → 딕셔너리 변환

        response = requests.post(API_URL, json=payload)  # ✅ 수정된 전송 방식
        result = response.json()

        prediction = result.get("prediction", "None")
        confidence = result.get("confidence", 0.0)

        print(f"[✓] 예측 결과: {prediction} (신뢰도: {confidence})")
        log_to_csv(features, prediction)
    except Exception as e:
        print(f"[x] 예측 실패: {e}")

def process_packet(packet):
    features = extract_features(packet)
    if features:
        print(f"📦 수집된 패킷 특징: {features}")
        send_to_api(features)

if __name__ == "__main__":
    print("🟢 실시간 패킷 수집 시작! (중지하려면 Ctrl+C)")

    # 🔥 수정된 테스트 요청 → 위에서 정의한 API_URL 사용
    test_packet = {
        "duration": 0,
        "protocol_type": 6,
        "src_bytes": 5000,
        "dst_bytes": 0,
        "flag": 0,
        "land": 0,
        "wrong_fragment": 0,
        "urgent": 0
    }

    response = requests.post(API_URL, json=test_packet)  # ✅ 여기에 API_URL 사용!
    print("✅ 예측 응답:", response.text)

    # sniff 재시작
    scapy.sniff(prn=process_packet, store=False)