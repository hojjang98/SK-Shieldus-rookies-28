import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import openai


load_dotenv(r"C:\Users\ghwns\movie_project\.env")

def get_openai_client():
    """OpenAI API 클라이언트 설정"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")
    
    openai.api_key = api_key
    return openai


def get_rag_movie_recommendation(collection, user_query, n_results=5):
    """
    RAG (Retrieval-Augmented Generation) 기반 영화 추천
    
    Args:
        collection: ChromaDB 컬렉션
        user_query (str): 사용자 질문
        n_results (int): 추천 영화 수
    
    Returns:
        dict: {"explanation": str, "movies": list}
    """
    try:
        # Vector DB에서 관련 영화 검색
        results = collection.query(
            query_texts=[user_query],
            n_results=n_results
        )
        
        if not results or not results['metadatas'][0]:
            return {
                "explanation": "죄송합니다. 관련된 영화를 찾을 수 없습니다. 다른 조건으로 검색해보시겠어요?",
                "movies": []
            }
        
        # 검색된 영화 정보를 Document 형태로 변환
        movies = []
        documents_text = []
        
        for metadata in results['metadatas'][0]:
            movie_info = {
                'title': metadata['title'],
                'genres': metadata['genres'],
                'vote_average': metadata['vote_average'],
                'vote_count': metadata['vote_count'],
                'runtime': metadata['runtime'],
                'overview': metadata['overview'],
                'poster_path': metadata['poster_path'],
                'release_date': metadata.get('release_date', '')
            }
            movies.append(movie_info)
            
            # RAG를 위한 텍스트 컨텍스트 구성
            doc_text = f"""
            영화 제목: {metadata['title']}
            장르: {metadata['genres']}
            평점: {metadata['vote_average']}/10 (투표 수: {metadata['vote_count']:,})
            런타임: {metadata['runtime']}분
            줄거리: {metadata['overview']}
            개봉일: {metadata.get('release_date', 'N/A')}
            """
            documents_text.append(doc_text)
        
        # LangChain LLM 설정
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # RAG 프롬프트 구성
        context = "\n\n---\n\n".join(documents_text)
        
        prompt = f"""당신은 친절한 영화 추천 전문가입니다.

                사용자 요청: "{user_query}"

                검색된 영화 정보:
                {context}

                위 영화들을 바탕으로 다음 내용을 포함하여 추천 설명을 작성해주세요:

                1. 사용자 요청과 추천 영화들의 연관성
                2. 각 영화의 주요 특징 (장르, 평점, 분위기 등)
                3. 왜 이 영화들을 추천하는지 구체적인 이유

                답변은 3-5문장으로 작성하고, 자연스럽고 친근한 말투로 작성해주세요.
                
                """

        messages = [
            SystemMessage(content="당신은 영화 데이터베이스를 기반으로 정확하고 유용한 영화 추천을 제공하는 전문가입니다."),
            HumanMessage(content=prompt)
        ]
        
        # LLM으로 설명 생성 
        response = llm.invoke(messages)
        explanation = response.content
        
        return {
            "explanation": explanation,
            "movies": movies
        }
    
    except Exception as e:
        return {
            "explanation": f"추천 생성 중 오류가 발생했습니다: {str(e)}",
            "movies": []
        }


def get_conversational_rag_response(collection, user_message, chat_history):
    """
    대화형 RAG - 이전 대화 컨텍스트를 고려한 영화 추천
    
    Args:
        collection: ChromaDB 컬렉션
        user_message (str): 사용자 최신 메시지
        chat_history (list): 이전 대화 기록 [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        dict: {"response": str, "movies": list}
    """
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # 대화 히스토리를 문자열로 변환
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in chat_history[-5:]  # 최근 5개만
        ])
        
        # 사용자 의도 파악 및 검색 쿼리 추출
        intent_prompt = f"""이전 대화:
                        {history_text}

                        최신 사용자 메시지: "{user_message}"

                        사용자가 영화 추천을 원하는지 판단하고, 원한다면 검색에 적합한 키워드를 추출해주세요.

                        형식:
                        - 영화 추천 요청인 경우: RECOMMEND|검색키워드
                        - 일반 대화인 경우: CHAT|응답내용
                        """

        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent_result = intent_response.content.strip()
        
        # 의도에 따라 처리
        if intent_result.startswith("RECOMMEND"):
            # 검색 쿼리 추출
            search_query = intent_result.split("|")[1] if "|" in intent_result else user_message
            
            # RAG 영화 추천
            recommendation = get_rag_movie_recommendation(collection, search_query, n_results=5)
            
            return {
                "response": recommendation["explanation"],
                "movies": recommendation["movies"]
            }
        
        else:
            # 일반 대화
            chat_prompt = f"""이전 대화:
                        {history_text}

                        사용자: {user_message}

                        당신은 친근한 영화 애호가입니다. 위 대화 맥락을 고려하여 자연스럽게 답변해주세요.
                        """
            
            chat_response = llm.invoke([HumanMessage(content=chat_prompt)])
            
            return {
                "response": chat_response.content,
                "movies": []
            }
    
    except Exception as e:
        return {
            "response": f"오류가 발생했습니다: {str(e)}",
            "movies": []
        }


def analyze_movie_success_openai(movie_data):
    """
    OpenAI로 영화 흥행 분석
    """
    client = get_openai_client()
    
    prompt = f"""다음 영화의 흥행 요인을 분석해주세요:

            제목: {movie_data['title']}
            장르: {movie_data['genres']}
            예산: ${movie_data.get('budget', 0):,.0f}
            수익: ${movie_data.get('revenue', 0):,.0f}
            이익: ${movie_data.get('profit', 0):,.0f}
            ROI: {movie_data.get('ROI', 0):.2f}배
            평점: {movie_data['vote_average']}/10
            관객수: {movie_data['vote_count']:,}명
            런타임: {movie_data['runtime']}분
            개봉연도: {movie_data.get('release_year', 'N/A')}

            이 영화의 흥행 성공/실패 요인을 3가지로 분석해주세요.
            """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 영화 산업 분석 전문가입니다. 데이터를 바탕으로 영화의 흥행 요인을 분석해주세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"OpenAI API 호출 실패: {str(e)}")