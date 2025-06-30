# AI 기반 침입 탐지 시스템 (AI-IDS)

> 실시간 네트워크 트래픽을 분석하여 공격 여부를 예측하는 머신러닝 기반 IDS(Intrusion Detection System) API입니다. FastAPI와 Scikit-learn 기반으로 구현되었으며, NSL-KDD 데이터셋을 활용하여 학습하였습니다.

---

##  프로젝트 개요

- **프로젝트명**: AI 기반 침입 탐지 시스템
- **목표**: 머신러닝 모델을 활용한 실시간 트래픽 분석 및 공격 탐지
- **사용 기술**: Python, FastAPI, Scikit-learn, Pandas, Joblib

---

##  모델 개요

- **데이터셋**: [NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html)
- **알고리즘**: RandomForestClassifier
- **특징 수**: 42개 특성 + 1개 라벨
- **라벨 분류**: `normal` / `attack` (이진 분류)

---

##  디렉토리 구조

ai_ids_fastapi/
├── data/ # KDDTest+.txt 등 데이터
├── models/ # 학습된 모델, 스케일러 파일
├── train/
│ └── train_model.py # 모델 학습 및 저장 스크립트
├── main.py # FastAPI 서버
└── requirements.txt # 필요 패키지


##  실행 방법

1. 가상환경 설정 및 의존성 설치
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

----


# AI-based Intrusion Detection System (FastAPI + Docker)

본 프로젝트는 머신러닝 모델을 이용한 이상 네트워크 패킷 탐지 시스템입니다. FastAPI로 서버를 구성하고 Docker를 활용해 배포를 준비했습니다.

##  Features
- Scikit-learn 기반 IDS 모델 학습 및 추론
- FastAPI 서버에서 RESTful API 제공 (`/predict`)
- Swagger UI 자동 생성 및 테스트 가능
- Docker로 컨테이너화하여 쉽게 배포 가능

##  Usage

### 1. Docker 빌드 & 실행

```bash
docker build -t ai-ids-app .
docker run -d -p 8000:8000 ai-ids-app

-----

