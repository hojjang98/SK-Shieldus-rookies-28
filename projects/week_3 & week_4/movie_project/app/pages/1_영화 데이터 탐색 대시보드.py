import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# 상위 디렉토리의 utils 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_movie_data

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 탐색 대시보드",
    page_icon="📊",
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
st.title("📊 영화 데이터 탐색 대시보드")
st.markdown("다양한 관점에서 영화 데이터를 분석해보세요!")

# 데이터 로드
@st.cache_data
def load_data():
    df = load_movie_data()
    # release_year 생성
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    return df

try:
    df = load_data()
    
    # 사이드바 필터
    st.sidebar.header("🔍 필터")
    
    # 연도 범위 필터
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    
    year_range = st.sidebar.slider(
        "개봉 연도",
        min_year, max_year,
        (1980, max_year)
    )
    
    # 평점 범위 필터
    rating_range = st.sidebar.slider(
        "평점 범위",
        0.0, 10.0,
        (0.0, 10.0),
        0.1
    )
    
    # 장르 필터 (멀티셀렉트)
    all_genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Adventure', 'Fantasy', 'Family'
                                   'Thriller', 'Romance', 'Animation', 'Documentary']
    
    selected_genres = st.sidebar.multiselect(
        "장르 선택 (선택 안하면 전체)",
        all_genres
    )

    
    # 데이터 필터링
    filtered_df = df[
        (df['release_year'] >= year_range[0]) &
        (df['release_year'] <= year_range[1]) &
        (df['vote_average'] >= rating_range[0]) &
        (df['vote_average'] <= rating_range[1])
    ].copy()
    
    # 장르 필터 적용
    if selected_genres:
        filtered_df = filtered_df[
            filtered_df['genres'].apply(
                lambda x: any(genre in str(x) for genre in selected_genres)
            )
        ]
    
    # 필터링 결과 표시
    st.sidebar.markdown("---")
    st.sidebar.metric("필터링된 영화 수", f"{len(filtered_df):,}")
    st.sidebar.metric("전체 영화 수", f"{len(df):,}")
    
    # 메인 대시보드
    if len(filtered_df) == 0:
        st.warning("⚠️ 선택한 조건에 맞는 영화가 없습니다. 필터를 조정해주세요.")
    else:
        # 탭 생성
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 기본 통계", 
            "🎬 장르 분석", 
            "🌍 국가별 분석", 
            "📅 시계열 분석"
        ])
        
        # 탭 1: 기본 통계
        with tab1:
            st.header("📈 기본 통계")
            
            # KPI 메트릭
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("평균 평점", f"{filtered_df['vote_average'].mean():.2f}/10")
            
            with col2:
                st.metric("평균 런타임", f"{filtered_df['runtime'].mean():.0f}분")
            
            with col3:
                st.metric("총 투표 수", f"{filtered_df['vote_count'].sum():,.0f}")
            
            with col4:
                most_common_lang = filtered_df['original_language'].mode()[0]
                st.metric("주요 언어", most_common_lang.upper())
            
            st.markdown("---")
            
            # 분포 차트
            col1, col2 = st.columns(2)
            
            with col1:
                # 평점 분포
                st.subheader("평점 분포")
                fig = px.histogram(
                    filtered_df,
                    x='vote_average',
                    nbins=50,
                    labels={'vote_average': '평점', 'count': '영화 수'}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 런타임 분포
                st.subheader("런타임 분포")
                fig = px.histogram(
                    filtered_df,
                    x='runtime',
                    nbins=50,
                    labels={'runtime': '런타임 (분)', 'count': '영화 수'}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Scatter plot
            st.subheader("투표 수에 따른 평점 분포")
            fig = px.scatter(
                filtered_df.sample(min(5000, len(filtered_df))),
                x='vote_count',
                y='vote_average',
                color='vote_average',
                hover_data=['title'],
                labels={'vote_count': '투표 수', 'vote_average': '평점'},
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 탭 2: 장르 분석
        with tab2:
            st.header("🎬 장르 분석")
            
            # 장르 데이터 전처리
            genre_df = filtered_df.copy()
            genre_df['genre_list'] = genre_df['genres'].str.split(', ')
            genre_exploded = genre_df.explode('genre_list')
            
            # 장르별 통계
            genre_stats = genre_exploded.groupby('genre_list').agg({
                'vote_average': 'mean',
                'vote_count': 'sum',
                'title': 'count',
                'runtime': 'mean'
            }).round(2)
            genre_stats.columns = ['평균 평점', '총 투표 수', '영화 수', '평균 런타임']
            genre_stats.index.name = "장르"
            genre_stats = genre_stats.sort_values('영화 수', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 장르별 영화 수
                st.subheader("장르별 영화 수 (Top 15)")
                fig = px.bar(
                    genre_stats.head(15),
                    x=genre_stats.head(15).index,
                    y='영화 수',
                    labels={'장르': 'genre_list', '영화 수': '영화 수'}
                )
                fig.update_layout(
                    xaxis_title="장르",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 장르별 평균 평점
                st.subheader("장르별 평균 평점 (Top 15)")
                top_genres = genre_stats.head(15)
                fig = px.bar(
                    top_genres,
                    x=top_genres.index,
                    y='평균 평점',
                    labels={'장르': 'genre_list', '평균 평점': '평균 평점'},
                    color='평균 평점',
                    color_continuous_scale='blues'
                )
                fig.update_layout(
                    xaxis_title="장르",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 장르별 상세 통계 테이블
            st.subheader("장르별 상세 통계")
            st.dataframe(
                genre_stats.head(20),
                use_container_width=True
            )
        
        # 탭 3: 국가별 분석
        with tab3:
            st.header("🌍 국가별 분석")
            
            # 국가 데이터 전처리
            country_df = filtered_df.copy()
            country_df['country_list'] = country_df['production_countries'].str.split(', ')
            country_exploded = country_df.explode('country_list')
            
            # 국가별 통계
            country_stats = country_exploded.groupby('country_list').agg({
                'vote_average': 'mean',
                'vote_count': 'sum',
                'title': 'count',
                'runtime': 'mean'
            }).round(2)
            country_stats.columns = ['평균 평점', '총 투표 수', '영화 수', '평균 런타임']
            country_stats.index.name = "국가"

            country_stats = country_stats[country_stats['영화 수'] >= 10]  # 최소 10편 이상
            country_stats = country_stats.sort_values('영화 수', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 국가별 영화 수
                st.subheader("국가별 영화 제작 수 (Top 15)")
                fig = px.bar(
                    country_stats.head(15),
                    x=country_stats.head(15).index,
                    y='영화 수',
                    labels={'country_list': '국가', '영화 수': '영화 수'}
                )
                fig.update_layout(
                    xaxis_title="국가",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 국가별 평균 평점
                st.subheader("국가별 평균 평점 (Top 15)")
                top_countries = country_stats.head(15)
                fig = px.bar(
                    top_countries,
                    x=top_countries.index,
                    y='평균 평점',
                    labels={'country_list': '국가', '평균 평점': '평균 평점'},
                    color='평균 평점',
                    color_continuous_scale='greens'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            # 국가별 상세 통계 테이블
            st.subheader("국가별 상세 통계")
            st.dataframe(
                country_stats.head(20),
                use_container_width=True
            )
        
        # 탭 4: 시계열 분석
        with tab4:
            st.header("📅 시계열 분석")
            
            # 연도별 통계
            yearly_stats = filtered_df.groupby('release_year').agg({
                'title': 'count',
                'vote_average': 'mean',
                'runtime': 'mean',
                'vote_count': 'sum'
            }).reset_index()
            yearly_stats.columns = ['연도', '영화 수', '평균 평점', '평균 런타임', '총 투표 수']
            
            # 연도별 영화 제작 편수
            st.subheader("연도별 영화 제작 편수")
            fig = px.line(
                yearly_stats,
                x='연도',
                y='영화 수',
                labels={'연도': '연도', '영화 수': '영화 수'}
            )
            fig.update_traces(line_color='#1f77b4', line_width=2)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 연도별 평균 평점
                st.subheader("연도별 평균 평점 추이")
                fig = px.line(
                    yearly_stats,
                    x='연도',
                    y='평균 평점',
                    labels={'연도': '연도', '평균 평점': '평균 평점'}
                )
                fig.update_traces(line_color='#2ca02c', line_width=2)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 연도별 평균 런타임
                st.subheader("연도별 평균 런타임 추이")
                fig = px.line(
                    yearly_stats,
                    x='연도',
                    y='평균 런타임',
                    labels={'연도': '연도', '평균 런타임': '평균 런타임 (분)'}
                )
                fig.update_traces(line_color='#ff7f0e', line_width=2)
                st.plotly_chart(fig, use_container_width=True)
            
            # 10년 단위 분석
            st.subheader("10년 단위(Decade) 분석")
            filtered_df['decade'] = (filtered_df['release_year'] // 10) * 10
            decade_stats = filtered_df.groupby('decade').agg({
                'title': 'count',
                'vote_average': 'mean',
                'runtime': 'mean'
            }).reset_index()
            decade_stats.columns = ['연대', '영화 수', '평균 평점', '평균 런타임']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=decade_stats['연대'],
                y=decade_stats['영화 수'],
                name='영화 수',
                marker_color='lightblue'
            ))
            fig.update_layout(
                xaxis_title="연대",
                yaxis_title="영화 수",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.info("data/tmdb_cleaned.csv 파일이 존재하는지 확인해주세요.")

# 사이드바 정보
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 사용 팁")
    st.markdown("""
    - 왼쪽 필터로 데이터 범위 조정
    - 장르를 선택하면 해당 장르만 분석
    - 각 탭에서 다양한 관점으로 분석 가능
    """)