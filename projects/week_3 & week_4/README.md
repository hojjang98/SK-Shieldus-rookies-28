### 🗓️ 프로젝트 집중 주간 (Week 3 & 4 통합)

## 🧩 주요 프로젝트 활동 요약 (Key Project Activities Summary)

| Day | 날짜 | 프로젝트 활동 주제 | 핵심 작업 |
|-----|------|------------|-------------|
| **Day 1** | **11.15** | **데이터 클리닝 상세 계획 수립 및 초기 전처리** | TMDB 데이터 인코딩/이상치/결측치 처리 기준 정의 및 데이터 다운로드 |
| **Day 2** | **11.17** | 데이터 수집 및 Vector DB 텍스트 구성 | TMDB API 연동, Embedding용 텍스트 결합 및 Vector DB 구축 |
| **Day 3** | **11.18** | Streamlit 시각화 대시보드 구현 완료 | `@st.cache` 전략 적용, Multi-Page 구조, Plotly 시각화 |
| **Day 4** | **11.19** | LangChain/RAG 분석 모델 통합 및 PPT 초안 제작 | ChromaDB 기반 RAG 검색 기능 최종 통합 및 LLM 설명 기능 구현 |
| **Day 5** | **11.20** | 분석 결과 수정 및 최종 QA | RAG 일관성 검증, 시연 스크립트 확정, 최종 발표 자료 완성 |
| **Day 6** | **11.21** | 최종 프레젠테이션 | 프로젝트 발표 및 Q/A (팀 역량 강화에 초점) |

---

## 📘 개요 (Overview)
**LLM/RAG 기반 영화 흥행 분석 시스템**은 TMDB 영화 데이터를 분석하여 흥행 요인을 파악하고, **RAG(검색 증강 생성)**를 통해 사용자의 질의에 근거 기반의 영화 추천과 AI 분석을 제공하는 프로젝트입니다.

이 프로젝트는 Week 3에 배운 LLM/RAG 기술과 Streamlit 대시보드 구축 능력을 통합하여, 데이터 분석 결과를 사용자 친화적인 인터랙티브 웹 서비스 형태로 제공하는 것을 목표로 했습니다.

---

## 🎯 목적 (Objective)
- LangChain, ChromaDB, OpenAI API를 활용하여 **RAG 기반의 검색 시스템**을 구현한다.
- **Streamlit**을 이용해 EDA, 흥행 지표 분석, RAG 추천 기능을 통합한 **멀티 페이지 대시보드**를 구축한다.
- 단순 예측 모델 사용을 지양하고, **데이터 시각화와 LLM의 결합**을 통해 **인사이트 도출**에 중점을 둔다.
- 팀 프로젝트를 통해 **모듈 분리(Modularity)**, 역할 분담, 그리고 **발표 중심의 최종 QA** 프로세스를 경험한다.

---

## ⚙️ 주요 기능 (Key Features)

| 기능 | 설명 |
|------|------|
| RAG 기반 추천 | 자연어 쿼리 또는 영화 제목 기반 **유사 영화 검색** 및 추천 사유 제공 (LLM 설명) |
| 흥행 지표 분석 | **ROI (투자 수익률)** 및 **Profit (이익)** 계산 기반으로 Top 10% 영화의 특징을 분석 |
| EDA 대시보드 | 연도별/장르별/국가별 통계 및 추이 분석을 위한 **인터랙티브 시각화** (Plotly) |
| 성능 최적화 | **`@st.cache_data`** (데이터 로드)와 **`@st.cache_resource`** (Vector DB 클라이언트 로드)를 통한 성능 최적화 |
| 모듈 분리 | `llm_utils.py`, `vector_db.py`, `data_loader.py` 등으로 기능을 분리한 안정적인 구조 |
| AI 흥행 요인 분석 | LLM이 영화의 데이터(예산, 수익, 평점)를 기반으로 **흥행 성공/실패 요인**을 자동 분석 |

---

## 🧠 학습 연결 (Learning Link)

