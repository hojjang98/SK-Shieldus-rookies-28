# 📄 2025.11.11 (Day 13) [RAG & LLM 기반 보안 로그 분석 대시보드]
---

## 1. 🧠 핵심 개념 정리 (Concepts & Theory)

| # | 개념 | 설명 | 예시 |
|:---:|:---|:---|:---|
| **1** | LLM 기반 로그 요약 | 원시 로그 일부를 LLM에게 전달하여 공격 유형·국가·위험도 등을 JSON 구조로 자동 추출함. | JSON-only 시스템 프롬프트 |
| **2** | RAG (Retrieval-Augmented Generation) | 외부 문서(보안 정책, 룰북, MITRE 문서 등)를 임베딩 후 검색하여 LLM이 맥락 기반 분석을 수행하도록 함. | FAISS + Embeddings + RetrievalQA |
| **3** | Streamlit 보안 대시보드 | CSV 업로드 → 전처리 → LLM 분석 → 시각화까지 한 화면에서 처리하는 대시보드 구축 방식. | `st.file_uploader()`, `st.plotly_chart()` |
| **4** | 지리 기반 보안 시각화 | 공격 IP의 위도·경도를 기반으로 세계 지도 상에 공격 분포 표현. | `px.scatter_geo()` |
| **5** | 위험도 기반 우선순위화 | LLM이 생성한 risk_score(1~10) 기준으로 고위험 IP를 자동 필터링함. | `df[df['risk_score'] >= 7]` |

---

## 2. 💻 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) LLM 로그 구조화 프롬프트

```python
system_content = '''
당신은 사이버보안 전문가입니다.
업로드된 로그를 분석하고 JSON만 출력하세요.
[
  {"ip": "", "country": "", "attack_type": "", "risk_score": 8}
]
'''
```

---

### (B) Streamlit 대시보드 기본 흐름

```python
st.title("LLM 기반 보안 로그 분석 대시보드")

file = st.file_uploader("로그 CSV 업로드")

if file:
    df = pd.read_csv(file)
    response = ask_llm(df)
    result = pd.DataFrame(json.loads(response.choices[0].message.content))
    st.dataframe(result)
```

---

### (C) Plotly 기반 공격 위치 시각화

```python
fig = px.scatter_geo(
    result,
    lat="latitude",
    lon="longitude",
    color="risk_score",
    hover_name="ip",
    projection="natural earth",
    color_continuous_scale="Reds",
    size="risk_score"
)
st.plotly_chart(fig)
```

---

## 3. 🛡️ 보안 관점 분석 (Security Insight & Scenario Mapping)

### SOC / 관제
- LLM이 로그의 잡음 대신 핵심 엔터티를 정리해주어 탐지 속도 증가.
- 지리적 분포를 통해 공격 국가·집중 지역을 빠르게 파악할 수 있음.

### CERT / 사고 대응
- ip, attack_type, country 자동 추출 → 사고 흐름(Time → Actor → 피해 범위) 재구성에 유용.
- 공격자의 패턴·경로를 시각적으로 재현 가능.

### 위협 인텔리전스
- 위험도(risk_score) 기반으로 우선 대응해야 할 공격자 그룹 분리.
- 공격 유형 분포를 통해 최신 공격 트렌드 파악.

### DevSecOps
- 빌드/스캔 로그도 동일한 구조로 요약·분석 가능.
- 반복적 오류/취약점의 자동 분류에 사용 가능.

### 개인정보 보호
- IP나 User ID를 마스킹한 뒤 요약하도록 하여 분석과 규제를 동시에 만족.

---

## 4. 🧩 요약 (Summary)

- RAG + LLM + Streamlit을 결합해 **가벼운 SIEM 형태의 로그 분석 파이프라인**을 구축했다.  
- 공격 유형·국가·위험도를 구조화하고, 시각화(Bar + Geo Plot)를 통해 **보안 인사이트**를 강화했다.  
- LLM을 단순 요약기가 아니라 **보안 이벤트 해석 엔진**으로 활용할 수 있음을 확인했다.  

**Next Step:**  
실제 보안 문서(MITRE ATT&CK 설명, 내부 정책, 룰북)를 RAG Retrieval에 연결해 “설명 가능한 탐지·대응(Explainable IR)” 시스템으로 확장할 계획이다.

---

## 💭 개인 인사이트 (Reflection)

- LLM이 로그의 패턴과 의미를 자동으로 구조화하는 과정이 매우 강력하다고 느꼈다.  
- Streamlit만으로도 SOC 환경에 가까운 대시보드를 빠르게 만들 수 있다는 점이 인상적이었다.  
- RAG를 활용하면 분석 결과에 ‘근거’를 제공할 수 있어, 보안 대응의 신뢰도를 크게 높일 수 있다고 느꼈다.

