import streamlit as st
import pandas as pd
import time
import os

LOG_FILE = "packet_logs.csv"  # packet_sniffer.py에서 로그 저장하는 파일

st.set_page_config(page_title="AI 침입 탐지 대시보드", layout="wide")

st.title("🛡️ AI 기반 침입 탐지 시스템")
st.markdown("실시간으로 네트워크 패킷을 분석하고 이상 여부를 탐지합니다.")

# 데이터 초기화
@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame(columns=[
        "timestamp", "duration", "protocol_type", "src_bytes",
        "dst_bytes", "flag", "land", "wrong_fragment", "urgent", "prediction"
    ])

placeholder = st.empty()

# 실시간 갱신 루프
while True:
    data = load_data()

    with placeholder.container():
        st.subheader("📊 최근 탐지된 패킷 정보")
        if not data.empty:
            st.dataframe(data.tail(20), use_container_width=True)

            st.subheader("📈 공격 탐지 비율")
            attack_counts = data['prediction'].value_counts()
            st.bar_chart(attack_counts)

        else:
            st.info("아직 수집된 패킷 데이터가 없습니다.")

    time.sleep(2)