| 학습 내용 | 적용 포인트 |
|------------|-------------|
| Pandas & EDA | TMDB 데이터 클리닝, 결측치 및 이상치 제거, ROI/Profit 계산 |
| Streamlit Caching | `@st.cache_data`, `@st.cache_resource`를 활용한 성능 최적화 및 DB 연결 관리 |
| RAG System | ChromaDB를 Vector Store로 사용하여 텍스트 데이터의 임베딩 검색 구조 구현 |
| LLM Prompting | 추천 사유 생성 및 흥행 분석을 위한 **시스템 프롬프트** 설계 |
| Modularity | `util` 폴더 내 기능 분리 및 `sys.path.append`를 통한 모듈 임포트 관리 |
| Plotly.express | 장르 분포, ROI 분포, 시계열 추이 분석 등 복잡한 통계 데이터의 동적 시각화 |

---

## 🔐 실무 연계 (Project Insight)

이 프로젝트는 **데이터 기반 의사 결정 시스템**의 핵심 파이프라인을 구현합니다.

| 실무 단계 | 코드 내 대응 기능 |
|-----------|------------------|
| 데이터 정제 (Preprocessing) | `Movie_Preprocessing.ipynb`의 이상치/결측치 처리 |
| 분석/모델링 (Modeling) | `Movie_Vector_DB.ipynb`의 Vector DB 구축 및 RAG 구현 |
| 의사 결정 지원 (Decision Support) | `box_office_analysis.py`의 ROI/성공 공식 도출 |
| 결과 전달 (Delivery) | `app.py` 및 Streamlit 대시보드 UI |
| 팀워크/QA (Deployment Prep) | 최종 QA, 발표 자료 완성, 역할 분담 (지속 가능성 강조) |

> 단순한 기술 구현을 넘어, 팀원 모두가 **70~80점의 역량**을 발휘하도록 유도하고, 최종 발표에서는 **"왜?"(인사이트)**를 중심으로 설명하도록 지시하여 프로젝트의 실질적인 가치를 높였습니다.

---

## 📂 최종 파일 구조 (Structure)

```bash
.
├── README.md                                 # 프로젝트 개요 및 목록
├── 홈.py                                     # Streamlit 메인 앱 (초기화 및 통계 요약)
├── data/                                     # 원본/클리닝 데이터 저장소
├── notebooks/                                # Jupyter Notebooks (분석 및 DB 구축 기록)
│   ├── Movie_Analysis.ipynb                  # EDA 및 일반 분석 기록
│   ├── Movie_Preprocessing.ipynb             # 데이터 전처리 상세 기록
│   └── Movie_Vector_DB.ipynb                 # Vector DB 구축 기록
├── pages/                                    # Streamlit 멀티 페이지 폴더
│   ├── 1_ 영화 데이터 탐색 대시보드.py        # (EDA Dashboard)
│   ├── 2_ 흥행 지표 분석.py                  # (Box Office Analysis)
│   ├── 3_ 감독별 흥행 분석.py                # 확장된 분석 페이지
│   └── 4_ 영화 제작 분석 시스템.py           # 확장된 분석 페이지
├── utils/                                    # 유틸리티 모듈 (LLM/DB/Data)
│   ├── data_loader.py                        # 데이터 로드 및 URL 유틸리티
│   ├── llm_utils.py                          # LLM 클라이언트 및 분석 함수
│   ├── production_rag.py                     # 최종 RAG 체인 통합 및 호출 로직
│   ├── tmdb_api.py                           # TMDB API 호출 유틸리티
│   └── vector_db.py                          # ChromaDB 클라이언트 로드 및 검색 기능
└── vector_db/                                # (GIT IGNORED) 임베딩 DB 저장 폴더

```


---

## 실행 방법(How to run)

### 1. 환경 설치: requirements.txt 기반으로 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Vector DB 구축

Movie_Vector_DB.ipynb 또는 별도 스크립트를 실행하여 vector_db/chroma_db 폴더에 DB를 생성해야 합니다.

### 3. Streamlit 대시보드 실행

```bash
streamlit run 홈.py
```


