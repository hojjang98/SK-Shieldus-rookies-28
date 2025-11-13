# 📄 2025.11.13 (Day 14) [실시간 로그 모니터링 · RAG 보안 챗봇 통합 실습]

---

## 1. 🧠 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 예시 |
|:---:|:---:|:---|:---|
| **1** | **Streamlit 기반 Real-Time Streaming** | `st.empty()` + `time.sleep()`로 5초 간격 로그 스트림 시뮬레이션 구성 | 실시간 로그 누적 출력 |
| **2** | **FAISS + OpenAIEmbedding VectorDB** | 공격 로그를 텍스트화 → 분할 → 임베딩 → 벡터DB 구축 | `FAISS.from_documents(docs, embeddings)` |
| **3** | **ConversationalRetrievalChain** | RAG + 챗봇 대화 기록을 결합해 문맥 기반 보안 분석 | `chain({"question": prompt, ...})` |
| **4** | **Session State 관리** | 실시간 로그, 메시지 이력, 대화 메모리 저장 | `st.session_state['logs']` |
| **5** | **2-Column 대시보드 UI** | 좌측 실시간 로그 / 우측 RAG 챗봇 형태의 보안 관제 화면 구성 | `realtime, chatbot = st.columns(2)` |

> 💡 **핵심 인사이트:**  
> 정적 로그 분석을 넘어서 **“실시간 탐지 + RAG 기반 위협 설명”**까지 하나의 Streamlit 앱에서 구현함으로써, 보안 모니터링 시스템의 핵심 골격을 직접 만들었다는 점이 가장 큰 학습 포인트였다.

---

## 2. 💻 실습 코드 & 응용 (Practice & Code Walkthrough)

### (1) 실시간 로그 모니터링

```python
if 'logs' not in st.session_state:
    st.session_state['logs'] = pd.DataFrame(columns=frm.columns)

logPrt = st.empty()
warningPrt = st.empty()

for idx, row in frm.iterrows():
    newLog = row.to_dict()

    st.session_state['logs'] = pd.concat([
        pd.DataFrame([newLog]),
        st.session_state['logs']
    ])

    if newLog['risk_score'] >= 85:
        warningPrt.warning('고위험 공격 감지!! 집중')
    else:
        warningPrt.info('시스템 정상 작동 중')

    logPrt.dataframe(st.session_state['logs'])
    time.sleep(5)
```

### (2) RAG 기반 보안 챗봇

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = splitter.create_documents(database)

embeddings = OpenAIEmbeddings()
vectorDB = FAISS.from_documents(docs, embeddings)

retriever = vectorDB.as_retriever(k=10)
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.9)
qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

response = qa_chain({
    "question": prompt,
    "chat_history": st.session_state["chat_history"]
})
```

| 구분 | 내용 |
|:---|:---|
| **핵심 코드 설명** | 로그를 자연어 문장으로 변환 → 벡터DB 구축 → RAG 검색을 통해 “근거 기반 위협 분석” 생성 |
| **보안 맥락** | 공격 패턴 비교, IP 기반 위협 블록, 사고 타임라인 재구성 등에서 핵심 |
| **확장 아이디어** | GeoIP 추가 → Folium 맵에 공격 지점 자동 시각화 가능 |

---

## 3. 🛡️ 보안 관점 분석 (Security Insight & Scenario Mapping)

### ● SOC / 관제  
- 실시간 로그 스트림이 5초 간격으로 갱신되어 공격 유형·리스크 점수를 즉시 확인 가능  
- “경보 + 자동 분석 챗봇” 구조를 통해 탐지 → 분석 → 보고 흐름이 하나로 통합  

### ● CERT / 사고대응  
- RAG 분석 결과가 공격자 IP, 시점, 공격 방식 등 **사고 타임라인 재구성**에 직접 활용 가능  
- 원본 로그 근거 기반 분석이므로 사고 보고서 품질 상승  

### ● 취약점 진단(VA)  
- 벡터DB에 축적된 과거 공격 로그를 기반으로 반복적 공격 여부를 유사도로 비교  
- 특정 서비스/포트에 대한 재발 위협 식별 가능  

### ● DevSecOps  
- 빌드 로그나 테스트 로그도 동일한 RAG 구조에 넣으면 자동 분석·요약 시스템 구축 가능  
- 파이프라인 오류 원인/보안 취약점 자동 서머리  

### ● 디지털 포렌식  
- 로그의 시간·행위 기반 연속성을 바탕으로 공격 흐름을 시각적으로 재구성  
- 추적·증거 확보 과정의 효율성 강화  

---

## 4. 🧩 요약 및 다음 단계 (Summary & Next Steps)

- 오늘 실습을 통해 **실시간 로그 흐름이 어떻게 시각적으로 표시되는지**, 그리고 그 데이터가 **RAG 기반 보안 분석 모델과 어떤 방식으로 연결되는지**를 직접 확인할 수 있었다.  
- 벡터DB 구성을 통해 단순한 텍스트 검색이 아닌 **맥락 기반·근거 기반 분석이 가능해지는 흐름**을 이해했고, 이것이 보안 관제 자동화에서 어떤 의미를 가지는지도 명확해졌다.  
- 실시간 스트림과 대화형 분석 모델이 한 화면에서 함께 동작하는 흐름을 보며, **현업의 관제 화면 구성이 어떤 원리로 운영되는지** 체감할 수 있었다.

---

## 💭 개인 인사이트 (Reflection)

- **배운 점:**  
  실시간 로그 스트림과 LLM 기반 분석이 결합되는 구조를 직접 따라 해보며, 보안 자동화 시스템의 기초적인 작동 흐름을 이해하게 되었다.

- **느낀 점:**  
  Streamlit만으로도 관제센터와 유사한 형태의 대시보드를 구성할 수 있다는 점이 꽤 새로웠고, 전체 흐름이 생각보다 직관적이라는 점이 인상적이었다.

- **심화 방향:**  
  Kafka 기반 로그 스트림이나 Logstash 파이프라인처럼, 실제 환경에서 쓰는 기술들이 이런 구조 위에서 어떻게 연결되는지 더 살펴보고 싶다.

- **향후 계획:**  
  내일은 기능을 더 확장하기보다는, 오늘 배운 내용과 코드 흐름을 다시 정리하고 문서화하여 이해도를 높이는 데 집중할 예정이다.  
  불필요하게 시스템을 복잡하게 만드는 작업은 피하고, 현재 학습한 구조를 확실히 내 것으로 만드는 방향으로 진행할 계획이다.




