import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="감독 분석", page_icon="🎬", layout="wide")

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

# 데이터 로드
@st.cache_data
def load_movie_data():
    """영화 데이터 로드"""
    possible_paths = [
        Path(__file__).parent.parent.parent / "data" / "tmdb_cleaned.csv",
        Path("../data/tmdb_cleaned.csv"),
        Path("data/tmdb_cleaned.csv"),
        Path(r"C:\Users\ghwns\movie-project_02\data\tmdb_cleaned.csv"),
    ]
    
    for data_path in possible_paths:
        if data_path.exists():
            df = pd.read_csv(data_path)
            return df
    
    st.error("❌ 데이터 파일을 찾을 수 없습니다!")
    st.stop()

@st.cache_data
def load_director_data():
    """감독 분석용 데이터 로드 및 전처리"""
    df = load_movie_data()
    
    # 장르 파싱
    def parse_genres(genre_str):
        """쉼표로 구분된 장르 문자열을 리스트로 변환"""
        if pd.isna(genre_str) or genre_str == '':
            return []
        if isinstance(genre_str, list):
            return genre_str
        try:
            genres = [g.strip() for g in str(genre_str).split(',')]
            return [g for g in genres if g]
        except:
            return []
    
    df['genre_list'] = df['genres'].apply(parse_genres)
    
    # 연도 추출
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    
    # 필터링
    df_full = df[(df['revenue'].notna()) & (df['budget'].notna())].copy()
    df_full = df_full[(df_full['revenue'] > 0) & (df_full['budget'] > 0)]
    
    # ROI 계산
    df_full['ROI'] = df_full['revenue'] / df_full['budget']
    df_full['profit'] = df_full['revenue'] - df_full['budget']
    
    # director 확인
    if 'director' not in df_full.columns:
        st.error("❌ 'director' 컬럼이 없습니다!")
        st.stop()
    
    df_full = df_full[df_full['director'].notna()]
    
    return df_full

# 데이터 로드
try:
    df_full = load_director_data()
except Exception as e:
    st.error(f"❌ 데이터 로드 실패: {e}")
    st.exception(e)
    st.stop()

# 사이드바 : 필터
st.sidebar.header("🎛️ 필터 설정")

min_movies = st.sidebar.slider("최소 작품 수", 1, 20, 5)
success_criteria = st.sidebar.selectbox(
    "흥행 성공 기준",
    ["ROI 3.0 이상", "블록버스터 (1억불)", "메가 히트 (2억불)", "작품성 (평점 7.0)"]
)
sort_by = st.sidebar.selectbox(
    "정렬 기준",
    ["총수익", "평균수익", "평균평점", "흥행작비율"]
)

# 메인: 감독 통계

st.title("🎬 감독별 흥행 분석")
st.markdown("감독별로 흥행한 장르들과 흥행 요인을 분석해드립니다!")

