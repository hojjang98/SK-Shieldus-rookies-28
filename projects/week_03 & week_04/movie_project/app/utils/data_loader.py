import pandas as pd
from pathlib import Path
import os

def load_movie_data():
    """
    영화 데이터 로드
    """
    # 여러 경로 시도
    possible_paths = [
        Path(__file__).parent.parent.parent / "data" / "tmdb_cleaned.csv",  # 프로젝트 루트
        Path("data/tmdb_cleaned.csv"),  # 상대 경로
        Path("../data/tmdb_cleaned.csv"),  # 상위 폴더
    ]
    
    for data_path in possible_paths:
        if data_path.exists():
            df = pd.read_csv(data_path)
            return df
    
    raise FileNotFoundError(f"tmdb_cleaned.csv를 찾을 수 없습니다. 확인한 경로: {[str(p) for p in possible_paths]}")

def load_recommendation_data():
    """
    추천 시스템용 데이터 로드 (필요한 컬럼만)
    """
    df = load_movie_data()
    
    df_rec = df[['id', 'title', 'overview', 'genres', 'keywords', 
                 'vote_average', 'vote_count', 'release_date', 
                 'runtime', 'original_language', 'poster_path']].copy()
    
    return df_rec

def get_poster_url(poster_path):
    """
    TMDB 포스터 URL 생성
    """
    if pd.isna(poster_path) or poster_path == '':
        return None
    
    base_url = "https://image.tmdb.org/t/p/w500"
    return f"{base_url}{poster_path}"