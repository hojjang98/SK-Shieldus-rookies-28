import streamlit as st
from pathlib import Path
import pandas as pd

# 1. 페이지 설정 (가장 먼저 실행)
st.set_page_config(
    page_title="Movie Analysis & Recommendation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS 스타일 적용
st.markdown("""
    <style>
    /* 사이드바 스타일 (기존 유지) */
    section[data-testid="stSidebar"] ul li {
        padding-bottom: 8px;
        margin-bottom: 8px;
        border-bottom: 1px solid #cccccc60;
    }
    section[data-testid="stSidebar"] ul li:last-child {
        border-bottom: none;
    }
    section[data-testid="stSidebar"] ul li a[aria-current="page"] {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #2C3E50 !important;
    }

    /* ======================== */
    /* 카드 스타일 (여백 최적화 버전) */
    /* ======================== */
    .feature-card {
        background-color: #F8FAFD;
        padding: 20px 15px; /* 좌우 여백 유지 */
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
        
        /* 공간 꽉 채우기 설정 */
        width: 100% !important;
        height: 100% !important; /* 이 부분이 중요: 내용에 따라 높이가 늘어나도록 */
        box-sizing: border-box !important;
        
        /* 텍스트 줄바꿈 방지 */
        word-break: keep-all !important;
        overflow-wrap: break-word;
        
        /* min-height를 조금 줄여서 내용이 적은 카드도 너무 길지 않게 */
        min-height: 205px; /* 기존 280px에서 250px로 줄여봄 */
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.10);
        background-color: #ffffff;
    }

    /* 제목 스타일 */
    .feature-title {
        font-size: 18px; 
        font-weight: 700;
        color: #1A202C;
        margin-bottom: 12px;
        line-height: 1.3;
    }

    /* 리스트 항목 */
    .feature-card ul {
        padding-left: 18px; /* 불릿 포인트 여백 유지 */
        margin: 0; /* [핵심 수정] ul의 기본 하단 마진을 0으로 만듦 */
        flex-grow: 1; /* [추가] 내용이 적은 카드도 높이를 채우도록 */
    }

    .feature-card li {
        padding: 3px 0;
        font-size: 14px;
        color: #4A5568;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 메인 페이지 내용
st.title("🎬 Movie Analysis & Recommendation System")

st.markdown("""
            <div style="font-size: 18px; line-height: 1.6; padding: 15px;">
            TMDB 데이터를 기반으로 다양한 분석 기능을 제공하는 영화 통합 분석 플랫폼입니다.<br>
            아래 기능들을 통해 영화의 흥행 요인을 탐색하고 추천 시스템을 경험해보세요.
            </div>
            """, unsafe_allow_html=True)

# 주요 기능 섹션
st.markdown("<h2 style='margin-top: 40px;'>주요 기능</h2>", unsafe_allow_html=True)
st.write("")

feature_list = [
    {
        "icon": "📊",
        "title": "영화 데이터 탐색",
        "items": [
            "인터랙티브 시각화",
            "장르별 흥행 분석",
            "국가별 성과 비교",
            "시계열 트렌드 분석"
        ]
    },
    {
        "icon": "💰",
        "title": "흥행 지표 분석",
        "items": [
            "Top 영화 분석",
            "투자 수익률 (ROI) 패턴 분석",
            "성공 영화 특징 분석",
            "AI 기반 흥행 요인 분석"
        ]
    },
    {
        "icon": "🎬",
        "title": "감독 기반 영화 탐색",
        "items": [
            "감독 종합 랭킹",
            "감독별 흥행 성공률 분석",
            "감독별 장르 분석",
            "개별 감독 상세 분석"
        ]
    },
    {
        "icon": "⭐",
        "title": "영화 제작 분석 시스템",
        "items": [
            "영화 기획안 종합 분석",
            "빠른 투자 수익률(ROI) 예측",
            "실시간 영화 시장 트렌드"
        ]
    }
]

# [수정됨] 카드가 4개이므로 컬럼도 4개로 설정해야 꽉 찹니다.
cols = st.columns(4)

for col, feature in zip(cols, feature_list):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{feature['icon']} {feature['title']}</div>
            <ul>
                {''.join([f"<li>{item}</li>" for item in feature['items']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)


# 통계 요약
st.markdown("---")
st.markdown("<h2>📊 데이터 통계</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

try:
    # 실제 파일이 없다면 에러가 나므로 예외처리 유지
    from utils.data_loader import load_movie_data
    
    df = load_movie_data()
    
    with col1:
        st.metric("전체 영화 수", f"{len(df):,}")
    
    with col2:
        st.metric("평균 평점", f"{df['vote_average'].mean():.2f}/10")
    
    with col3:
        unique_genres = df['genres'].str.split(', ').explode().nunique()
        st.metric("장르 수", f"{unique_genres}")
    
    with col4:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        min_year = df['release_date'].dt.year.min()
        max_year = df['release_date'].dt.year.max()
        
        if pd.notna(min_year) and pd.notna(max_year):
            year_range = f"{int(min_year)} - {int(max_year)}"
        else:
            year_range = "N/A"
        
        st.metric("연도 범위", year_range)

except Exception as e:
    # 데이터 로드 실패 시에도 UI가 깨지지 않게 처리
    # st.warning("데이터를 불러오는 중입니다 (Demo Mode)") 
    pass