# Dockerfile
FROM python:3.10-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y tcpdump libpcap-dev curl

# 프로젝트 복사
WORKDIR /app
COPY . .

# Python 라이브러리 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 실행 권한 부여
RUN chmod +x entrypoint.sh

# 환경 변수 기본값 설정 (선택)
ENV MODE=dashboard
ENV PORT=8501

# ENTRYPOINT 명확히 설정
ENTRYPOINT ["bash", "./entrypoint.sh"]
