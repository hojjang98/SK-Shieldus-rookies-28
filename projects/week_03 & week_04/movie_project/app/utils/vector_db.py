import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path

# 환경변수 로드
load_dotenv()

@st.cache_resource
def load_vector_db():
    """Vector DB 로드 (캐싱)"""
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            st.error("❌ OPENAI_API_KEY가 .env 파일에 없습니다!")
            return None
        
        # Embedding Function 생성
        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-ada-002"
        )
        
        # 두 경로 모두 시도
        possible_paths = [
            Path("../vector_db/chroma_db"),  # 프로젝트 루트
            Path("vector_db/chroma_db"),     # app 폴더 내부
        ]
        
        db_path = None
        for path in possible_paths:
            if path.exists():
                db_path = path
                break
        
        if db_path is None:
            st.error("❌ Vector DB를 찾을 수 없습니다!")
            st.code(f"시도한 경로:\n" + "\n".join([str(p.absolute()) for p in possible_paths]))
            st.info("💡 notebooks/Movie_Analysis.ipynb를 실행하여 Vector DB를 생성해주세요!")
            return None
        
        # ChromaDB 클라이언트 생성
        chroma_client = chromadb.PersistentClient(path=str(db_path))
        
        # 컬렉션 확인
        collections = chroma_client.list_collections()
        collection_names = [c.name for c in collections]
        
        if not collections or "movies" not in collection_names:
            st.error("❌ 'movies' 컬렉션이 없습니다!")
            st.info(f"📂 사용 가능한 컬렉션: {collection_names}")
            return None
        
        # 컬렉션 로드
        collection = chroma_client.get_collection(
            name="movies",
            embedding_function=embedding_function
        )
        
        return collection
        
    except Exception as e:
        st.error(f"❌ Vector DB 로드 실패: {e}")
        st.exception(e)
        return None


def search_similar_movies(collection, query, n_results=5):
    """
    쿼리와 유사한 영화 검색
    
    Args:
        collection: ChromaDB 컬렉션
        query (str): 검색 쿼리
        n_results (int): 반환할 결과 수
    
    Returns:
        dict or None: 검색 결과
    """
    if collection is None:
        st.warning("⚠️ Vector DB가 로드되지 않았습니다!")
        return None
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        st.error(f"❌ 검색 오류: {e}")
        return None


def recommend_by_movie_title(collection, movie_title, n_results=6):
    """
    특정 영화와 유사한 영화 추천
    
    Args:
        collection: ChromaDB 컬렉션
        movie_title (str): 기준 영화 제목
        n_results (int): 반환할 결과 수
    
    Returns:
        dict or None: 추천 결과
    """
    if collection is None:
        st.warning("⚠️ Vector DB가 로드되지 않았습니다!")
        return None
    
    try:
        results = collection.query(
            query_texts=[movie_title],
            n_results=n_results
        )
        return results
    except Exception as e:
        st.error(f"❌ 추천 오류: {e}")
        return None


def get_movie_by_title(collection, movie_title, n_results=1):
    """
    영화 제목으로 검색
    
    Args:
        collection: ChromaDB 컬렉션
        movie_title (str): 검색할 영화 제목
        n_results (int): 반환할 결과 수
    
    Returns:
        dict or None: 검색 결과
    """
    if collection is None:
        st.warning("⚠️ Vector DB가 로드되지 않았습니다!")
        return None
    
    try:
        results = collection.query(
            query_texts=[movie_title],
            n_results=n_results
        )
        return results
    except Exception as e:
        st.error(f"❌ 영화 검색 오류: {e}")
        return None


def search_by_filters(collection, genres=None, min_rating=0.0, max_rating=10.0, 
                     min_year=None, max_year=None, n_results=10):
    """
    필터를 사용한 영화 검색
    
    Args:
        collection: ChromaDB 컬렉션
        genres (list): 장르 리스트
        min_rating (float): 최소 평점
        max_rating (float): 최대 평점
        min_year (int): 최소 개봉 연도
        max_year (int): 최대 개봉 연도
        n_results (int): 반환할 결과 수
    
    Returns:
        dict or None: 검색 결과
    """
    if collection is None:
        st.warning("⚠️ Vector DB가 로드되지 않았습니다!")
        return None
    
    try:
        # where 필터 구성
        where_filter = {
            "$and": [
                {"vote_average": {"$gte": min_rating}},
                {"vote_average": {"$lte": max_rating}}
            ]
        }
        
        # 연도 필터 추가
        if min_year:
            where_filter["$and"].append(
                {"release_date": {"$gte": f"{min_year}-01-01"}}
            )
        if max_year:
            where_filter["$and"].append(
                {"release_date": {"$lte": f"{max_year}-12-31"}}
            )
        
        # 장르 필터 추가
        if genres and len(genres) > 0:
            genre_filter = {
                "$or": [{"genres": {"$contains": genre}} for genre in genres]
            }
            where_filter["$and"].append(genre_filter)
        
        # 검색 실행
        results = collection.get(
            where=where_filter,
            limit=n_results
        )
        
        return results
        
    except Exception as e:
        st.error(f"❌ 필터 검색 오류: {e}")
        return None