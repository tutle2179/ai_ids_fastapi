#  AI 기반 침입 탐지 시스템 (AI_IDS_FASTAPI)

FastAPI + Scapy + Streamlit을 기반으로 실시간 네트워크 침입 탐지 및 시각화를 구현한 프로젝트입니다.

---

##  주요 기능
- FastAPI 기반 `/predict` API
- Scapy로 실시간 패킷 수집 및 AI 예측
- Streamlit으로 탐지 결과 실시간 시각화
- 공격 패킷 테스트 시뮬레이션 지원

---

##  프로젝트 구조

```
ai_ids_fastapi/
│
├── app/
│ ├── main.py
│ ├── model.py
│ ├── schema.py
│ └── utils.py
├── packet_sniffer.py
├── streamlit_dashboard.py
├── test_attack_packet.py
├── train/
│ ├── train_model.py
├── models/
│ ├── ids_model.pkl
│ └── scaler.pkl
├── data/
│ └── KDDTest+.txt
├── packet_logs.csv
├── requirements.txt
```
---

##  설치 및 실행 방법

```bash
# 1. 가상환경 설치
python -m venv venv
source venv/Scripts/activate

# 2. 라이브러리 설치
pip install -r requirements.txt

# 3. FastAPI 서버 실행
uvicorn app.main:app --reload --port 8010

# 4. 실시간 패킷 수집 실행
python packet_sniffer.py

# 5. Streamlit 대시보드 실행
streamlit run streamlit_dashboard.py

# (선택) 테스트 공격 패킷 전송
python test_attack_packet.py



모델 학습 방법

cd train
python train_model.py

데이터셋: NSL-KDD (KDDTest+.txt)
사용 Feature: duration, protocol_type, src_bytes, dst_bytes, flag, land, wrong_fragment, urgent

향후발전방향

- 실 트래픽 기반 감지를 위한 클라우드 서버 연동
- 실시간 패킷 캡처 고도화 (eth0, ens3 등 인터페이스 지정)
- HTTPS 서버 트래픽 디코딩 및 분석

기술 스택

- FastAPI, Streamlit, Scapy
- Scikit-learn, Pandas, joblib


##  3. 마무리 점검 리스트

| 항목 | 상태 | 확인사항 |
|------|------|----------|
| ✅ FastAPI `/predict` 정상 작동 | 완료 | 포트 8010에서 정상 응답 |
| ✅ packet_sniffer.py 실시간 감지 | 완료 | 정상 예측 응답 출력 확인 |
| ✅ streamlit_dashboard.py 시각화 | 완료 | 공격/정상 비율 막대차트 확인 |
| ✅ 모델 학습 코드 정상 작동 | 완료 | 8개 feature 기반 학습 완료 |
| ✅ README 작성 | 진행중 | 템플릿 적용 및 커스텀 필요 |
| 🔄 requirements.txt 최신화 | 필요 | `pip freeze > requirements.txt` 필요 |
| 🔄 `train/models` → `models` 경로 정비 | 필요 | 모델 저장 위치 정리 |

---


