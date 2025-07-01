#!/bin/bash
set -e

# .env 존재 여부 확인
if [ ! -f .env ]; then
  echo "❌ .env 파일이 존재하지 않습니다. 종료합니다."
  exit 1
fi

# 환경 변수 로드
set -a
source .env
set +a

echo "======================================="
echo "🔧 시작 모드: $1"
echo "======================================="

if [ "$1" = "api" ]; then
    echo "▶ FastAPI 서버 실행"
    uvicorn app.main:app --host 0.0.0.0 --port 8010

elif [ "$1" = "sniffer" ]; then
    echo "▶ 패킷 수집기 실행"
    python packet_sniffer.py --iface "$IFACE"

elif [ "$1" = "dashboard" ]; then
    echo "▶ Streamlit 대시보드 실행"
    streamlit run streamlit_dashboard.py --server.port 8501

else
    echo "❌ 올바른 모드를 지정해주세요: api | sniffer | dashboard"
    exit 1
fi
