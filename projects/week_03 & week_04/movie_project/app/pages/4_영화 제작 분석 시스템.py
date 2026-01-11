import streamlit as st
from pathlib import Path
import sys
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from utils.vector_db import load_vector_db
from utils.production_rag import ProductionRAG

# 페이지 설정
st.set_page_config(
    page_title="영화 제작 분석 시스템",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
            <style>
            section[data-testid="stSidebar"] ul li {
                padding-bottom: 8px;
                margin-bottom: 8px;
                border-bottom: 1px solid #cccccc60;
            }
            section[data-testid="stSidebar"] ul li:last-child {
                border-bottom: none;
            }
            </style>
            """, unsafe_allow_html=True)

st.title("🎬 영화 제작 분석 시스템")
st.markdown("영화 산업의 기획·투자 의사결정을 지원할 수 있도록 분석합니다!")

# 데이터 로드
@st.cache_resource
def get_collection():
    return load_vector_db()

@st.cache_data
def get_movie_data():
    """영화 데이터 로드 (여러 경로 시도)"""
    possible_paths = [
        Path(__file__).parent.parent.parent / "data" / "tmdb_cleaned.csv",
        Path("../data/tmdb_cleaned.csv"),
        Path("data/tmdb_cleaned.csv"),
    ]
    
    for path in possible_paths:
        if path.exists():
            df = pd.read_csv(path)
            return df
    
    # 모든 경로 실패
    st.error(f"❌ tmdb_cleaned.csv를 찾을 수 없습니다!")
    st.info(f"시도한 경로:\n" + "\n".join([f"- {p.absolute()}" for p in possible_paths]))
    return None

collection = get_collection()
df = get_movie_data()

if collection is None:
    st.error("❌ Vector DB를 로드할 수 없습니다.")
    st.info("💡 notebooks/Movie_Analysis.ipynb를 실행하여 Vector DB를 먼저 생성해주세요!")
elif df is None:
    st.error("❌ 영화 데이터를 로드할 수 없습니다.")
    st.info("💡 data/tmdb_cleaned.csv 파일이 존재하는지 확인해주세요!")
else:
    # RAG 시스템 초기화
    try:
        rag_system = ProductionRAG(collection, df)
        
        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["📋 기획안 분석", "📊 빠른 투자 수익률(ROI) 예측", "📈 시장 트렌드"])
        
        
        # 탭 1: 기획안 종합 분석
        with tab1:
            st.markdown("### 📋 영화 기획안 종합 분석")
            st.markdown("기획 중인 영화의 흥행 가능성과 수익성을 AI가 분석해드립니다.")
            
            with st.form("proposal_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("영화 제목", placeholder="예: The Next Blockbuster")
                    
                    genre_options = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 
                                   'Thriller', 'Romance', 'Animation', 'Documentary', 'Adventure', 'Fantasy', 'Family']
                    genre = st.selectbox("주요 장르", genre_options)
                    
                    budget = st.number_input(
                        "예상 제작 예산 (USD)",
                        min_value=100000,
                        max_value=500000000,
                        value=1000000,
                        step=100000,
                        format="%d"
                    )
                
                with col2:
                    target_audience = st.text_input(
                        "타겟 관객",
                        placeholder="예: 20-40대 SF 팬층"
                    )
                    
                    similar_movies = st.text_area(
                        "참고 영화 (한 줄에 하나씩)",
                        placeholder="Inception\nInterstellar\nThe Matrix"
                    )
                    
                    runtime = st.number_input("예상 러닝타임 (분)", 30, 480, 120)
                
                synopsis = st.text_area(
                    "시놉시스 / 기획 의도",
                    placeholder="영화의 주요 내용, 컨셉, 차별화 포인트를 입력하세요...",
                    height=150
                )
                
                submitted = st.form_submit_button("AI 분석 시작", type="primary", use_container_width=True)
            
            if submitted and title and synopsis:
                with st.spinner("AI가 시장 데이터를 분석하고 있습니다..."):
                    try:
                        # 기획안 구성
                        proposal = {
                            'title': title,
                            'genre': genre,
                            'budget': budget,
                            'target_audience': target_audience,
                            'synopsis': synopsis,
                            'similar_movies': [m.strip() for m in similar_movies.split('\n') if m.strip()],
                            'runtime': runtime
                        }
                        
                        # RAG 분석 실행
                        result = rag_system.analyze_production_proposal(proposal)
                        
                        if result['success']:
                            # 분석 결과 표시
                            st.markdown("---")
                            
                            # 메인 분석 보고서
                            st.markdown(result['analysis'])
                            
                            st.markdown("---")
                            

# 성과 지표
                            if result['performance_metrics']:
                                st.markdown("## 핵심 성과 지표 (KPI)")
                                
                                perf = result['performance_metrics']
                                
                                # 첫 줄: 보수적 예측
                                st.markdown("#### 보수적 예측 (하위 40% 기준)")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric(
                                        "보수적 예상 수익",
                                        f"${perf['adjusted_revenue']:,.0f}",
                                        f"{((perf['adjusted_revenue']/budget - 1) * 100):.1f}%"
                                    )
                                
                                with col2:
                                    st.metric(
                                        "보수적 예상 ROI",
                                        f"{perf['adjusted_roi']:.2f}배",
                                        "손익분기" if perf['is_profitable'] else "주의"
                                    )
                                
                                with col3:
                                    st.metric(
                                        "최악의 경우",
                                        f"${perf['catastrophic_case']:,.0f}",
                                        "하위 15%"
                                    )
                                
                                with col4:
                                    st.metric(
                                        "최대 수익",
                                        f"${perf['best_case']:,.0f}",
                                        "낙관적"
                                    )
                                
                                # 두 번째 줄: 일반 통계
                                st.markdown("#### 일반 통계 (참고)")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric(
                                        "평균 수익",
                                        f"${perf['avg_revenue']:,.0f}",
                                        "장르 평균"
                                    )
                                
                                with col2:
                                    st.metric(
                                        "평균 ROI",
                                        f"{perf['avg_roi']:.2f}배",
                                        "장르 평균"
                                    )
                                
                                with col3:
                                    st.metric(
                                        "중위 수익",
                                        f"${perf['median_revenue']:,.0f}",
                                        "중간값"
                                    )
                                
                                with col4:
                                    st.metric(
                                        "중위 ROI",
                                        f"{perf['median_roi']:.2f}배",
                                        "중간값"
                                    )
                                
                                st.info(f"분석 기반: 유사 영화 {perf['sample_size']}편 | 보수적 기준(하위 40%) + 일반 통계 제공")
                            
                            st.markdown("---")
                            
                            # 유사 영화 참고 사례
                            if result['similar_movies']:
                                st.markdown("## 유사 영화 성과 사례")
                                
                                similar_df = pd.DataFrame(result['similar_movies'])
                                similar_df = similar_df.sort_values('roi', ascending=False)
                                
                                display_df = similar_df[['title', 'genre', 'budget', 'revenue', 'roi', 'vote_average']].head(10)
                                display_df.columns = ['영화 제목', '장르', '제작비', '수익', 'ROI', '평점']
                                
                                # 포맷팅
                                display_df['제작비'] = display_df['제작비'].apply(lambda x: f"${x:,.0f}")
                                display_df['수익'] = display_df['수익'].apply(lambda x: f"${x:,.0f}")
                                display_df['ROI'] = display_df['ROI'].apply(lambda x: f"{x:.2f}배")
                                display_df['평점'] = display_df['평점'].apply(lambda x: f"{x:.1f}/10")
                                
                                st.dataframe(display_df, use_container_width=True, hide_index=True)
                        
                        else:
                            st.error(f"❌ 분석 실패: {result['error']}")
                    
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
                        st.exception(e)
        
        
        # 탭 2: 빠른 ROI 예측
        
        with tab2:
            st.markdown("### 📊 빠른 ROI 예측")
            st.markdown("장르와 예산만으로 빠르게 ROI를 예측합니다.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                quick_genre = st.selectbox(
                    "장르 선택",
                    ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 
                     'Thriller', 'Romance', 'Animation'],
                    key="quick_genre"
                )
            
            with col2:
                quick_budget = st.number_input(
                    "제작 예산 (USD)",
                    min_value=1000000,
                    max_value=500000000,
                    value=30000000,
                    step=5000000,
                    key="quick_budget"
                )
            
            if st.button("빠른 예측", type="primary", use_container_width=True):
                with st.spinner("계산 중..."):
                    estimate = rag_system.quick_roi_estimate(quick_genre, quick_budget)
                    
                    if estimate:
                        st.markdown("---")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("예상 ROI", f"{estimate['avg_roi']:.2f}배")
                        
                        with col2:
                            st.metric("예상 수익", f"${estimate['expected_revenue']:,.0f}")
                        
                        with col3:
                            expected_profit = estimate['expected_revenue'] - quick_budget
                            st.metric("예상 순이익", f"${expected_profit:,.0f}")
                        
                        
                        
                    else:
                        st.warning("⚠️ 충분한 데이터가 없습니다. 다른 조건을 시도해보세요.")
        
        
        # 탭 3: 시장 트렌드
        
        with tab3:
            st.markdown("### 📈 실시간 시장 트렌드")
            
            if st.button("인기 영화 및 개봉 예정작 조회", use_container_width=True):
                with st.spinner("데이터 수집 중..."):
                    try:
                        trending = rag_system.tmdb_client.get_trending_movies()
                        upcoming = rag_system.tmdb_client.get_upcoming_movies()
                        
                        if trending or upcoming:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### 🔥 현재 인기 영화")
                                for movie in trending[:10]:
                                    with st.expander(f"**{movie['title']}**"):
                                        st.write(f"**인기도:** {movie['popularity']:.1f}")
                                        st.write(f"**평점:** {movie['vote_average']:.1f}/10")
                                        st.write(f"**개봉일:** {movie.get('release_date', 'N/A')}")
                            
                            with col2:
                                st.markdown("#### 🎬 개봉 예정작")
                                for movie in upcoming[:10]:
                                    with st.expander(f"**{movie['title']}**"):
                                        st.write(f"**개봉 예정:** {movie.get('release_date', 'N/A')}")
                                        st.write(f"**인기도:** {movie['popularity']:.1f}")
                        else:
                            st.warning("⚠️ TMDB API 데이터를 가져올 수 없습니다.")
                    
                    except Exception as e:
                        st.error(f"❌ 트렌드 수집 실패: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ RAG 시스템 초기화 실패: {str(e)}")
        st.exception(e)

# 사이드바
with st.sidebar:
    st.markdown("### 🎯 시스템 기능")
    st.markdown("""
    **기획안 분석:**
    - 수익 예측
    - ROI 전망
    - 리스크 분석
    - 제작 전략 제안
    """)
    
    st.markdown("---")
    st.markdown("### 💡 사용 팁")
    st.markdown("""
    1. 상세한 시놉시스 입력
    2. 유사 영화 참고 제시
    3. 현실적인 예산 설정
    4. 타겟 관객 명확히 정의
    """)
    
    st.markdown("---")
    st.markdown("### 📊 데이터 현황")
    if df is not None:
        valid_data = df[(df['budget'] > 0) & (df['revenue'] > 0)]
        st.info(f"분석 가능: {len(valid_data):,}편")
        st.success(f"전체: {len(df):,}편")