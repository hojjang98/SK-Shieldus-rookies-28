import json
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="보안 접근 로그 대시보드", layout="wide")
st.title("🛡️ Secure Access Log Dashboard")

log_path = "access.log"

# ===== 로그 파일 확인 =====
if not os.path.exists(log_path):
    st.warning("⚠️ 아직 access.log 파일이 없습니다. 먼저 secure_log_monitor.py를 실행해주세요.")
else:
    logs = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("{") and line.endswith("}"):
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # 혹시라도 깨진 JSON은 무시
    if not logs:
        st.error("❌ 유효한 JSON 로그를 찾지 못했습니다.")
        st.stop()

    df = pd.DataFrame(logs)


    # ===== 필터 =====
    st.sidebar.header("🔍 필터 설정")
    user_filter = st.sidebar.multiselect("사용자 선택", df["user"].unique())
    result_filter = st.sidebar.multiselect("결과 선택", df["result"].unique())

    if user_filter:
        df = df[df["user"].isin(user_filter)]
    if result_filter:
        df = df[df["result"].isin(result_filter)]

    # ===== 데이터 출력 =====
    st.subheader("📋 접근 로그 데이터")
    st.dataframe(df, use_container_width=True)

    # ===== 1. 접근 결과 비율 =====
    st.subheader("📊 접근 성공/실패 비율")
    fig_pie = px.pie(df, names="result", title="Access Success vs Fail")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ===== 2. 사용자별 접근 횟수 =====
    st.subheader("👥 사용자별 접근 횟수")
    fig_bar = px.bar(df, x="user", color="result", title="Access Count per User", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ===== 3. 에러 유형별 분석 =====
    if "error" in df.columns and not df[df["result"] == "FAIL"].empty:
        st.subheader("🚫 에러 유형별 발생 횟수")
        error_df = df[df["result"] == "FAIL"]
        fig_err = px.bar(error_df, x="error", color="user", title="Error Type Frequency")
        st.plotly_chart(fig_err, use_container_width=True)

    # ===== 4. 시간별 접근 추이 =====
    st.subheader("⏱️ 시간별 접근 추이")
    df["timestamp"] = pd.date_range(end=pd.Timestamp.now(), periods=len(df))
    fig_time = px.line(df, x="timestamp", y="result", color="user", title="Access Timeline")
    st.plotly_chart(fig_time, use_container_width=True)

    # ===== CSV 다운로드 =====
    st.download_button(
        label="📥 CSV로 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="access_log_export.csv",
        mime="text/csv"
    )
