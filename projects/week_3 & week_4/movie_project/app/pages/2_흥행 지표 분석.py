import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# 상위 디렉토리의 utils 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_movie_data, get_poster_url

# 페이지 설정
st.set_page_config(
    page_title="흥행 지표 분석",
    page_icon="💰",
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
st.title("💰 흥행 지표 분석")
st.markdown("성공한 영화들의 패턴을 분석하고 AI로 흥행 요인을 파악합니다!")

# 데이터 로드
@st.cache_data
def load_data():
    df = load_movie_data()
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    return df

try:
    df = load_data()
    
    # Budget과 Revenue가 있는 데이터만 필터링
    df_full = df[df['budget'].notna() & df['revenue'].notna()].copy()
    df_full = df_full[df_full['budget'] > 1000]
    df_full = df_full[df_full['revenue'] > 1000]
    
    # ROI 계산
    df_full['ROI'] = (df_full['revenue'] - df_full['budget']) / df_full['budget']
    df_full['profit'] = df_full['revenue'] - df_full['budget']
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Top 영화", 
        "📈 투자 수익률 (ROI) 분석", 
        "🎯 성공 공식",
        "🧐 AI 분석"
    ])
    
    # 탭 1: Top 영화
    with tab1:
        st.header("🏆 Top 영화 분석")
        
        # 정렬 기준 선택
        sort_option = st.selectbox(
            "정렬 기준 선택",
            ["수익 (Revenue)", "투자 수익률(ROI)", "평점 (Rating)", "이익 (Profit)"]
        )
        
        if sort_option == "수익 (Revenue)":
            sort_col = 'revenue'
        elif sort_option == "투자 수익률(ROI)":
            sort_col = 'ROI'
        elif sort_option == "평점 (Rating)":
            sort_col = 'vote_average'
        else:
            sort_col = 'profit'
        
        top_n = st.slider("표시할 영화 개수", 5, 50, 20)
        
        top_movies = df_full.nlargest(top_n, sort_col)
        
        # 차트 표시
        st.subheader(f"Top {top_n} 영화 ({sort_option})")
        
        fig = px.bar(
            top_movies.head(top_n),
            x=sort_col,
            y='title',
            orientation='h',
            labels={sort_col: sort_option, 'title': '영화 제목'},
            color=sort_col,
            color_continuous_scale='YlOrRd'
        )
        fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
        
        # 상세 테이블
        st.subheader("상세 정보")
        display_df = top_movies[['title', 'revenue', 'budget', 'profit', 'ROI', 
                                  'vote_average', 'vote_count', 'release_year']].copy()
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x/1e6:.1f}M")
        display_df['budget'] = display_df['budget'].apply(lambda x: f"${x/1e6:.1f}M")
        display_df['profit'] = display_df['profit'].apply(lambda x: f"${x/1e6:.1f}M")
        display_df['ROI'] = display_df['ROI'].apply(lambda x: f"{x:.2f}x")
        display_df.columns = ['제목', '수익', '예산', '이익', 'ROI', '평점', '투표수', '개봉년도']

        # 상세 테이블 인덱스 조정
        display_df = display_df.reset_index(drop=True)
        display_df.index += 1
        display_df.index.name = "순위"
        
        st.dataframe(display_df, use_container_width=True, height=400)
    
    # 탭 2: ROI 분석
    with tab2:
        st.header("📈 투자 수익률(ROI) 분석")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("평균 ROI", f"{df_full['ROI'].mean():.2f}x")
        
        with col2:
            st.metric("중위 ROI", f"{df_full['ROI'].median():.2f}x")
        
        with col3:
            profitable = len(df_full[df_full['ROI'] > 0])
            st.metric("수익 영화", f"{profitable:,}편 ({profitable/len(df_full)*100:.1f}%)")
        
        with col4:
            st.metric("최고 ROI", f"{df_full['ROI'].max():.2f}x")
        
        st.markdown("---")
        
        # ROI 분포
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ROI 분포")
            roi_filtered = df_full[df_full['ROI'] < df_full['ROI'].quantile(0.95)]
            fig = px.histogram(
                roi_filtered,
                x='ROI',
                nbins=50,
                labels={'ROI': 'ROI', 'count': '영화 수'}
            )
            fig.add_vline(x=roi_filtered['ROI'].median(), line_dash="dash", 
                         line_color="red", annotation_text="Median", annotation_position="top")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Budget vs Revenue")
            sample_df = df_full.sample(min(1000, len(df_full)))
            fig = px.scatter(
                sample_df,
                x='budget',
                y='revenue',
                color='ROI',
                hover_data=['title'],
                labels={'budget': '예산', 'revenue': '수익'},
                color_continuous_scale='RdYlGn',
                log_x=True,
                log_y=True
            )
            # Break-even line
            fig.add_trace(go.Scatter(
                x=[sample_df['budget'].min(), sample_df['budget'].max()],
                y=[sample_df['budget'].min(), sample_df['budget'].max()],
                mode='lines',
                name='Break-even',
                line=dict(color='red', dash='dash')
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        # 예산 구간별 ROI
        st.subheader("예산 구간별 평균 ROI")
        df_full['budget_range'] = pd.cut(
            df_full['budget'], 
            bins=[0, 1e6, 5e6, 20e6, 50e6, 100e6, 1e9],
            labels=['$1M', '$1-5M', '$5-20M', '$20-50M', '$50-100M', '$100M']
        )
        
        roi_by_budget = df_full.groupby('budget_range').agg({
            'ROI': ['mean', 'median', 'count']
        }).round(2)
        roi_by_budget.columns = ['평균 ROI', '중위 ROI', '영화 수']
        roi_by_budget = roi_by_budget.rename_axis("예산 구간")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=roi_by_budget.index.astype(str),
            y=roi_by_budget['평균 ROI'],
            name='평균 ROI',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Scatter(
            x=roi_by_budget.index.astype(str),
            y=roi_by_budget['중위 ROI'],
            name='중위 ROI',
            mode='lines+markers',
            marker_color='red'
        ))
        fig.update_layout(
            xaxis_title="예산 구간",
            yaxis_title="ROI",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(roi_by_budget, use_container_width=True)
    
    # 탭 3: 성공 공식
    with tab3:
        st.header("🎯 성공 영화의 공식")
        
        # Top 10% 영화 분석
        top_10_threshold = df_full['revenue'].quantile(0.9)
        success_movies = df_full[df_full['revenue'] >= top_10_threshold].copy()
        
        st.subheader(f"Top 10% 영화 분석 (수익 ${top_10_threshold/1e6:.1f}M 이상)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("영화 수", f"{len(success_movies):,}편")
        
        with col2:
            st.metric("평균 예산", f"${success_movies['budget'].mean()/1e6:.1f}M")
        
        with col3:
            st.metric("평균 수익", f"${success_movies['revenue'].mean()/1e6:.1f}M")
        
        with col4:
            st.metric("평균 ROI", f"{success_movies['ROI'].mean():.2f}x")
        
        st.markdown("---")
        
        # 장르 분석
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 장르")
            success_movies['genre_list'] = success_movies['genres'].str.split(', ')
            success_genres = success_movies.explode('genre_list')['genre_list'].value_counts().head(10)
            
            fig = px.bar(
                x=success_genres.values,
                y=success_genres.index,
                orientation='h',
                title="Most Common Genres in Top 10% Movies",
                labels={'x': '영화 수', 'y': '장르'}
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 국가")
            success_movies['country_list'] = success_movies['production_countries'].str.split(', ')
            success_countries = success_movies.explode('country_list')['country_list'].value_counts().head(10)
            
            fig = px.bar(
                x=success_countries.values,
                y=success_countries.index,
                orientation='h',
                title="Most Common Countries in Top 10% Movies",
                labels={'x': '영화 수', 'y': '국가'}
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        
        # 특징 비교
        st.subheader("성공 영화 vs 일반 영화 비교")
        
        comparison_df = pd.DataFrame({
            '지표': ['평균 예산', '평균 수익', '평균 ROI', '평균 평점', '평균 런타임'],
            'Top 10% 영화': [
                f"${success_movies['budget'].mean()/1e6:.1f}M",
                f"${success_movies['revenue'].mean()/1e6:.1f}M",
                f"{success_movies['ROI'].mean():.2f}x",
                f"{success_movies['vote_average'].mean():.2f}",
                f"{success_movies['runtime'].mean():.0f}분"
            ],
            '전체 영화': [
                f"${df_full['budget'].mean()/1e6:.1f}M",
                f"${df_full['revenue'].mean()/1e6:.1f}M",
                f"{df_full['ROI'].mean():.2f}x",
                f"{df_full['vote_average'].mean():.2f}",
                f"{df_full['runtime'].mean():.0f}분"
            ]
        })
        
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # 인사이트 요약
        st.markdown("---")
        st.subheader("핵심 인사이트")
        
        st.markdown(f"""
        **성공 영화의 특징:**
        
        1. **예산**: 평균 ${success_movies['budget'].mean()/1e6:.1f}M (전체 평균의 {success_movies['budget'].mean()/df_full['budget'].mean():.1f}배)
        2. **장르**: {success_genres.index[0]}, {success_genres.index[1]}, {success_genres.index[2]} 장르가 많음
        3. **제작국**: {success_countries.index[0]}에서 {len(success_movies[success_movies['production_countries'].str.contains(success_countries.index[0], na=False)])}편 제작
        4. **평점**: 평균 {success_movies['vote_average'].mean():.2f}/10
        5. **런타임**: 평균 {success_movies['runtime'].mean():.0f}분
        """)
    
    # 탭 4: AI 분석
    with tab4:
        st.header("🧐 AI 기반 영화 흥행 분석")
        st.markdown("AI가 특정 영화의 흥행 요인을 분석합니다.")
        
        # 영화 선택
        st.subheader("분석할 영화 선택")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 드롭다운으로 영화 선택
            movie_list = df_full.nlargest(100, 'revenue')['title'].tolist()
            selected_movie_title = st.selectbox(
                "영화 선택 (Top 100 수익 영화)",
                movie_list
            )
        
        with col2:
            st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
            analyze_button = st.button("AI 분석 시작", type="primary", use_container_width=True)
        
        if analyze_button:
            # 선택한 영화 정보
            movie_data = df_full[df_full['title'] == selected_movie_title].iloc[0]
            
            # 영화 정보 표시
            st.markdown("---")
            st.subheader(f"📽️ {movie_data['title']}")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                poster_url = get_poster_url(movie_data['poster_path'])
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x450?text=No+Poster", 
                           use_container_width=True)
            
            with col2:
                st.markdown(f"**장르**: {movie_data['genres']}")
                st.markdown(f"**개봉일**: {movie_data['release_date']}")
                st.markdown(f"**예산**: ${movie_data['budget']/1e6:.1f}M")
                st.markdown(f"**수익**: ${movie_data['revenue']/1e6:.1f}M")
                st.markdown(f"**이익**: ${movie_data['profit']/1e6:.1f}M")
                st.markdown(f"**ROI**: {movie_data['ROI']:.2f}x")
                st.markdown(f"**평점**: ⭐ {movie_data['vote_average']}/10 ({movie_data['vote_count']:,}명)")
                st.markdown(f"**런타임**: {movie_data['runtime']}분")
            
            with col3:
                # 성공 지표
                st.metric("수익 순위", 
                         f"{(df_full['revenue'] > movie_data['revenue']).sum() + 1}위")
                st.metric("ROI 순위", 
                         f"{(df_full['ROI'] > movie_data['ROI']).sum() + 1}위")
                
                if movie_data['revenue'] >= top_10_threshold:
                    st.success("🏆 Top 10% 영화")
                else:
                    st.info("📊 일반 영화")
            
            # AI 분석
            st.markdown("---")
            st.subheader("AI 분석 결과")
            
            try:
                from utils.llm_utils import analyze_movie_success_openai
                
                with st.spinner("OpenAI가 분석 중입니다..."):
                    analysis = analyze_movie_success_openai(movie_data.to_dict())
                
                st.markdown(analysis)
                
            except Exception as e:
                st.error(f"AI 분석 중 오류 발생: {str(e)}")
                st.info("💡 OpenAI API 키가 설정되어 있는지 확인해주세요. (.env 파일의 OPENAI_API_KEY)")
        
        else:
            st.info("👆 영화를 선택하고 'AI 분석 시작' 버튼을 눌러주세요!")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.info("data/tmdb_cleaned.csv 파일이 존재하는지 확인해주세요.")

# 사이드바
with st.sidebar:
    st.markdown("### 📊 분석 정보")
    try:
        st.info(f"분석 대상: {len(df_full):,}편")
        st.info(f"평균 ROI: {df_full['ROI'].mean():.2f}x")
    except:
        pass
    
    st.markdown("---")
    st.markdown("### 💡 주요 기능")
    st.markdown("""
    - Top 영화 랭킹
    - ROI 패턴 분석
    - 성공 공식 도출
    - AI 흥행 요인 분석
    """)