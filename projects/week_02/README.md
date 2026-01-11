# 📊 Project 02 — Streamlit Log Dashboard

## 🧩 학습 내용 요약 (Weekly Summary)
| Day | 주제 | 핵심 개념 |
|-----|------|------------|
| **Day 1 (11.03)** | Numpy 기초 및 벡터화 연산 | 로그 데이터의 벡터화 처리 및 고속 계산 |
| **Day 2 (11.04)** | Pandas & EDA 기초 | 로그 적재, 결측 보정, DataFrame 변환 |
| **Day 3 (11.05)** | Pandas 기반 로그 정규화 | 데이터 표준화, 타입 변환, 결측 처리 |
| **Day 4 (11.06)** | Matplotlib·Seaborn 기반 시각화 | 그룹화, 통계형 시각화, 이상치 탐지 그래프 |
| **Day 5 (11.07)** | Folium·Plotly·Streamlit 실습 | 인터랙티브 지도, 동적 그래프, 웹 대시보드 구성 |

---

## 📘 개요 (Overview)
**Streamlit Log Dashboard**는 Week1에서 구축한 `Mini Security Log Monitor`의 결과(`access.log`)를 기반으로, 보안 로그를 **데이터프레임 형태로 가공 → 시각화 → 대시보드화** 한 프로젝트이다.  

이번 주에는 Week1 코드를 단순 재사용하지 않고, **랜덤 사용자·랜덤 인증 로직을 추가하여 보다 현실적인 로그 패턴을 자동 생성**하도록 확장하였다.  
이로써 Pie Chart·Bar Chart·Line Chart에서 다양한 분포를 시각적으로 분석할 수 있는 구조를 완성하였다.

---

## 🎯 목적 (Objective)
- Week1의 `secure_log_monitor.py`를 가공하여 **랜덤 로그 자동 생성 기능**을 추가한다.  
- **Matplotlib / Seaborn**을 활용해 탐지율 및 실패율을 시각화한다.  
- **Plotly / Streamlit**을 사용해 실시간 대시보드 형태로 구성한다.  
- 단순 텍스트 로그를 **구조화된 보안 이벤트 데이터셋**으로 전환해 시각적 인사이트를 도출하는 과정을 체험한다.

---

## ⚙️ 주요 기능 (Key Features)
| 기능 | 설명 |
|------|------|
| 🧮 랜덤 로그 자동 생성 | `secure_log_monitor.py`에 랜덤 사용자·인증 반전 로직 추가 (현실적 분포 확보) |
| 🧾 JSON 기반 데이터 로드 | `access.log`의 JSON 라인을 필터링하여 Pandas DataFrame으로 변환 |
| 📊 통계 기반 시각화 | 성공/실패 비율(Pie), 사용자별 접근 분포(Bar) 표시 |
| 🌐 Streamlit 대시보드 | 필터, 메트릭, 그래프, 데이터 테이블 UI 구성 |
| ⚡ 실시간 반영 | 로그 파일 갱신 시 수동 새로고침으로 즉시 반영 |
| 🗺️ 확장 가능 구조 | Folium 및 GeoIP 추가 시 지역 기반 공격 맵 시각화 가능 |

---

## 🧠 학습 연결 (Learning Link)
| 학습 내용 | 적용 포인트 |
|------------|-------------|
| `numpy`, `pandas` | 로그 데이터 정규화 및 전처리 |
| `random` 모듈 | 인증 여부를 무작위로 전환하여 다양한 로그 패턴 생성 |
| `groupby`, `pivot_table` | 사용자별/시간대별 탐지 이벤트 집계 |
| `matplotlib`, `seaborn` | 탐지율 및 실패율 그래프 작성 |
| `plotly.express` | 인터랙티브 시각화 구현 |
| `streamlit` | 대시보드 UI 구성 및 필터 연동 |
| `time.sleep()` | 로그 생성 타이밍 분산으로 시계열 분석 기반 마련 |

---

## 🔐 실무 연계 (SOC Perspective)
이번 프로젝트는 “**로그 → 정제 → 시각화 → 인사이트 도출**” 과정을  
보안관제센터(SOC)의 **기초 분석 사이클**로 옮겨온 것이다.

| SOC 단계 | 코드 내 대응 기능 |
|-----------|------------------|
| 로그 수집 (Collection) | Week1 `secure_log_monitor.py` 확장 버전에서 랜덤 로그 수집 |
| 데이터 정제 (Preprocessing) | Pandas 기반 JSON 파싱 및 구조화 |
| 이벤트 시각화 (Visualization) | Plotly·Seaborn으로 성공/실패 분포 분석 |
| 대시보드 분석 (Dashboard) | Streamlit UI로 사용자별/시간대별 필터링 |
| 보고 및 판단 (Reporting) | 보안 이벤트 패턴 및 실패율 시각화 |

> 💡 단순 코드 실행에서 벗어나,  
> “**데이터를 해석하고 의사결정을 지원하는 시각화 엔진**”의 기초를 다졌다.

---

## 📂 파일 구조 (Structure)

```bash
├── README.md
├── secure_log_monitor.py
├── access.log
├── dashboard.py
└── system.log
```

### 실행 방법 (How to Run)

1. Week1 프로젝트 실행 후 로그 생성

```bash
python secure_log_monitor.py
```

> 약 50개의 랜덤 로그가 access.log에 기록됨
> 사용자·인증 상태가 랜덤 분포로 생성되어 다양한 시각화 가능

2. Streamlit 대시보드 실행

```bash
streamlit run dashboard.py
```

3. 대시보드 주요 구성

| 항목 | 내용 |
|------|------|
| **필터 (Sidebar)** | 사용자 선택, 결과 선택(SUCCESS / FAIL) |
| **메트릭 (상단 요약)** | 총 접근 시도 수, 실패율(%) |
| **그래프 ①** | 🥧 **Pie Chart** — 접근 결과 비율(SUCCESS vs FAIL) |
| **그래프 ②** | 📊 **Bar Chart** — 사용자별 접근 시도 및 결과 분포 |
| **데이터 테이블** | 🧾 **Raw Log Data** — 필터링된 JSON 로그 목록 |
| **자동 갱신(옵션)** | 🔄 `st_autorefresh()` 기반 주기적 새로고침으로 실시간 모니터링 구현 가능 |


- 주요 기능:
    - 사용자별 / 결과별 필터
    - 실패율 Pie Chart
    - 시간대별 이벤트 분포 Line Chart

🧩 확장 아이디어 (Next Step)

> 시간대별 접근 추이(Line Chart): 로그 생성 시각 기반 시계열 분석
> 실시간 업데이트: Streamlit st_autorefresh(interval=5000) 활용
> 지도 시각화 확장: Folium + GeoIP로 공격 발생 지역 표시
> 로그 심화 분석: Pandas 그룹화로 사용자별 실패율 / 평균 응답시간 계산
> 보안 인텔리전스 연계: 외부 Threat Intelligence API 결합

> Week2 프로젝트는 Week1의 탐지 엔진을 데이터 분석 레이어로 확장한 단계이다. 로그를 “텍스트”가 아닌 “데이터”로 바라보는 관점을 체득하는 것이 핵심이다.