import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

st.set_page_config(page_title="Security Log Dashboard", layout="wide")

st.title("🛡️ Security Log Dashboard")
st.caption("Week2 - Streamlit 기반 보안 로그 시각화")

def load_access_log(path="access.log"):
    if not os.path.exists(path):
        return pd.DataFrame()
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(records)

df = load_access_log()

if df.empty:
    st.warning("⚠️ access.log 파일에 읽을 수 있는 JSON 데이터가 없습니다.")
    st.stop()

st.sidebar.header("필터")
user_filter = st.sidebar.multiselect("사용자 선택", df["user"].unique(), default=df["user"].unique())
result_filter = st.sidebar.multiselect("결과 선택", df["result"].unique(), default=df["result"].unique())

filtered = df[(df["user"].isin(user_filter)) & (df["result"].isin(result_filter))]

st.metric("총 접근 시도", len(filtered))
fail_count = (filtered["result"] == "FAIL").sum()
fail_rate = (fail_count / len(filtered)) * 100 if len(filtered) > 0 else 0
st.metric("실패율 (%)", f"{fail_rate:.1f}")

st.subheader("📊 접근 결과 비율")
fig_pie = px.pie(filtered, names="result", title="Access Result Ratio", color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("👥 사용자별 접근 시도")
fig_bar = px.bar(filtered, x="user", color="result", barmode="group", title="Access Attempts per User")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("🧾 Raw Log Data")
st.dataframe(filtered, use_container_width=True)

st.caption("© 2025 SK Shielders Rookies 28기 | Streamlit Log Dashboard")