with st.spinner("감독 데이터 분석 중..."):
    # 기본 집계
    director_stats = df_full.groupby('director').agg({
        'id': 'count',
        'revenue': ['mean', 'sum'],
        'vote_average': 'mean',
        'vote_count': 'mean',
        'ROI': 'median',
        'budget': 'mean',
        'runtime': 'mean'
    }).round(2)
    
    director_stats.columns = ['작품수', '평균수익', '총수익', '평균평점', '평균투표수', 'ROI중앙값', '평균예산', '평균러닝타임']
    director_stats = director_stats[director_stats['작품수'] >= min_movies]
    
    # 주요 장르
    def get_director_genres(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        all_genres = director_movies.explode('genre_list')['genre_list']
        all_genres = all_genres[all_genres.notna() & (all_genres != '')]
        
        if len(all_genres) == 0:
            return 'N/A'
        
        genre_counts = all_genres.value_counts()
        top_genres = [f"{genre}({count})" for genre, count in genre_counts.head(3).items()]
        return ', '.join(top_genres)
    
    # 장르 다양성
    def get_genre_diversity(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        all_genres = director_movies.explode('genre_list')['genre_list']
        all_genres = all_genres[all_genres.notna() & (all_genres != '')]
        return all_genres.nunique()
    
    # 활동 시기
    def get_active_decades(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        decades = director_movies['release_year'].apply(lambda x: f"{int(x//10)*10}s" if pd.notna(x) else None)
        decade_counts = decades.value_counts().head(3)
        return ', '.join(decade_counts.index.tolist()) if len(decade_counts) > 0 else 'N/A'
    
    # 성공률 함수들
    def get_roi_success_rate(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        success_count = (director_movies['ROI'] >= 3.0).sum()
        return round(success_count / len(director_movies) * 100, 1)
    
    def get_blockbuster_rate(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        success_count = (director_movies['revenue'] >= 100_000_000).sum()
        return round(success_count / len(director_movies) * 100, 1)
    
    def get_mega_hit_rate(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        success_count = (director_movies['revenue'] >= 200_000_000).sum()
        return round(success_count / len(director_movies) * 100, 1)
    
    def get_quality_rate(director_name):
        director_movies = df_full[df_full['director'] == director_name]
        success_count = (director_movies['vote_average'] >= 7.0).sum()
        return round(success_count / len(director_movies) * 100, 1)
    
    # 모든 지표 추가
    director_stats['주요장르'] = director_stats.index.map(get_director_genres)
    director_stats['장르다양성'] = director_stats.index.map(get_genre_diversity)
    director_stats['활동시기'] = director_stats.index.map(get_active_decades)
    director_stats['ROI3.0이상(%)'] = director_stats.index.map(get_roi_success_rate)
    director_stats['블록버스터(%)'] = director_stats.index.map(get_blockbuster_rate)
    director_stats['메가히트(%)'] = director_stats.index.map(get_mega_hit_rate)
    director_stats['작품성7.0이상(%)'] = director_stats.index.map(get_quality_rate)

# 탭 구성

tab1, tab2, tab3, tab4 = st.tabs(["📊 종합 랭킹", "🎯 흥행 분석", "🎨 장르 분석", "👤 개별 감독"])

# 탭 1: 종합 랭킹

with tab1:
    st.header("📊 감독 종합 랭킹")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("전체 감독 수", f"{len(director_stats):,}명")
    with col2:
        st.metric("평균 작품 수", f"{director_stats['작품수'].mean():.1f}편")
    with col3:
        st.metric("평균 총수익", f"${director_stats['총수익'].mean()/1e6:.1f}M")
    with col4:
        st.metric("평균 평점", f"{director_stats['평균평점'].mean():.2f}")
    
    st.markdown("---")
    
    sort_column_map = {
        "총수익": "총수익",
        "평균수익": "평균수익",
        "평균평점": "평균평점",
        "흥행작비율": "블록버스터(%)"
    }
    
    sorted_stats = director_stats.sort_values(sort_column_map[sort_by], ascending=False)
    
    st.subheader(f"Top 30 감독 ({sort_by} 기준)")
    display_columns = ['작품수', '총수익', '평균수익', '평균평점', '주요장르', '활동시기']
    
    display_df = sorted_stats[display_columns].head(30).copy()
    display_df['총수익'] = (display_df['총수익'] / 1e6).round(1).astype(str) + 'M'
    display_df['평균수익'] = (display_df['평균수익'] / 1e6).round(1).astype(str) + 'M'
    display_df.index.name = "감독"

    st.dataframe(display_df, use_container_width=True, height=800)

# 탭 2: 흥행 분석

with tab2:
    st.header("🎯 흥행 성공률 분석")
    
    criteria_map = {
        "ROI 3.0 이상": ("ROI3.0이상(%)", "ROI중앙값"),
        "블록버스터 (1억불)": ("블록버스터(%)", "메가히트(%)"),
        "메가 히트 (2억불)": ("메가히트(%)", "블록버스터(%)"),
        "작품성 (평점 7.0)": ("작품성7.0이상(%)", "평균평점")
    }
    
    primary_col, secondary_col = criteria_map[success_criteria]
    success_stats = director_stats.sort_values(primary_col, ascending=False).head(20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top 20 감독 - {success_criteria}")
        display_cols = ['작품수', primary_col, secondary_col, '주요장르', '총수익']
        display_df = success_stats[display_cols].copy()
        display_df['총수익'] = (display_df['총수익'] / 1e6).round(1).astype(str) + 'M'
        display_df.index.name = "감독"
        st.dataframe(display_df, use_container_width=True, height=600)
    
    with col2:
        fig = px.bar(
            success_stats.head(20),
            x=primary_col,
            y=success_stats.head(20).index,
            orientation='h',
            labels={primary_col: "성공률 (%)", "감독": "감독"},
        )
        fig.update_layout(height=700, yaxis={'categoryorder':'total ascending'}, yaxis_title="감독")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("흥행·작품성 균형 감독 (블록버스터 50% + 작품성 50%)")
    balanced = director_stats[
        (director_stats['블록버스터(%)'] >= 50) & 
        (director_stats['작품성7.0이상(%)'] >= 50)
    ].sort_values('총수익', ascending=False).head(15)
    
    if len(balanced) > 0:
        display_cols = ['작품수', '블록버스터(%)', '작품성7.0이상(%)', '주요장르', '총수익', '평균평점']
        display_df = balanced[display_cols].copy()
        display_df['총수익'] = (display_df['총수익'] / 1e6).round(1).astype(str) + 'M'
        display_df.index.name = "감독"
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("해당 조건을 만족하는 감독이 없습니다.")

# 탭 3: 장르 분석

with tab3:
    st.header("🎨 감독별 장르 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("장르 스페셜리스트 (집중형)")
        specialists = director_stats.sort_values('장르다양성', ascending=True).head(15)
        display_cols = ['작품수', '장르다양성', '주요장르', '총수익', '평균평점']
        display_df = specialists[display_cols].copy()
        display_df['총수익'] = (display_df['총수익'] / 1e6).round(1).astype(str) + 'M'
        display_df.index.name = "감독"
        st.dataframe(display_df, use_container_width=True)
    
    with col2:
        st.subheader("장르 제너럴리스트 (다양형)")
        generalists = director_stats.sort_values('장르다양성', ascending=False).head(15)
        display_cols = ['작품수', '장르다양성', '주요장르', '총수익', '평균평점']
        display_df = generalists[display_cols].copy()
        display_df['총수익'] = (display_df['총수익'] / 1e6).round(1).astype(str) + 'M'
        display_df.index.name = "감독"
        st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Top 10 감독 장르 매트릭스")
    
    top_10_directors = director_stats.sort_values('총수익', ascending=False).head(10).index
    director_genre_detail = df_full[df_full['director'].isin(top_10_directors)].explode('genre_list').groupby(['director', 'genre_list']).size().reset_index(name='작품수')
    director_genre_pivot = director_genre_detail.pivot(index='director', columns='genre_list', values='작품수').fillna(0)
    
    fig = px.imshow(
        director_genre_pivot,
        labels=dict(x="장르", y="감독", color="작품 수"),
        color_continuous_scale="Greens",
        aspect="auto"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# 탭 4: 개별 감독 프로필

with tab4:
    st.header("👤 개별 감독 상세 분석")
    
    director_list = sorted(director_stats.index.tolist())
    
    if len(director_list) > 0:
        selected_director = st.selectbox("감독 선택", director_list, index=0)
        
        if selected_director:
            director_movies = df_full[df_full['director'] == selected_director].copy()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("총 작품 수", f"{len(director_movies)}편")
            with col2:
                st.metric("총 수익", f"${director_movies['revenue'].sum()/1e6:.1f}M")
            with col3:
                st.metric("평균 평점", f"{director_movies['vote_average'].mean():.2f}")
            with col4:
                st.metric("평균 ROI", f"{director_movies['ROI'].mean():.2f}")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("장르별 작품 비율")
                genre_counts = director_movies.explode('genre_list')['genre_list'].value_counts()
                fig = px.pie(
                    values=genre_counts.values,
                    names=genre_counts.index,
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("연도별 수익")
                yearly_revenue = director_movies.groupby('release_year')['revenue'].sum().reset_index()
                fig = px.line(
                    yearly_revenue,
                    x='release_year',
                    y='revenue',
                    markers=True,
                )
                fig.update_layout(xaxis_title="연도", yaxis_title="수익 ($)")
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📽️ 작품 목록 (수익 순)")
            movies_display = director_movies[['title', 'release_year', 'revenue', 'budget', 'ROI', 'vote_average']].copy()
            movies_display['revenue'] = (movies_display['revenue'] / 1e6).round(1)
            movies_display['budget'] = (movies_display['budget'] / 1e6).round(1)
            movies_display['ROI'] = movies_display['ROI'].round(2)
            movies_display = movies_display.sort_values('revenue', ascending=False)
            movies_display.columns = ['제목', '개봉연도', '수익(M$)', '예산(M$)', 'ROI', '평점']

            # 상세 테이블 인덱스 조정
            movies_display = movies_display.reset_index(drop=True)
            movies_display.index += 1
            movies_display.index.name = "목록"

            st.dataframe(movies_display, use_container_width=True, height=400)
    else:
        st.warning("조건을 만족하는 감독이 없습니다.")