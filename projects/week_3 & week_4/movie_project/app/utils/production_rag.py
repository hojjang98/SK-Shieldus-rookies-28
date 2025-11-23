import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.tmdb_api import TMDBClient
import pandas as pd

load_dotenv()


class ProductionRAG:
    """영화 제작사용 RAG 시스템 (극도로 보수적 분석 특화)"""
    
    def __init__(self, collection, df):
        """
        Args:
            collection: ChromaDB 컬렉션 (내부 DB)
            df: 영화 데이터프레임 (예산/수익 정보)
        """
        self.collection = collection
        self.df = df
        self.tmdb_client = TMDBClient()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,  
            api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def analyze_production_proposal(self, proposal):
        """
        영화 기획안 분석 메인 함수
        """
        try:
            # 내부 DB에서 유사 영화 검색 (샘플 수 증가)
            search_query = f"{proposal['genre']} {proposal.get('synopsis', '')}"
            internal_results = self.collection.query(
                query_texts=[search_query],
                n_results=30  
            )
            
            # 내부 데이터에서 재무 정보 추출 (0원 데이터 제거)
            similar_movies_data = self._extract_financial_data(internal_results)
            
            # TMDB API로 최신 시장 트렌드 수집
            market_trends = self._get_market_trends(proposal['genre'])
            
            # 유사 영화 성과 분석 
            performance_analysis = self._analyze_similar_performance(
                similar_movies_data,
                proposal['budget'],
                proposal.get('synopsis', '')  #
            )
            
            # LLM으로 종합 분석 리포트 생성
            comprehensive_analysis = self._generate_production_analysis(
                proposal,
                similar_movies_data,
                market_trends,
                performance_analysis
            )
            
            return {
                "success": True,
                "analysis": comprehensive_analysis,
                "similar_movies": similar_movies_data,
                "market_trends": market_trends,
                "performance_metrics": performance_analysis
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_financial_data(self, search_results):
        """내부 DB 결과에서 재무 데이터 추출 (🔥 0원 데이터 필터링)"""
        movies_data = []
        
        if not search_results or 'metadatas' not in search_results or not search_results['metadatas']:
            return []

        for metadata in search_results['metadatas'][0]:
            movie_title = metadata.get('title')
            
            # 원본 데이터프레임에서 재무 정보 매핑
            movie_info = self.df[self.df['title'] == movie_title]
            
            if not movie_info.empty:
                movie_row = movie_info.iloc[0]
                
                budget = movie_row.get('budget', 0) if pd.notna(movie_row.get('budget')) else 0
                revenue = movie_row.get('revenue', 0) if pd.notna(movie_row.get('revenue')) else 0
                
                # 예산이나 수익이 0 이하면 노이즈 데이터로 간주하여 제외
                if budget <= 0 or revenue <= 0:
                    continue
                
                movies_data.append({
                    'title': movie_row.get('title'),
                    'genre': metadata.get('genres'),
                    'budget': budget,
                    'revenue': revenue,
                    'profit': revenue - budget,
                    'roi': revenue / budget,
                    'vote_average': metadata.get('vote_average', 0),
                    'vote_count': metadata.get('vote_count', 0),
                    'runtime': metadata.get('runtime', 0),
                    'release_date': metadata.get('release_date', '')
                })
        
        return movies_data
    
    def _get_market_trends(self, genre):
        """TMDB API로 최신 시장 트렌드 수집"""
        try:
            trends = {
                'trending': self.tmdb_client.get_trending_movies(),
                'upcoming': self.tmdb_client.get_upcoming_movies()
            }
            
            filtered_trends = []
            for movie in trends['trending'][:5]:
                filtered_trends.append({
                    'title': movie.get('title'),
                    'popularity': movie.get('popularity'),
                    'vote_average': movie.get('vote_average'),
                    'release_date': movie.get('release_date')
                })
            
            return filtered_trends
        except Exception as e:
            print(f"Market trends error: {e}")
            return []
    
    def _calculate_commercial_score(self, synopsis):
        """
        시놉시스 기반 상업성 점수 계산 (현실적 페널티)
        반환값: (점수 계수 0.4~1.0, 발견된 독소 키워드 리스트)
        """
        if not synopsis:
            return 1.0, []

        # 상업성 주의 키워드 (심각한 것만 선별)
        caution_keywords = [
            # 치명적 독소 (확실히 위험한 것만)
            "대사가 없는", "no dialogue", "실험적", "experimental", 
            "다큐멘터리", "documentary", 
            "흑백", "black and white", "롱테이크", "long take",
            "관조적", "철학적", "philosophical",
            
            # 중간 수준 주의
            "무대극", "stage play", "모노드라마", "monodrama",
            "독백", "monologue", "회고록", "memoir",
            "관념적", "abstract", "초현실", "surreal",
            "전위", "avant-garde", "미니멀", "minimal"
        ]
        
        penalty_factor = 1.0
        found_poisons = []
        synopsis_lower = synopsis.lower()
        
        for word in caution_keywords:
            if word in synopsis_lower:
                # 키워드 하나당 기대 수익 20% 삭감 (0.8 곱하기) - 40%에서 완화
                penalty_factor *= 0.8
                found_poisons.append(word)
        
        # 최소 보장치를 40%로 상향 (극단적 경우도 어느정도 기회 부여)
        return max(penalty_factor, 0.4), found_poisons

    def _analyze_similar_performance(self, similar_movies, proposed_budget, synopsis=""):
        """
        유사 영화 성과 분석 (현실적 보수 + 균형잡힌 페널티)
        """
        if not similar_movies:
            return None
        
        # 장르 전체 평균 예산 계산
        all_budgets = [m['budget'] for m in similar_movies]
        avg_genre_budget = sum(all_budgets) / len(all_budgets) if all_budgets else 0

        # 예산 범위별 필터링 (±50%)
        budget_range = (proposed_budget * 0.5, proposed_budget * 1.5)
        similar_subset = [
            m for m in similar_movies 
            if budget_range[0] <= m.get('budget', 0) <= budget_range[1]
        ]
        
        # 범위 내 영화가 3개 미만이면 전체 유사 영화 사용
        if len(similar_subset) < 3:
            similar_subset = similar_movies[:15]
        
        # 통계 데이터 추출
        revenues = [m['revenue'] for m in similar_subset]
        rois = [m['roi'] for m in similar_subset]
        
        if not revenues:
            return None

        # [페널티 1] 상업성 점수 계산 (완화됨)
        commercial_factor, poison_words = self._calculate_commercial_score(synopsis)
        
        # [페널티 2] 예산 오버페이 계수 계산 (완화)
        budget_efficiency = 1.0
        if proposed_budget > avg_genre_budget * 1.5:  # 1.5배 이상일 때만 페널티
            # 예산이 평균의 2배면 효율 0.85배, 3배면 0.7배 (0.65, 0.45에서 완화)
            overpay_ratio = proposed_budget / avg_genre_budget
            budget_efficiency = 1.0 / (1.0 + (overpay_ratio - 1.5) * 0.3)  # 0.7에서 0.3으로 완화
        
        # Pandas 보수적 통계
        rev_series = pd.Series(revenues)
        roi_series = pd.Series(rois)
        
        # 기본 베이스는 하위 40% 수익 (30%에서 완화)
        conservative_base = rev_series.quantile(0.40)
        
        # 2중 페널티 적용 (예산 페널티는 심한 경우만)
        # = 보수적 베이스 × 상업성 계수 × 예산 효율 계수
        final_adjusted_revenue = conservative_base * commercial_factor * budget_efficiency
        
        # 최종 ROI = 페널티 적용된 수익 / 제안 예산
        final_adjusted_roi = final_adjusted_revenue / proposed_budget if proposed_budget > 0 else 0
        
        # BEP 경고 - ROI 2.5배
        is_profitable = final_adjusted_roi >= 2.5
        
        # 최악의 시나리오 (하위 15% 수익) - 10%에서 완화
        catastrophic_case = rev_series.quantile(0.15)

        return {
            # --- 일반 통계 (참고용) ---
            'avg_revenue': rev_series.mean(),
            'median_revenue': rev_series.median(),
            'worst_case': rev_series.min(),
            'best_case': rev_series.max(),
            'avg_roi': roi_series.mean(),
            'median_roi': roi_series.median(),
            
            # --- 핵심 지표 ---
            'conservative_revenue': conservative_base,           # 하위 40% 기준
            'adjusted_revenue': final_adjusted_revenue,          # 페널티 적용
            'adjusted_roi': final_adjusted_roi,                  # 최종 보수적 ROI
            'conservative_roi': roi_series.quantile(0.40),       # 하위 40% ROI
            'catastrophic_case': catastrophic_case,              # 최악 시나리오
            
            # --- 페널티 상세 ---
            'commercial_factor': commercial_factor,              # 상업성 계수 (0.4~1.0)
            'budget_efficiency': budget_efficiency,              # 예산 효율 (0.7~1.0)
            'poison_words': poison_words,                        # 주의 키워드
            'is_profitable': is_profitable,                      # BEP 달성 여부
            
            # --- 메타 정보 ---
            'sample_size': len(similar_subset),
            'genre_avg_budget': avg_genre_budget,
            'budget_vs_avg': proposed_budget / avg_genre_budget if avg_genre_budget > 0 else 1.0
        }

    def _generate_production_analysis(self, proposal, similar_movies, trends, performance):
        """LLM으로 종합 분석 보고서 생성 (🔥 화폐 이스케이프 처리 포함)"""
        
        # 유사 영화 정보 포맷팅 
        similar_text = "\n".join([
            f"- {m['title']}: 예산 \\${m['budget']:,.0f} → 수익 \\${m['revenue']:,.0f} (ROI: {m['roi']:.2f}배)"
            for m in similar_movies[:5]
        ]) if similar_movies else "유효한 데이터가 부족합니다."
        
        # 시장 트렌드 포맷팅
        trends_text = "\n".join([
            f"- {t['title']}: 인기도 {t['popularity']:.1f}, 평점 {t['vote_average']:.1f}"
            for t in trends[:3]
        ]) if trends else "데이터 없음"
        
        # 주의 키워드 경고 메시지
        warning_msg = ""
        if performance and performance.get('poison_words'):
            poison_str = ', '.join(performance['poison_words'])
            warning_msg = f"\n⚠️ **상업성 주의**: 시놉시스에서 흥행 리스크 키워드({poison_str})가 발견되어 수익 예측이 하향 조정되었습니다."

        # 예산 주의 경고
        budget_warning = ""
        if performance and performance.get('budget_vs_avg', 1.0) > 1.8:  # 1.5 → 1.8 (더 관대하게)
            budget_ratio = performance['budget_vs_avg']
            budget_warning = f"\n💰 **예산 주의**: 제안 예산이 장르 평균의 {budget_ratio:.1f}배입니다. 예산 효율을 고려한 조정이 필요할 수 있습니다."
        
        # 성과 지표 포맷팅
        if performance:
            perf_text = f"""
일반적 장르 기대 수익: \\${performance['median_revenue']:,.0f}
📊 **보수적 예상 수익**: \\${performance['adjusted_revenue']:,.0f} (상업성/예산 효율 반영)
⚠️ **최악의 시나리오**: \\${performance['catastrophic_case']:,.0f} (하위 15% 케이스)

일반적 장르 ROI: {performance['avg_roi']:.2f}배
📊 **보수적 예상 ROI**: {performance['adjusted_roi']:.2f}배
🎯 **손익분기 달성**: {'✅ 가능' if performance['is_profitable'] else '❌ 어려움 (ROI 2.5배 미만)'}

보수적 예측 기준(하위 40%): \\${performance['conservative_revenue']:,.0f}
최저 성과: \\${performance['worst_case']:,.0f}
분석 샘플: {performance['sample_size']}편

조정 계수:
- 상업성 계수: {performance['commercial_factor']:.0%}
- 예산 효율 계수: {performance['budget_efficiency']:.0%}
{warning_msg}
{budget_warning}
"""
        else:
            perf_text = "분석할 유효 데이터가 부족합니다."
        
        # LLM 프롬프트 구성
        prompt = f"""당신은 영화 투자 분석 전문가입니다. 다음 기획안을 현실적으로 분석해주세요.

## 기획안 정보
- 제목: {proposal.get('title', 'N/A')}
- 장르: {proposal['genre']}
- 예상 예산: \\${proposal['budget']:,.0f}
- 타겟 관객: {proposal.get('target_audience', 'N/A')}
- 시놉시스: {proposal.get('synopsis', 'N/A')}

## 유사 영화 성과 (실제 데이터 기반)
{similar_text}

## 성과 지표 (보수적 기준 적용)
{perf_text}

## 최신 시장 트렌드
{trends_text}

다음 항목을 포함하여 제작사를 위한 분석 보고서를 작성해주세요:

1. **수익 예측** (보수적 예상 수익 기준, 조정 요인 설명)
2. **ROI 전망** (현재 예산 대비 ROI, 손익분기 달성 가능성)
3. **리스크 분석** (주요 위험 요인, 상업성 및 예산 측면)
4. **강점 및 기회** (긍정적 요소가 있다면 함께 제시)
5. **제작 전략 제안** (리스크 완화 방안, 개선 아이디어)
6. **최종 의견** (투자 가능성 평가)
   - ROI 2.5배 이상 → "투자 추천"
   - ROI 2.0~2.5배 → "조건부 추천" 
   - ROI 2.0배 미만 → "재검토 필요"

균형잡힌 시각으로 데이터 기반 분석을 제공해주세요."""
        
        # 시스템 명령어 (화폐 이스케이프 + 균형잡힌 분석)
        system_instruction = """
당신은 20년 경력의 영화 투자 분석 전문가입니다.

[출력 형식 가이드라인 - 반드시 준수]
1. **화폐 기호 이스케이프(필수)**: 금액을 표기할 때 반드시 **\\$** (역슬래시+달러) 형태로 출력하십시오.
   - 나쁜 예: $50,000,000 (절대 금지)
   - 좋은 예: \\$50,000,000 (정상 출력)

2. **볼드체 사용 금지**: 숫자나 금액 데이터에는 절대 볼드체를 씌우지 마십시오.

3. **띄어쓰기 명확히**: 숫자와 한글 조사 사이 띄어쓰기 필수

4. **LaTeX 수식 금지**: 달러 기호로 감싸는 수식 문법 사용 금지

[분석 가이드라인]
1. **균형잡힌 관점**: 리스크와 기회를 모두 객관적으로 평가하십시오.
2. **보수적 기준**: 제공된 보수적 예상 수익(하위 40% 기준)을 중심으로 분석하되, 긍정적 요소도 함께 제시하십시오.
3. **BEP 기준**: ROI 2.5배를 손익분기 기준으로 삼되, 2.0~2.5배 구간은 "주의 필요" 수준으로 평가하십시오.
4. **건설적 제안**: 단순히 반대하기보다는, 개선 방안과 대안을 제시하십시오.
5. **상업성 평가**: 상업성 계수가 낮더라도 예술성이나 특정 타겟층 공략 등 대안적 가치를 고려하십시오.
6. **투자 판단 기준**: 
   - 보수적 ROI 2.5배 이상이면 "투자 추천"으로 명확히 판정하십시오.
   - 조건부 추천은 ROI 2.0~2.5배 구간에서만 사용하십시오.
"""
        messages = [
            SystemMessage(content=system_instruction.strip()),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def quick_roi_estimate(self, genre, budget):
        """빠른 ROI 예측 (간이 버전, 보수적 기준 적용)"""
        try:
            # 장르별 유사 영화 검색
            results = self.collection.query(
                query_texts=[f"{genre} movies"],
                n_results=50
            )
            
            similar_data = self._extract_financial_data(results)
            
            # 예산 범위 필터링
            budget_range = (budget * 0.5, budget * 1.5)  
            similar = [
                m for m in similar_data
                if budget_range[0] <= m.get('budget', 0) <= budget_range[1]
            ]
            
            if len(similar) < 5:
                similar = similar_data[:20]
            
            if not similar:
                return None
            
            # 보수적 통계 사용 (하위 40%)
            rois = [m['roi'] for m in similar]
            revenues = [m['revenue'] for m in similar]
            
            roi_series = pd.Series(rois)
            rev_series = pd.Series(revenues)
            
            return {
                'avg_roi': roi_series.quantile(0.40),  # 하위 40%
                'expected_revenue': rev_series.quantile(0.40),  # 하위 40%
                'sample_size': len(similar),
            }
        
        except Exception as e:
            print(f"Quick ROI estimate error: {e}")
            return None