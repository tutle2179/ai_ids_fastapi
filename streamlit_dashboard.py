import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime, timedelta

LOG_FILE = "packet_logs.csv"
REFRESH_INTERVAL = 3  # 자동 새로고침 간격 (초)

st.set_page_config(page_title="AI 침입 탐지 대시보드", layout="wide")

st.title("🔒 AI 기반 침입 탐지 대시보드")
st.caption("실시간 네트워크 패킷을 분석하여 이상 여부를 시각화합니다.")

@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    return pd.DataFrame(columns=[
        "timestamp", "duration", "protocol_type", "src_bytes",
        "dst_bytes", "flag", "land", "wrong_fragment", "urgent", "prediction"
    ])

# -------------------- 필터 옵션 --------------------
st.sidebar.header("📅 필터 옵션")
auto_refresh = st.sidebar.toggle("🔄 자동 새로고침", value=True)
filter_attack = st.sidebar.checkbox("🚨 공격 패킷만 보기", value=False)

default_date = datetime.now().date()
start_date = st.sidebar.date_input("조회 시작 날짜", default_date)
start_time = st.sidebar.time_input("조회 시작 시간", datetime.now().time().replace(minute=0, second=0))

start_dt = datetime.combine(start_date, start_time)

placeholder = st.empty()

# -------------------- 반복 루프 --------------------
while True:
    data = load_data()
    with placeholder.container():
        st.subheader("📊 실시간 탐지 현황")

        if data.empty:
            st.info("아직 수집된 패킷 데이터가 없습니다.")
        else:
            # 날짜/시간 필터
            data = data[data["timestamp"] >= start_dt]

            if filter_attack:
                data = data[data["prediction"] == "attack"]

            data_tail = data.tail(100)

            total_count = len(data)
            attack_count = len(data[data["prediction"] == "attack"])
            attack_ratio = (attack_count / total_count * 100) if total_count > 0 else 0.0

            col1, col2, col3 = st.columns(3)
            col1.metric("전체 탐지 수", total_count)
            col2.metric("공격 탐지 수", attack_count)
            col3.metric("공격 비율 (%)", f"{attack_ratio:.1f}")

            st.subheader("📋 최근 패킷 목록 (최대 100개)")
            st.dataframe(data_tail[::-1], use_container_width=True)

            st.subheader("📈 전체 탐지 비율")
            chart_data = data['prediction'].value_counts()
            st.bar_chart(chart_data)

    if not auto_refresh:
        break
    time.sleep(REFRESH_INTERVAL)
