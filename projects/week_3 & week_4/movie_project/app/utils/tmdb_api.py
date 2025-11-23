import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class TMDBClient:
    """TMDB API 클라이언트 (한국어 설정 적용)"""
    
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"
        # 공통 파라미터: 한국어 설정
        self.default_params = {
            'api_key': self.api_key,
            'language': 'ko-KR',  # 결과 언어를 한국어로
            'region': 'KR'        # 개봉일 기준을 한국으로
        }
    
    def get_trending_movies(self, time_window='week'):
        """최신 인기 영화 (한국 기준)"""
        url = f"{self.base_url}/trending/movie/{time_window}"
        
        try:
            response = requests.get(url, params=self.default_params)
            response.raise_for_status()
            return response.json()['results']
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return []
    
    def get_upcoming_movies(self):
        """개봉 예정 영화 (한국 상영 기준)"""
        url = f"{self.base_url}/movie/upcoming"
        
        try:
            response = requests.get(url, params=self.default_params)
            response.raise_for_status()
            return response.json()['results']
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return []
    
    def get_movie_details(self, movie_id):
        """영화 상세 정보"""
        url = f"{self.base_url}/movie/{movie_id}"
        # 상세 정보 요청 시에는 append_to_response 유지하면서 한국어 파라미터 병합
        params = self.default_params.copy()
        params['append_to_response'] = 'credits,keywords'
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return None
    
    def search_movies_by_genre(self, genre_id, year=None):
        """장르별 영화 검색"""
        url = f"{self.base_url}/discover/movie"
        params = self.default_params.copy()
        params.update({
            'with_genres': genre_id,
            'sort_by': 'revenue.desc'
        })
        
        if year:
            params['primary_release_year'] = year
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()['results']
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return []