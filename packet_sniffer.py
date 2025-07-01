import logging
import time
import requests
import csv
import os
import argparse
from scapy.all import sniff, IP, TCP, UDP, get_if_list

# ===================== 초기 설정 =====================
LOG_FILE = "packet_logs.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "duration", "protocol_type", "src_bytes",
                         "dst_bytes", "flag", "land", "wrong_fragment", "urgent", "prediction"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/packet_sniffer.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

API_URL = "http://localhost:8010/predict"

# ===================== 인터페이스 자동 탐색 함수 =====================
def auto_select_interface():
    interfaces = get_if_list()
    logging.info("🔍 자동 인터페이스 탐색 중...")
    for iface in interfaces:
        if "Loopback" in iface or "lo" in iface:
            continue
        try:
            packets = sniff(iface=iface, timeout=4, count=3, store=False)
            if packets:
                logging.info(f"✅ 자동 감지된 인터페이스: {iface}")
                return iface
        except Exception as e:
            continue
    logging.warning("⚠ 자동 감지 실패. 수동 선택으로 전환.")
    return None

# ===================== 패킷 → 특징 추출 함수 =====================
def extract_features(pkt):
    try:
        if IP in pkt:
            proto = pkt[IP].proto
            length = len(pkt)
            if proto == 6 and TCP in pkt:
                return {
                    "duration": 0,
                    "protocol_type": 6,
                    "src_bytes": length,
                    "dst_bytes": 0,
                    "flag": 0,
                    "land": 0,
                    "wrong_fragment": 0,
                    "urgent": 0
                }
            elif proto == 17 and UDP in pkt:
                return {
                    "duration": 0,
                    "protocol_type": 17,
                    "src_bytes": length,
                    "dst_bytes": 0,
                    "flag": 0,
                    "land": 0,
                    "wrong_fragment": 0,
                    "urgent": 0
                }
    except Exception as e:
        logging.warning(f"[extract_features] 패킷 처리 오류: {e}")
    return None

# ===================== CSV 저장 =====================
def log_to_csv(features, prediction):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            features["duration"],
            features["protocol_type"],
            features["src_bytes"],
            features["dst_bytes"],
            features["flag"],
            features["land"],
            features["wrong_fragment"],
            features["urgent"],
            prediction
        ])

# ===================== 예측 요청 =====================
def predict_packet(features):
    try:
        response = requests.post(API_URL, json=features)
        if response.status_code == 200:
            result = response.json()
            pred = result.get("prediction", "unknown")
            conf = result.get("confidence", 0.0)
            logging.info(f"[✓] 예측 결과: {pred} (신뢰도: {conf})")
            log_to_csv(features, pred)
        else:
            logging.error(f"[predict_packet] 응답 오류: {response.status_code}")
            log_to_csv(features, "fail")
    except Exception as e:
        logging.error(f"[predict_packet] 예측 실패: {e}")
        log_to_csv(features, "fail")

# ===================== 패킷 처리 =====================
def process_packet(pkt):
    features = extract_features(pkt)
    if features:
        logging.info(f"수집된 패킷 특징: {list(features.values())}")
        predict_packet(features)

# ===================== 메인 =====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI 침입 탐지 실시간 패킷 수집기")
    parser.add_argument("--iface", type=str, help="수집할 네트워크 인터페이스 이름")
    args = parser.parse_args()

    iface = args.iface or auto_select_interface()

    if not iface:
        interfaces = get_if_list()
        print("💻 사용 가능한 인터페이스 목록:")
        for idx, name in enumerate(interfaces):
            print(f"{idx}: {name}")
        try:
            index = int(input("👉 사용할 인터페이스 번호를 입력하세요: "))
            iface = interfaces[index]
        except Exception:
            print("❗ 기본 인터페이스로 자동 설정합니다.")
            iface = interfaces[0]

    logging.info(f"🟢 패킷 수집 시작 (인터페이스: {iface})")
    try:
        while True:
            sniff(prn=process_packet, store=False, iface=iface, timeout=10)
    except KeyboardInterrupt:
        logging.info("🛑 수집 종료됨")
    except Exception as e:
        logging.error(f"[main] sniff 중 오류 발생: {e}")
