from scapy.all import IP, TCP, send
import time

# 반복 횟수 설정
NUM_PACKETS = 10
INTERVAL_SEC = 1  # 전송 간격(초)

for i in range(NUM_PACKETS):
    packet = IP(dst="127.0.0.1") / TCP(dport=80, flags="S") / ("X" * 20000)
    print(f" [{i+1}/{NUM_PACKETS}] 공격 시뮬레이션 패킷 전송 중...")
    send(packet, verbose=0)
    print(" 전송 완료!")
    time.sleep(INTERVAL_SEC)
