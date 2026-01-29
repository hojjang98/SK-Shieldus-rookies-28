# Research Review: Towards an Integrated Risk Analysis Security Framework
> **Analyzed Date:** 2025.01.27  
> **Keywords:** Risk_Assessment, Risk_Management, MARISMA, Systematic_Review, SME_Security  
> **Source:** Frontiers of Computer Science, 2024, Vol. 18(3), Article 183808  
> **DOI:** 10.1007/s11704-023-1582-6  
> **Link:** https://link.springer.com/article/10.1007/s11704-023-1582-6

---

## Why This Paper?

### 선정 배경
**도메인 탐색 결과:**  
8주간 여러 논문을 읽고, 13주차부터는 SOC 관련 논문을 읽은 후, 최종 프로젝트 희망이 보안 컨설팅 방향으로 전환됨에 따라 체계적으로 컨설팅 전문성을 쌓기 위한 새로운 학습 단계 시작.

**이 논문을 선택한 이유:**  
- 2024년 최신 연구로, 30개의 위험 분석 방법론을 체계적으로 비교 분석
- 학술적 분석뿐 아니라 실제 스페인, 콜롬비아, 에콰도르, 아르헨티나 기업에 적용 중인 MARISMA 프레임워크 포함
- 취약점 진단, 위험 평가, 보안 체계 구축 등 예상 프로젝트 주제와 직접 연관
- Systematic Literature Review 방법론으로 기존 연구의 한계를 명확히 식별

**학습 목표:**  
1. 현대 위험 분석 방법론의 10가지 핵심 약점 이해
2. 실무 적용 가능한 위험 평가 프레임워크 설계 원칙 습득
3. SME 환경에서의 보안 컨설팅 접근법 학습

---

## Day 1 – Research Context & Motivation
*(정보 사회의 생존 조건: 적응형 위험 분석의 필요성)*

### 1. 연구 배경: 전통적 위험 분석의 한계

**디지털 전환 시대의 보안 역설**

현대 기업들은 사이버 보안에 막대한 투자를 하고 있지만, 위협의 수와 영향은 오히려 증가하고 있다. 특히 정보 시스템은 기업 경쟁력의 핵심 요소가 되었으며, 정보와 프로세스는 기업의 가장 중요한 자산으로 인식되고 있다.

**전통적 위험 분석의 3가지 구조적 문제**

| 문제 영역 | 구체적 한계 | 비즈니스 영향 |
|-----------|-------------|---------------|
| **기술 진화 속도** | 고전적 위험 분석 모델이 Cloud, IoT, Big Data, CPS 등 신기술 환경의 위험을 제대로 반영하지 못함 | 알려지지 않은 위험과 취약점 노출 |
| **협업 필요성 증가** | 기업 간 연계, 제3자 서비스, 다자간 프로젝트 등에서 발생하는 **연관 위험(Associative Risk)** 및 **계층적 위험(Hierarchical Risk)** 미반영 | 공급망 공격 등 간접 위험 관리 실패 |
| **정적 분석의 한계** | 위험 분석은 비용이 많이 드는 프로세스이며, 기존 방법론은 변경 시마다 전체 분석을 반복하도록 설계되지 않음 | 수개월~수년 전 위험 평가 결과로 현재를 판단하는 오류 |

**중소기업(SME)의 이중 위기**

대기업과 달리 SME는:
- 적절한 가이드라인 없이 보안 시스템 개발
- 불충분한 자원과 낮은 보안 문화
- 복잡한 위험 분석 방법론을 적용할 인력/예산 부족

시장의 보안 도구들은 문제의 일부만 해결하며, 포괄적이고 통합된 방식으로 접근하지 못한다.

**연구 문제의식**

> "현대 기술 환경(Cloud, IoT, Big Data)과 협업 비즈니스 모델에 적합하면서, 동시에 SME도 실용적으로 적용할 수 있는 **동적이고 적응형인** 위험 분석 프레임워크를 어떻게 설계할 것인가?"

### 2. 핵심 개념: 위험 관리의 진화

#### A. 위험 분석의 기본 개념

| 개념 | 정의 | 컨설팅 맥락에서의 의미 |
|------|------|---------------------|
| **위험 분석 (Risk Analysis)** | 자산, 위협, 취약점을 식별하고 위험 수준을 평가하는 프로세스 | 고객사의 현재 보안 상태를 객관적으로 진단하는 기반 |
| **위험 관리 (Risk Management)** | 식별된 위험을 감소, 전이, 수용, 회피하는 통제 전략 | 진단 결과를 바탕으로 실행 가능한 보안 개선 로드맵 제시 |
| **연관 위험 (Associative Risk)** | 파트너사, 공급업체, 클라우드 제공자 등 외부 관계에서 발생하는 위험 | 공급망 보안, SaaS 의존성, 아웃소싱 리스크 평가 |
| **계층적 위험 (Hierarchical Risk)** | 시스템 구성요소 간 종속성으로 인해 한 계층의 위험이 다른 계층으로 전파되는 위험 | 인프라 장애가 애플리케이션에 미치는 영향 등 종속성 분석 |

#### B. 새로운 기술 패러다임이 가져온 위험 변화

**Cloud Computing의 영향**
- 물리적 경계의 소멸 → 전통적 경계 기반 보안 모델 무력화
- 가상화된 자원 → 물리 서버뿐 아니라 가상 서버의 위험 고려 필요
- 제3자 의존성 → 클라우드 제공자의 보안 수준에 직접 영향받음

**IoT 환경의 특수성**
- 수많은 엔드포인트 → 공격 표면 기하급수적 증가
- 물리-디지털 융합 → OT(Operational Technology) 보안 고려 필요
- 제한된 자원 기기 → 전통적 보안 솔루션 적용 어려움

**Industry 4.0 / CPS의 도전**
- 사이버-물리 시스템 연동 → 사이버 공격이 물리적 피해로 직결
- SCADA 시스템 보안 → 중요 기반시설 보호의 새로운 차원

### 3. 연구 방법: Systematic Literature Review

본 논문은 **Kitchenham의 체계적 문헌 고찰(Systematic Review) 프로토콜**을 따른다. 이 방법론은 의학 연구를 위해 개발되었으나, 정보 시스템 연구에 적합하도록 조정되었다.

#### 연구 설계 구조

```
[연구 질문 정의]
    ↓
[검색 전략 수립]
 - 데이터 소스: ACM, IEEE, Elsevier, Springer, Taylor&Francis, Wiley
 - 검색 기간: 2011-2022 (11년)
 - 키워드: Risk Analysis, Risk Management, SME, Cloud, IoT, Dynamic, 
           Associative Risk, Hierarchical Risk
    ↓
[연구 선별 기준]
 - 포함 기준: 제목/키워드/초록 분석
 - 제외 기준: 요약/결론 정밀 분석
    ↓
[최종 선정]
 초기: 6,635개 논문
 → 최종: 30개 핵심 연구
```

#### 선정된 연구의 분류

| 유형 | 개수 | 예시 |
|------|------|------|
| **Process** | 4 | 위험 평가 절차, 단계별 워크플로우 |
| **Framework** | 9 | 위험 관리 구조, 아키텍처 |
| **Model** | 9 | 위험 계산 모델, 수학적 표현 |
| **Methodology** | 6 | 통합된 방법론 (프로세스 + 모델) |
| **Others** | 2 | 기타 관련 연구 |

### 4. 연구의 핵심 기여

#### A. 학술적 기여: 10가지 약점의 체계적 식별

본 연구는 30개의 기존 연구를 12가지 평가 기준으로 분석하여, 현대 위험 분석 방법론의 10가지 핵심 약점을 도출했다:

| 약점 코드 | 약점 명칭 | 설명 | 현실적 영향 |
|----------|-----------|------|-------------|
| **AC** | Adaptive Catalogues | 시간에 따라 변화하는 요소 카탈로그 부재 | 새로운 위협에 대응하기 위해 방법론 전체를 재설계해야 함 |
| **HA** | Hierarchy & Associativity | 계층적/연관적 위험 구조 미반영 | 클라우드, 공급망 등 간접 위험 평가 불가 |
| **RKL** | Reuse Knowledge & Learning | 과거 분석 결과 재사용 및 학습 메커니즘 부족 | 매번 처음부터 분석, 경험 축적 불가 |
| **DY** | Dynamic & Evolutionary | 정적 분석, 변화 시 전체 재평가 필요 | 수개월 전 결과로 현재 위험 판단 |
| **CC** | Collaborative Capability | 기업 간 협업 위험 관리 불가 | 파트너사 보안 수준 공유/조율 불가 |
| **AE** | Valuation of Elements | 자산, 영향 등의 정량적 평가 메커니즘 부족 | 비용 대비 효과 계산 어려움 |
| **DM** | Dynamic Metrics | 고정된 위험 계산 공식 | 산업/상황별 맞춤형 위험 측정 불가 |
| **LLS** | Low Level of Subjectivity | 높은 주관성 → 제3자가 결과 신뢰 어려움 | 외부 감사, 인증 시 객관성 부족 |
| **SLC** | Simplicity & Low Cost | 복잡도 높아 SME 적용 불가 | 실무 도입률 저조 |
| **TS** | Tool Support | 자동화 도구 부재 → 수작업 의존 | 시간/비용 과다, 일관성 부족 |

#### B. 실무 기여: MARISMA 프레임워크 제안

논문은 식별된 10가지 약점을 해결하기 위해 **MARISMA**(Methodology for the Analysis of Risks on Information Systems, using Meta-pattern and Adaptability) 프레임워크를 제안한다.

**MARISMA의 4대 구성 요소**

```
┌─────────────────────────────────────────┐
│  1. Meta-Pattern (CAT 구조)             │
│  - Control, Asset, Threat의 관계 정의   │
│  - 모든 위험 분석 패턴의 공통 구조       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  2. 3가지 핵심 프로세스                  │
│  - RPG: 위험 패턴 생성                   │
│  - RAMG: 위험 분석 및 관리               │
│  - DRM: 동적 위험 관리                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  3. Knowledge Base (패턴 저장소)         │
│  - 산업별/기술별 위험 패턴 축적          │
│  - 인스턴스 간 학습 공유                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  4. eMARISMA Tool (클라우드 기반)        │
│  - Java/Grails 기반 자동화 도구          │
│  - MySQL, Spring Security 활용           │
└─────────────────────────────────────────┘
```

**실제 적용 현황**
- 적용 국가: 스페인, 콜롬비아, 에콰도르, 아르헨티나
- 적용 섹터: 정부, 중요 기반시설, 석유화학, 화학, 조선
- 지속적 개선: 실무 적용 피드백으로 프레임워크 진화 중

### 5. 컨설팅 관점 인사이트

**적용 가능성: 왜 이 연구가 컨설팅 실무에 중요한가**

1. **체계적 분석 프레임워크 제공**
   - 30개 방법론의 장단점을 한눈에 비교 가능
   - 고객사 상황에 맞는 방법론 선택 시 근거 자료로 활용

2. **SME 특화 접근**
   - 대부분의 고객사가 SME라는 현실 반영
   - 복잡도와 실용성의 균형점 제시

3. **동적 위험 관리의 중요성**
   - 일회성 진단이 아닌 지속적 관리 모델
   - 컨설팅 이후 유지보수 계약으로 연결 가능

**기존 학습과의 연결**
- SOC 논문들: 위협 탐지/분석 기술 → 이 논문: 위험을 어떻게 **평가하고 관리**할 것인가
- Bulgurcu (2010): 인간 행동 측면 → 이 논문: 조직 전체 위험 관리 측면
- 보완 관계: 탐지 기술 + 인간 요소 + 위험 관리 = 통합 보안 컨설팅

**현실적 고려사항**
- MARISMA는 연구팀의 spin-off 회사를 통해 상용화
- 실제 도입 시 eMARISMA 도구 비용, 교육 기간, 조직 변화 관리 필요
- 한국 환경에서는 ISMS-P, ISO 27001과의 매핑 작업 선행되어야 함

---

**Day 1 마무리:**  
오늘은 현대 위험 분석의 구조적 한계를 이해했다. 기술 진화 속도, 협업 증가, 정적 분석의 한계라는 3대 문제가 전통적 방법론을 무력화시키고 있으며, 특히 SME는 복잡한 방법론을 적용할 여력이 없다. 이 논문은 30개 연구의 체계적 분석을 통해 10가지 약점을 식별하고, MARISMA라는 실무 검증된 해결책을 제시한다. 내일은 이 30개 연구들이 구체적으로 어떤 접근을 시도했는지, 그리고 왜 실패했는지를 심층 분석할 예정이다.

# Research Review: Towards an Integrated Risk Analysis Security Framework
> **Day 2 Focus:** 30개 선정 연구의 상세 분석 및 비교  
> **Source:** Section 4 (Information Collection) & Table 2 (Main Contributions)

---

## Day 2 – Selected Studies Analysis
*(30개 위험 분석 연구의 접근법과 한계)*

### 1. 연구 분석 개요

논문은 6,635개의 초기 결과에서 선별 기준을 적용하여 최종 30개의 연구를 선정했다. 각 연구는 5가지 유형으로 분류되었다:

**분류 기준:**
- **Process**: 목표 달성을 위한 연속적 단계의 활동 집합
- **Framework**: 위험 관리 프레임워크 구축을 지원하는 계층 구조
- **Model**: 복잡한 시스템의 이해를 돕기 위한 표현 도구
- **Methodology**: Process와 Model을 통합한 체계적 접근법
- **Others**: 위 범주에 완전히 맞지 않지만 유용한 개념을 포함한 연구

### 2. Process 유형 연구 (4개)

#### P1: Hybrid Information Security Risk Assessment Procedure [56]

**핵심 접근:**
- DEMATEL(Decision Making Trial and Evaluation Laboratory)과 ANP(Analytic Network Process) 결합
- ISO/IEC 27001의 3개 보안 통제 영역에 초점

**평가 절차:**
1. 시스템 특성 파악
2. 위협과 취약점 식별
3. 위험 평가
4. 영향 분석
5. 위험 결정
6. 통제 권고사항

**한계:**
- 유연성 부족, 근본적으로 이론적
- 실무 적용 복잡도 높음
- 연관 및 계층적 요인 미고려

#### P2: Fuzzy Logic-Based System for Enterprise Collaboration [57]

**핵심 접근:**
- 협업 생애주기 4단계(사전 생성, 생성, 운영, 종료)의 위험 요인 식별
- 각 위험을 확률과 영향으로 기술

**실무 검증:**
- Collaboration Risk Evaluator (CRE) 프로토타입 웹 서비스 개발
- 실제 사용 사례로 검증

**한계:**
- 모든 유형의 기업과 섹터에 적용 가능성 고려 부족
- 지식 재사용 메커니즘 없음

#### P3: SDN Information Security Risk Assessment [58]

**핵심 접근:**
- Software Defined Network(SDN) 아키텍처 기반
- Pythagorean Fuzzy Sets를 활용한 불확실성 고려
- 다기준 의사결정(MCDM) 방법 개발

**기여:**
- 퍼지 기법으로 연관 요인 고려 가능
- SDN 속성과 취약점 간 영향 관계 파악

**한계:**
- 근본적으로 이론적 연구
- 복잡한 실무 사례에서 결과 검증 없음

#### P4: Integrated Risk Assessment via Fuzzy Theory [59]

**핵심 접근:**
- 환경 요인으로 인한 불완전한 결과나 높은 불확실성을 다루기 위한 퍼지 기법
- 철도 분야에 특화되었으나 IT 분야로 외삽 가능

**기여:**
- 질적/양적 기법 모두 사용
- 계층적 관계 고려
- 사례 연구 정의

**한계:**
- 근본적으로 이론적 연구
- 복잡한 실무 사례에서 결과 검증 없음

### 3. Framework 유형 연구 (9개)

#### F1: Comprehensive Framework for Enterprise Information Security [60]

**구조:**
- 2개의 구조적 차원: 범위, 평가 기준
- 2개의 절차적 차원: 프로세스, 평가 도구
- STOPE(Strategy, Technology, Organization, People, Environment) 관점
- DMAIC(Define, Measure, Analyse, Improve, Control) 순환 단계

**한계:**
- 이론적 연구
- 실무 사례 적용 결과 없음

#### F2: Knowledge-Based Risk Management (KBRM) [61]

**핵심 개념:**
- 지식 관리(KM) 프로세스로 위험 관리 효과성 향상
- 5가지 활동: 지식 기반 위험 식별, 포착, 공유, 평가, 교육

**기여:**
- 지식 관리를 위험 분석에 적용한 최초 시도

**한계:**
- 이론적 연구
- 실무 검증 없음

#### F3: Info-structure for ISRA [62]

**목적:**
- 기업이 가장 적합한 위험 관리 방법론을 선택하고 이해하도록 정보 구조화

**기여:**
- 위험 평가 전 필요한 정보 수집 프레임워크
- 동적 위험과 관계적 측면의 중요성 강조

**한계:**
- 이론적 연구
- SME에 적용하기 어려운 주요 방법론만 고려
- 실무 검증 없음

#### F4: Dynamic Risk Management Framework [63]

**핵심 개념:**
- PDCA(Plan-Do-Check-Act) 전략 기반 동적 위험 평가
- 초기 평가 후 지속적 평가 순환

**기여:**
- 위험 평가 프로세스 내 동적 개념의 중요성 증가

**한계:**
- 매우 초기 단계
- 실무 검증 없음

#### F5: Fuzzy Reinforcement for Software Risk Assessment [64]

**핵심 접근:**
- 소프트웨어 프로젝트 개발에서 불확실성 관리
- 퍼지 기법 기반 위험 평가 프레임워크 개발 기반

**한계:**
- 이론적 연구
- 실무 검증 없음

#### F6: Core Unified Risk Framework (CURF) [21]

**목적:**
- 정보 시스템 위험 평가 방법들을 비교하는 프레임워크

**기여:**
- 동적 프레임워크 필요성 명시
- 클라우드 컴퓨팅 적응과 지식 재사용 포함

**한계:**
- 비교 방법 제시만 하고 새로운 제안 없음

#### F7: Fuzzy Methodology for RAM Analysis [65]

**핵심 접근:**
- FMEA(Failure Mode and Effect Analysis) 기반
- 규칙 기반 접근법과 퍼지 기법 활용
- Fuzzy Lambda-Tau(FLT)로 신뢰성, 가용성, 유지보수성(RAM) 계산

**적용 범위:**
- 화학 처리 플랜트에 초점
- 모든 정보 시스템에 적응 가능할 만큼 일반적
- 중요 기반시설 위험 분석의 중요성 강화

**한계:**
- 이론적 연구
- 실무 검증 없음

#### F8: LiSRA - Lightweight Security Risk Assessment [66]

**목적:**
- 모든 유형 조직, 특히 SME 적응을 위한 의사결정 지원

**기여:**
- 기존 보안 활동 고려
- 요소 간 의존성 고려 (연관 관계 강조)
- 질적 기법으로 빠르고 쉬운 초기 평가
- 이전 구현의 지식 활용 메커니즘

**한계:**
- 이론적 연구
- 실무 검증 없음

#### F9: BPRIM - Business Process-Risk Integrated Method [67]

**핵심 개념:**
- 위험 관리와 비즈니스 프로세스 관리 통합
- BPM과 ERM 생애주기 결합
- 위험 메타모델 (일반 수준에서 정의, 다양한 영역에 적응 가능)
- 반형식적 그래픽 모델링 언어

**지원 도구:**
- 프로세스 모델링만 지원, 위험 버전 미지원
- 현재 버전은 위험 관리보다 비즈니스 프로세스 관리에 가까움

**실무 적용:**
- 의료 섹터 일부 실무 사례 테스트
- 다른 섹터에서의 효과성은 아직 미분석

### 4. Model 유형 연구 (9개)

#### MO1: ISS Risk Assessment under Uncertain Environment [68]

**핵심 이론:**
- Evidence Theory(베이지안 주관 확률 이론의 일반화) 기반
- 정보 보안 시스템 위험 평가에서 불확실성이 중요하다는 가정

**기여:**
- 퍼지 측정으로 BBA(Basic Belief Assignment) 정의
- 전문가 예측 증거 간 충돌로 인한 불확실성 감소

**실무 적용:**
- 클라우드 컴퓨팅 환경에 적용 가능
- 실무 사례 연구로 검증
- 매우 일반적이며 소프트웨어 도구 지원 없음

#### MO2: VIKOR-DEMATEL-ANP Model [69]

**핵심 접근:**
- VIKOR, DEMATEL, ANP를 결합한 다기준 의사결정(MCDM) 모델
- 상호 의존성과 피드백을 보이는 충돌 기준 해결

**4단계 프로세스:**
1. 위험 평가
2. 위험 완화
3. 위험 모니터링 및 검토
4. 위험 관리 개선

**특징:**
- PDCA 전략으로 개발된 지속적 순환
- 사례 연구로 모델 적용 및 정제
- 매우 일반적이며 소프트웨어 도구 지원 없음

#### MO3: Causal Relationships and Vulnerability Propagation [70]

**핵심 개념:**
- 위험 요인 간 인과 관계 식별
- 취약점 전파의 복잡성과 불확실성 분석
- 보안 취약점이 위험 요인의 인과 체인을 통해 다양한 경로로 전파/확대

**방법론:**
- 베이지안 네트워크 개발
- 관찰 사례와 도메인 전문가 지식 기반

**한계:**
- 이론적 연구
- 실무 검증 없음

**관련 연구:**
Wang et al. [71]도 베이지안 네트워크를 위험 분석에 사용, 주로 이론적 관점

#### MO4: Situation Awareness Model (SA-ISRM) [72]

**목적:**
- 정보 보안 위험 관리 프로세스 보완
- 실무에서의 결함 완화 (잘못된 의사결정, 부적절한 보안 전략 초래)

**접근:**
- 기업 전체의 위험 관련 정보 수집, 분석, 커뮤니케이션
- 미국 국가 안보 정보 기업의 사례 연구로 정제

**한계:**
- 모든 유형의 기업과 섹터에 대한 적용 가능성 미고려
- 지식 재사용 메커니즘 없음

#### MO5: Security Data-Driven Approach [26]

**핵심 개념:**
- 조직의 데이터 생애주기 프로세스 지향 (생성, 편집, 시각화, 처리, 전송, 저장)
- 자산 계층(논리적, 물리적, 인적)에 적응
- 사전 정의된 패턴 활용

**구조:**
- 보안 요구사항의 피라미드
- 각 피라미드는 계층적 다층 구조: 보안 문제, 관련 비즈니스 프로세스, 추출된 보안 데이터, 관련 자산, 식별된 위험, 보안 통제의 최적 조합

**검증:**
- 간단한 비교 사례 연구
- 매우 일반적이며 소프트웨어 도구 지원 없음

#### MO6: Threat-Occurrence Predictive Models [73]

**핵심 개념:**
- 더 현실적인 위험 추정 달성
- 예측 모델로 효율성 증가
- 과거 위협 빈도를 미래 위협 확률로 대체
- 로지스틱 회귀 접근법 사용

**기여:**
- 동적 적응의 중요성 (조직의 실제 조건과 변화 고려)
- 모든 유형 기업, 특히 SME 적응 중요성 강조
- 사례 연구로 모델 적용 및 정제

**한계:**
- 동적 적응 측면 미고려
- 지식 재사용 메커니즘 없음

#### MO7: Data Breach Management Model [74]

**초점:**
- 조직의 데이터 보안
- 보안 사고 관리 및 동적 보안 환경에서의 데이터 유출 관리

**기여:**
- 위험에 대한 전체적 접근법 중요성
- 데이터 유출 위험 및 관련 관리에 특화
- 휴리스틱 기법으로 동적 역량 적응 필요성
- 계층적 관계 고려
- 사례 연구 정의

**한계:**
- 이론적 연구
- 실무 검증 없음

#### MO8: Bi-Objective Integer Programming for Cyber-infrastructure [75]

**핵심 접근:**
- 확률적-결정론적 위험 평가 모델
- 각 검토/개선 순환에서 보안 통제 집합 선택
- 주어진 예산 내 잔여 위험 최적화

**기여:**
- 기술적 의사결정과 경제적 의사결정 통합
- 예산 제약이라는 실제 시나리오 반영
- 이중 확률적-결정론적 접근으로 불확실성 고려

**적용:**
- IT 기반 공급망에 초점
- 다른 영역에도 적용 가능

**한계:**
- 이론적 연구
- 실무 검증 없음

#### MO9: Configurable Dependency Model for SCADA [76]

**목적:**
- 산업 제어 시스템(ICS) 전용 목표 지향 위험 분석 모델
- SCADA 장치의 기술적/비기술적 하위 요소 간 다중 의존성 동적 평가

**기여:**
- 동적 및 적응형 모델의 중요성
- 시스템의 특정 컨텍스트 의존성 고려
- 변화하는 상황에 적응
- 특정 섹터/기술에 적응된 위험 분석 프로세스 필요성
- 물 제어 시스템 사례 연구

**한계:**
- 의존성 재구성이 수동
- 도메인 전문가 필요
- 순수 운영 기술(OT) 환경 외 시스템에 외삽 어려움

### 5. Methodology 유형 연구 (6개)

#### ME1: MAGERIT Fuzzification [77]

**핵심 접근:**
- MAGERIT 방법론을 퍼지 계산 모델로 확장
- 전통적 방법론의 측정 기법에서 불확실성 정도 감소

**기여:**
- 측정 값, 의존성, 빈도, 자산 저하를 표현하는 언어적 용어 척도
- 정보 시스템 자산 간 관계가 내부적이며 제3자 의존적일 수 있음 인정
- 연관 요인 고려 필요성 지지

**한계:**
- 이론적 연구
- 실무 검증 없음

#### ME2: FMEA with Fuzzy Similarity [78]

**핵심 접근:**
- FMEA 기법, 특히 규칙 기반 접근법과 퍼지 기법 통합
- 퍼지 숫자의 측정 값 유사성과 가능성 이론 통합

**목적:**
- 위험 분석에서 자의성 감소, 따라서 불확실성 감소

**한계:**
- 이론적 연구
- 실무 검증 없음

#### ME3: Functional QSRA for Critical Infrastructure [79]

**핵심 접근:**
- 중요 기반시설 지향 정량적 보안 위험 평가 방법론
- 동시 위협 및 취약점 평가 접근
- Bow Tie 위험 모델을 베이지안 네트워크 모델에 매핑
- 위험/취약점 확률을 잠재적 손실 값과 통합

**관련 연구:**
Abdo et al. [80]도 화학 시설에 초점을 맞춘 Bow Tie 모델 사용

**특징:**
- 화학 시설에 초점 (실제 사례 연구 준비)
- 요소 구성 및 커스터마이징으로 모든 중요 기반시설에 적응 가능
- 전문가 지식 필요

**검증:**
- 사례 연구로 방법론 적용 및 정제
- 매우 일반적이며 소프트웨어 도구 지원 없음

#### ME4: Risk Assessment for IoT [81]

**핵심 접근:**
- IoT 환경에 적용 가능한 위험 분석 및 관리 방법론
- 질적 및 양적 방법
- 각 시나리오에 적응된 공격 트리 구축
- Exploitability Value 기준

**프로세스:**
- 질적 수준으로 시스템 공격 난이도 평가
- 구체적 양적 값으로 변환
- 식별된 취약점 간 의존성 그래프 기반으로 전체 exploitability value 계산

**한계:**
- 본질적으로 이론적
- 실무 사례 적용했으나 너무 전역적
- 프로세스 상세 정보 부족
- 유지보수에 높은 수준의 전문가 지식 필요
- 물리적 구성요소 공격 위험에 주로 초점 (너무 특화됨)

#### ME5: Dynamic Simulation for SME Cyber Risk [82]

**목적:**
- SME 지향 사이버 위험 평가 방법론
- 사이버 보안 투자 의사결정 지원 지표 및 동적 메트릭

**특징:**
- 소규모 기업에 간단히 적용 가능
- 동적 조직 복잡성 적응
- 시간 경과에 따른 사이버 위험 및 관련 동적 특성 평가

**도구:**
- SMECRA(SME Cyber Risk Assessment) 지원 도구 제공

**한계:**
- 경제적 관점에서 위험 시나리오 시뮬레이션에 주로 초점
- 글로벌 위험 관리 미지원

#### ME6: Fuzzy Model for Human-Robot Systems [83]

**목적:**
- 새로운 운영 패러다임(인간과 로봇의 상호 의존성) 적응 특화 위험 분석 방법론

**기여:**
- 변화하고 예측 불가능한 환경(HMI)을 위한 특화 위험 분석 프로세스 중요성
- 높은 불확실성과 잠재적 위험 상황 고려
- 퍼지 집합 이론과 z-numbers를 사용한 MCDM 기반 방법론

**한계:**
- 근본적으로 이론적 연구
- 실무 사례 미테스트
- 지원 도구 없음
- 지식 재사용 메커니즘 미고려
- 상당한 전문가 지식 없이 적용 어려움

### 6. Others 유형 연구 (2개)

#### O1: Risk Improvement Factor Formula [84]

**제안:**
- 조직의 정보 보안 위험 분석 프로세스를 위한 질적 접근
- 위험 수준에 대한 점진적 개선 요인 고려

**기여:**
- 의사결정의 중요한 요인으로 고려 가능

**한계:**
- 이론적 연구
- 실무 검증 없음

#### O2: Security Risk in Hybrid Data Centers [85]

**내용:**
- 데이터 센터 특정 분야의 위험 분석 및 관리 프로세스 필요성에 관한 논의 연구
- 특정 메커니즘 제안/정의 없음

**관련 개념:**
- 물리적 서버뿐 아니라 가상 서버가 받는 위험도 포함 필요
- 클라우드 컴퓨팅 새 필요사항과 연계
- 전통적 물리 시스템과 가상 시스템 공존
- 가상화로 파생된 연관 위험

**초기 작업:**
- 데이터 센터 초점의 위험 및 취약점 초기 선정 (가상 서버 특화 포함)
- VoIP 서비스의 가용성 측면 평가 사례 연구 (초기 단계, 상세 부족)

### 7. Day 2 종합 분석

**주요 발견:**

1. **이론과 실무의 격차**
   - 30개 연구 중 대다수가 이론적 수준
   - 실무 사례로 검증된 연구: P2, MO1, MO2, MO4, MO5, MO6, MO9, ME3, ME4, ME5, O2 일부
   - 복잡한 실무 환경에서 정제/검증된 연구는 소수

2. **기법적 접근의 공통점**
   - 퍼지 기법(Fuzzy Techniques) 광범위 사용: 불확실성 감소 목적
   - MCDM(다기준 의사결정) 방법 선호
   - 베이지안 네트워크 활용: 인과 관계 및 불확실성 모델링

3. **도구 지원 부족**
   - 대부분의 연구가 소프트웨어 도구 미제공
   - 도구 제공 사례: P2(CRE), ME5(SMECRA), F9(일부)
   - 실무 적용을 위한 자동화 부족

4. **특화 vs 일반화**
   - 특정 도메인 특화: SDN(P3), 철도(P4), SCADA/ICS(MO9), IoT(ME4), HMI(ME6)
   - 일반화 추구: 대부분의 Framework와 Model
   - 특화 연구는 실무 적용 가능성 높으나 범용성 낮음

5. **주요 기법 트렌드**
   - DEMATEL-ANP 조합
   - VIKOR-DEMATEL-ANP 통합
   - Fuzzy 기법 (Fuzzy Sets, Fuzzy Logic, Fuzzy MCDM)
   - FMEA (Failure Mode and Effect Analysis)
   - Bayesian Networks
   - PDCA (Plan-Do-Check-Act) 순환

---

**Day 2 마무리:**  
30개 연구의 상세 분석을 통해 현재 위험 분석 연구의 풍경을 파악했다. 대다수 연구가 이론적 수준에 머물러 있으며, 퍼지 기법과 다기준 의사결정 방법을 선호한다. 실무 검증이 이루어진 연구는 소수이며, 자동화 도구 지원은 거의 없다. 특정 도메인(IoT, SCADA, 클라우드)에 특화된 연구들이 등장하고 있으나, 범용적 적용 가능성은 제한적이다. 내일 Day 3에서는 Table 3의 12가지 기준으로 이 30개 연구를 정량적으로 비교 분석하여, 어떤 연구도 모든 요구사항을 충족하지 못한다는 것을 확인할 예정이다.

# Research Review: Towards an Integrated Risk Analysis Security Framework
> **Day 3 Focus:** 12가지 기준 기반 정량적 비교 분석  
> **Source:** Section 5 (Analysis of Results) & Table 3

---

## Day 3 – Comparative Analysis Results
*(Table 3: 30개 연구의 체계적 비교와 한계)*

### 1. 평가 프레임워크: 12가지 기준

논문은 30개 선정 연구를 12가지 기준으로 평가했다. 각 기준은 3단계로 평가된다:
- **Yes**: 완전히 충족
- **Part**: 부분적으로 충족
- **No**: 미충족

#### 기준 1~10: 과학 커뮤니티가 식별한 바람직한 특성

| 코드 | 명칭 | 정의 | 출처/근거 |
|------|------|------|-----------|
| **AC** | Adaptive Catalogues | 유연성을 높이기 위한 적응형 카탈로그 필요성 | [39, 81, 86] |
| **HA** | Hierarchy and Associativity | 연관 및 계층 구조 고려 필요. Cloud 전환으로 중요성 증가 | [87-89] |
| **RKL** | Reuse Knowledge and Learning | 이전 위험 분석의 지식 재사용으로 더 나은 분석 수행 | [90], 의사결정 지원 기법 [73, 91, 92] |
| **DY** | Dynamic and Evolutionary | 위험 분석은 비용 많이 드는 프로세스. 정적 그림이 아닌 동적 시스템 필요 | [49] |
| **CC** | Collaborative Capability | 여러 기업이 위험 시스템을 정렬하여 더 효율적 관리 | [93, 94] |
| **AE** | Valuation of Elements | 위험 관련 요소의 정량적 평가 메커니즘 부족 | [95], 비용 계산 [96] |
| **DM** | Dynamic Metrics | 동적 위험 메트릭 개발 및 자동화 필요 | [97], 적절한 메트릭 필요성 [98] |
| **LLS** | Low Level of Subjectivity | 주관적 측면 많아 제3자가 객관적 결과 신뢰 어려움 | [99, 100] |
| **SLC** | Simplicity and Low Cost | 많은 방법론의 높은 복잡도. 단순성과 실용적 지향 중요 | [101, 102], 특히 SME [103-106] |
| **TS** | Tool Support | 자동화 도구 지원이 근본적 요소 | [60, 107], NATO 강조 |

#### 기준 11~12: 저자들이 Action Research로 추가한 특성

| 코드 | 명칭 | 정의 | 추가 근거 |
|------|------|------|-----------|
| **GS** | Global Scope | 모델이 기업의 정보 시스템 보안에 전역적으로 적용되는지, 하위 집합만인지 | 실무 경험 |
| **PC** | Practical Cases | 실무 사례 기반으로 개발 및 정제되어 실제 적용 가능성 강화 | 실무 경험 |

### 2. Table 3 정량적 분석 결과

#### A. Process 유형 (P1-P4)

| 연구 | AC | HA | RKL | DY | CC | AE | DM | LLS | SLC | TS | GS | PC |
|------|----|----|-----|----|----|----|----|----|-----|----|----|-----|
| **P1** | No | Part | No | No | No | Part | No | No | No | No | No | No |
| **P2** | No | Part | No | No | No | Part | No | No | No | Yes | No | Yes |
| **P3** | No | Part | No | No | No | Part | No | Part | No | No | No | Part |
| **P4** | No | Part | No | No | No | Part | No | Part | No | No | No | No |

**주요 발견:**
- 모든 Process가 AC, RKL, DY, CC, DM, GS 미충족
- HA는 모두 부분적으로만 충족 (Part)
- P2만 도구 지원(TS)과 실무 사례(PC)에서 Yes
- 대부분 이론적이며 실무 검증 부족

#### B. Framework 유형 (F1-F9)

| 연구 | AC | HA | RKL | DY | CC | AE | DM | LLS | SLC | TS | GS | PC |
|------|----|----|-----|----|----|----|----|----|-----|----|----|-----|
| **F1** | No | Part | No | No | No | No | No | No | No | No | No | No |
| **F2** | No | No | Yes | No | No | No | No | No | No | No | No | No |
| **F3** | No | Part | Yes | No | No | No | No | No | No | No | Yes | No |
| **F4** | No | No | Part | No | No | No | No | Part | No | No | Yes | No |
| **F5** | No | No | No | No | No | Part | No | Part | No | No | No | No |
| **F6** | No | Part | Yes | Part | No | No | No | No | No | No | Yes | No |
| **F7** | No | No | No | No | No | Part | No | Part | No | No | Yes | No |
| **F8** | No | Part | Yes | No | No | Part | No | No | Yes | Yes | Yes | No |
| **F9** | Part | No | No | No | No | No | No | No | No | Part | Yes | Part |

**주요 발견:**
- F2, F3, F6, F8이 RKL(지식 재사용)에서 Yes
- F8이 가장 많은 기준 충족 (SLC, TS, GS 포함)
- F9가 유일하게 AC를 부분 충족
- CC(협업 능력)는 모든 Framework가 미충족
- 대부분 실무 사례(PC) 없음

#### C. Model 유형 (MO1-MO9)

| 연구 | AC | HA | RKL | DY | CC | AE | DM | LLS | SLC | TS | GS | PC |
|------|----|----|-----|----|----|----|----|----|-----|----|----|-----|
| **MO1** | No | Part | No | Part | No | Part | No | Part | No | No | Yes | Yes |
| **MO2** | No | No | Part | No | No | Part | No | No | No | No | Yes | Yes |
| **MO3** | No | Part | No | No | No | Part | No | Part | No | No | Yes | No |
| **MO4** | No | Part | Part | No | No | No | No | No | No | No | Yes | Yes |
| **MO5** | Part | Part | No | No | No | Part | No | No | No | No | No | Part |
| **MO6** | No | No | No | Part | No | No | No | Part | Part | No | Yes | Yes |
| **MO7** | No | Part | No | Part | No | No | No | No | No | No | No | No |
| **MO8** | No | No | No | Part | No | Part | No | No | No | No | No | No |
| **MO9** | Part | Yes | No | Yes | No | Part | No | No | No | No | No | Yes |

**주요 발견:**
- MO9가 HA에서 유일한 Yes (SCADA 의존성 모델)
- MO9가 DY에서도 Yes (동적 평가)
- Model 유형이 GS와 PC에서 상대적으로 높은 비율
- MO1, MO2, MO4, MO6, MO9가 실무 사례 보유
- AC, CC, DM은 거의 모든 Model이 미충족

#### D. Methodology 유형 (ME1-ME6)

| 연구 | AC | HA | RKL | DY | CC | AE | DM | LLS | SLC | TS | GS | PC |
|------|----|----|-----|----|----|----|----|----|-----|----|----|-----|
| **ME1** | No | Part | No | Part | No | Part | No | Part | No | No | Yes | No |
| **ME2** | No | Part | No | No | No | Part | No | Part | No | No | Yes | No |
| **ME3** | No | No | No | No | No | No | No | No | No | No | No | Yes |
| **ME4** | No | No | No | No | No | Part | No | No | No | No | No | Yes |
| **ME5** | No | No | No | Yes | No | Part | Yes | No | Yes | Yes | No | Yes |
| **ME6** | No | Part | No | No | No | No | No | Yes | No | No | No | No |

**주요 발견:**
- ME5가 DY와 DM에서 Yes (동적 시뮬레이션)
- ME5가 SLC, TS에서도 Yes (SME 지향, SMECRA 도구)
- ME3, ME4, ME5가 실무 사례 보유
- ME6이 LLS에서 유일한 Yes
- AC, RKL, CC는 모든 Methodology가 미충족

#### E. Others 유형 (O1-O2)

| 연구 | AC | HA | RKL | DY | CC | AE | DM | LLS | SLC | TS | GS | PC |
|------|----|----|-----|----|----|----|----|----|-----|----|----|-----|
| **O1** | No | No | Yes | No | No | Part | No | No | No | No | Yes | No |
| **O2** | No | Part | No | Part | No | No | No | No | No | No | No | Part |

### 3. 기준별 종합 분석

#### 기준별 충족 현황 (Yes 개수)

| 기준 | Yes 개수 | 주요 충족 연구 | 해석 |
|------|----------|----------------|------|
| **AC** | 0개 | 없음 | 적응형 카탈로그를 완전히 구현한 연구 전무 |
| **HA** | 1개 | MO9 | SCADA 의존성 모델만 계층/연관 구조 완전 지원 |
| **RKL** | 4개 | F2, F3, F6, F8, O1 | 지식 재사용은 일부 Framework에서만 구현 |
| **DY** | 2개 | MO9, ME5 | 동적 위험 관리는 극소수만 달성 |
| **CC** | 0개 | 없음 | 기업 간 협업 위험 관리 연구 전무 |
| **AE** | 0개 | 없음 | 요소의 정량적 평가를 완전히 구현한 연구 없음 |
| **DM** | 1개 | ME5 | 동적 메트릭은 SME 시뮬레이션에서만 구현 |
| **LLS** | 1개 | ME6 | 낮은 주관성은 HMI 퍼지 모델에서만 달성 |
| **SLC** | 3개 | F8, ME5 | 단순성/저비용은 SME 특화 연구에서만 |
| **TS** | 4개 | P2, F8, F9(Part), ME5 | 자동화 도구 제공 연구는 소수 |
| **GS** | 14개 | 다수 | 전역 범위 적용은 상대적으로 많은 연구가 추구 |
| **PC** | 9개 | 일부 | 실무 사례 검증은 30개 중 9개만 |

#### 기준별 미충족 비율

**완전 미충족 기준 (모든 연구가 No):**
- AC (Adaptive Catalogues): 100% 미충족
- CC (Collaborative Capability): 100% 미충족

**거의 미충족 기준 (Yes 1-2개):**
- HA (Hierarchy & Associativity): 96.7% 미충족
- DY (Dynamic & Evolutionary): 93.3% 미충족
- DM (Dynamic Metrics): 96.7% 미충족
- LLS (Low Level of Subjectivity): 96.7% 미충족

**상대적으로 나은 기준 (Yes 3개 이상):**
- RKL (Reuse Knowledge & Learning): 4개 Yes
- TS (Tool Support): 4개 Yes
- GS (Global Scope): 14개 Yes
- PC (Practical Cases): 9개 Yes

### 4. 논문의 결론 (Section 5 원문 기반)

논문은 Table 3 분석을 통해 다음을 결론짓는다:

#### AC - Adaptive Catalogues
> "Practically no proposal orients part of its operation towards the existence of element catalogues that can vary over time without altering the methodology."

**해석:** 사실상 어떤 제안도 방법론을 변경하지 않고 시간에 따라 변화하는 요소 카탈로그 존재를 지향하지 않음.

#### HA - Hierarchy and Associativity
> "None of the proposals fully takes into account the concepts of hierarchy and associativity among risk analyses, leaving aside fundamental concepts such as shared assets or dependencies among different risk analyses. However, many have already begun to consider that this aspect is fundamental."

**해석:** 어떤 제안도 계층과 연관성 개념을 완전히 고려하지 않음. 공유 자산이나 서로 다른 위험 분석 간 의존성 같은 근본 개념 누락. 그러나 많은 연구가 이 측면이 근본적임을 인식하기 시작함.

#### RKL - Knowledge Reuse and Learning
> "Only a few proposals highlight the need to be able to reuse knowledge for future implementations. But few of them implement adequate processes for knowledge reuse, and especially for learning from experience."

**해석:** 소수만 미래 구현을 위한 지식 재사용 필요성 강조. 그러나 적절한 재사용 프로세스를 구현한 연구는 더 적으며, 특히 경험으로부터 학습하는 메커니즘은 거의 없음.

#### DY - Dynamic and Evolutionary
> "Some proposals highlight the need for risk analysis to be dynamic, but without providing complete solutions with which to make the system dynamic. The remaining proposals do not consider this characteristic."

**해석:** 일부 제안만 동적 위험 분석 필요성 강조하나, 시스템을 동적으로 만들 완전한 솔루션 미제공. 나머지 제안들은 이 특성을 고려하지 않음.

#### CC - Collaborative Capacity
> "None of the proposals studied considers the concept of collaborative networks among companies as a solution by which to better protect companies from external threats."

**해석:** 연구된 제안 중 어떤 것도 외부 위협으로부터 기업을 더 잘 보호하기 위한 솔루션으로서 기업 간 협업 네트워크 개념을 고려하지 않음.

#### AE - Valuation of Elements
> "Not all the proposals contemplate the valuation of elements as part of this, i.e., taking into account aspects such as the quantitative value of assets, impacts, etc. However, quite a few of them do analyse some of these aspects."

**해석:** 모든 제안이 요소 평가를 고려하지는 않음 (자산의 정량적 가치, 영향 등). 그러나 상당수가 일부 측면은 분석함.

#### DM - Dynamic Metrics
> "Although many of the proposals include formulas with which to calculate risk, none of them consider the possibility of these formulas being dynamic, i.e., that they could be sufficiently versatile to calculate risk in different ways from the basic elements of the risk analysis."

**해석:** 많은 제안이 위험 계산 공식 포함하나, 이 공식이 동적일 가능성을 고려한 연구는 없음. 즉, 위험 분석의 기본 요소로부터 다양한 방식으로 위험을 계산할 수 있을 만큼 충분히 다재다능한 공식 없음.

#### LLS - Low Level of Subjectivity
> "With regard to the development of additional mechanisms with which to reduce the level of subjectivity, some proposals have made efforts in this direction, albeit at a conceptual level."

**해석:** 주관성 수준 감소를 위한 추가 메커니즘 개발과 관련하여, 일부 제안이 이 방향으로 노력했으나 개념 수준에 그침.

#### SLC - Simplicity and Low Cost
> "The orientation towards simple methodologies and models that can be applied by SMEs has barely been taken into account as a differentiating factor in the proposals studied, signifying that no real mechanisms have been developed that would allow these proposals to be really useful for SMEs."

**해석:** SME가 적용 가능한 단순 방법론/모델 지향은 연구된 제안에서 차별화 요소로 거의 고려되지 않음. 이는 SME에 실제로 유용한 제안을 가능하게 할 실제 메커니즘이 개발되지 않았음을 의미.

#### TS - Tool Support
> "Some proposals have already identified the need to be supported by tools in order to automate part of their processes. Other proposals have developed partial tools that support part of the process."

**해석:** 일부 제안은 프로세스 일부 자동화를 위한 도구 지원 필요성 식별. 다른 제안들은 프로세스 일부를 지원하는 부분 도구 개발.

#### GS - Global Scope
> "Although some proposals are already oriented towards their application in the scope of an Information System as a whole, there are still many that are focused on specific areas. This signifies that they should be complemented with other mechanisms in order to achieve a risk analysis with a complete scope."

**해석:** 일부 제안이 정보 시스템 전체 범위 적용을 지향하나, 여전히 많은 연구가 특정 영역에 초점. 이는 완전한 범위의 위험 분석 달성을 위해 다른 메커니즘으로 보완되어야 함을 의미.

#### PC - Practical Cases
> "Most of the proposals contemplate risk analysis from a theoretical point of view, without establishing concrete risk-management mechanisms based on practical cases."

**해석:** 대부분의 제안이 이론적 관점에서 위험 분석을 고려하며, 실무 사례 기반의 구체적 위험 관리 메커니즘을 확립하지 않음.

### 5. 핵심 통찰

**논문이 명시적으로 밝힌 결론:**

> "As Table 3 shows, very few papers describe complex case studies that show the possibility of applying the proposed model or methodology in practice, and the benefits that could be attained from doing so. Moreover, although some of them attempt to develop dynamic low-cost processes, they have a high level of complexity as regards their implementation."

**번역:** Table 3이 보여주듯, 제안된 모델/방법론을 실무에 적용할 가능성과 그로부터 얻을 수 있는 이점을 보여주는 복잡한 사례 연구를 기술한 논문은 매우 적음. 더욱이, 일부는 동적 저비용 프로세스 개발을 시도하나 구현과 관련하여 높은 복잡도를 가짐.

> "It will be noted that none of the proposals studied has all the characteristics required for them to be implemented in any type of company, regardless of its characteristics and size."

**번역:** 연구된 제안 중 어떤 것도 특성과 규모에 관계없이 모든 유형의 기업에 구현되기 위해 필요한 모든 특성을 갖추지 못했음을 주목해야 함.

**정량적 증거:**
- 30개 연구 중 **0개**가 12가지 기준을 모두 충족
- 30개 연구 중 **0개**가 10개 이상 기준 충족
- 가장 높은 점수: MO9와 ME5가 각각 4-5개 기준에서 Yes/Part
- 평균적으로 각 연구는 12개 기준 중 1-3개만 충족

---

**Day 3 마무리:**  
Table 3의 정량적 분석은 명확한 결론을 제시한다: **30개 연구 중 어떤 것도 현대 위험 분석의 모든 요구사항을 충족하지 못한다.** 특히 AC(적응형 카탈로그)와 CC(협업 능력)는 단 하나의 연구도 구현하지 못했으며, HA(계층/연관성), DY(동적), DM(동적 메트릭), LLS(낮은 주관성)는 각각 1-2개 연구만 완전 충족했다. 대부분의 연구가 이론적 수준에 머물러 있으며(PC 30개 중 9개만 Yes), SME가 실제로 적용 가능한 단순하고 저비용인 솔루션(SLC)은 3개만 제공했다. 이러한 체계적 분석 결과가 MARISMA 프레임워크 개발의 직접적 동기가 되었다. 내일 Day 4에서는 MARISMA가 이 10가지 약점을 어떻게 해결하는지 구체적으로 분석할 예정이다.

# Research Review: Towards an Integrated Risk Analysis Security Framework
> **Day 4 Focus:** MARISMA 프레임워크의 구조와 약점 해결 메커니즘  
> **Source:** Section 6 (The MARISMA Framework)

---

## Day 4 – MARISMA Framework Analysis
*(10가지 약점의 체계적 해결: 이론에서 실무로)*

### 1. MARISMA 개요

**정식 명칭:**  
MARISMA = **M**ethodology for the **A**nalysis of **RI**sks on Information **S**ystems, using **M**eta-pattern and **A**daptability

**개발 배경:**
> "The shortcomings identified during the systematic review have been used as the basis on which to propose the development of a framework called MARISMA."

체계적 문헌 고찰에서 식별된 약점들을 기반으로 개발된 프레임워크.

**개발 과정:**
> "The MARISMA framework originated as the main result of several PhD theses of members of our research team. It has been developed using an iterative and incremental process and is directly applied to customers of our spin-offs."

- 연구팀 여러 박사 논문의 주요 결과물
- 반복적이고 점진적인 프로세스로 개발
- Spin-off 회사의 고객에게 직접 적용 중

### 2. MARISMA의 4대 구성 요소

#### 구성 요소 1: Meta-Pattern (CAT 구조)

**정의:**
> "The first of these elements is a structure denominated as a meta-pattern (number 1 in Fig. 1), whose objective is to support the different information models of the methodology, and which contains the elements required in order to be able to perform a risk analysis and its subsequent management."

**CAT 구조:**
- **C**ontrol (통제)
- **A**sset (자산)
- **T**hreat (위협)

**특징:**
> "This meta-pattern is made up of three base elements, denominated as Control-Asset-Threat (CAT) (see Fig. 2), and two matrices connecting these elements. The meta-pattern is a common structure for all the patterns (normative schemes in which to perform the risk analysis) that are applied in the methodology."

- 3개 기본 요소 + 2개의 연결 매트릭스
- 모든 패턴(위험 분석 수행을 위한 규범적 스킴)의 공통 구조
- 방법론에 적용되는 모든 패턴의 기반

#### 구성 요소 2: 3가지 핵심 프로세스

**2-1. RPG (Risk Pattern Generator) Process**

**목적:**
> "The RPG (Risk Pattern Generator) Process, whose objective is the Generation of patterns for risk analysis, including their relationships and the knowledge acquired in the different implementations"

- 위험 분석용 패턴 생성
- 관계 포함
- 다양한 구현에서 획득한 지식 포함

**2-2. RAMG (Risk Analysis and Management Generator) Process**

**목적:**
> "The RAMG (Risk Analysis and Management Generator) Process, which deals with the Generation of risk analysis and management through the instantiation of the most appropriate pattern."

- 가장 적합한 패턴의 인스턴스화를 통한 위험 분석 및 관리 생성

**추가 기능:**
> "It also allows the definition of dynamic metrics with which to value assets and the risk calculation formula itself, thus making it possible to solve the problems of AE - Valuation of Elements and DM - Dynamic Metrics"

- 자산 가치 평가를 위한 동적 메트릭 정의
- 위험 계산 공식 자체 정의
- **AE와 DM 문제 해결**

**2-3. DRM (Dynamic Risk Management) Process**

**목적:**
> "The DRM (Dynamic Risk Management) Process, which deals with the dynamic maintenance of risk analysis through the use of the matrices that interconnect the different artefacts"

- 서로 다른 요소를 상호 연결하는 매트릭스 사용
- 위험 분석의 동적 유지관리

**작동 메커니즘:**
> "that allow the system to recalculate the risk as security incidents occur, the defined metrics fail, or the expert systems generate suggestions."

- 보안 사고 발생 시 위험 재계산
- 정의된 메트릭 실패 시 위험 재계산
- 전문가 시스템이 제안 생성 시 위험 재계산

#### 구성 요소 3: Knowledge Base

**구조:**
> "This framework also has a third element. This is a knowledge base of patterns (number 3 in Fig. 1) that allows the maintenance of different normative patterns, along with the knowledge acquired from their instantiation in the different risk analyses."

- 다양한 규범적 패턴 유지
- 서로 다른 위험 분석에서의 인스턴스화로부터 획득한 지식 유지

#### 구성 요소 4: eMARISMA Tool

**기술 스택:**
> "The eMARISMA tool is based on cloud computing and was developed using an open architecture based on Java technology under Grails. Its security layers are based on Spring Security and ACL (Access Control List) and its relational schema is supported by MySQL."

- 클라우드 컴퓨팅 기반
- Java/Grails 기반 오픈 아키텍처
- Spring Security와 ACL로 보안 계층 구현
- MySQL 관계형 스키마

**아키텍처 (Fig. 5):**
> "It is divided into two independent parts (see Fig.5). On the one hand, there is the pattern generator, which functions as a pattern repository and a knowledge repository. On the other, there is the risk and event analysis manager, which can be located on different servers, and which communicates with the pattern module in order to instantiate patterns and send new knowledge to it."

**두 개의 독립적 부분:**
1. **Pattern Generator**
   - 패턴 저장소로 기능
   - 지식 저장소로 기능

2. **Risk and Event Analysis Manager**
   - 다른 서버에 위치 가능
   - 패턴 모듈과 통신하여 패턴 인스턴스화
   - 새로운 지식을 패턴 모듈에 전송

### 3. MARISMA의 약점 해결 메커니즘

논문은 각 구성 요소가 어떻게 10가지 약점을 해결하는지 명시적으로 설명한다:

#### 해결 메커니즘 1: AC (Adaptive Catalogues)

**문제:**
> "The use of the Meta-pattern makes it possible to solve the problem of having 'AC - Adaptive Catalogues', by providing a knowledge base with different patterns that can evolve"

**해결책:**
- Meta-pattern 사용으로 진화 가능한 서로 다른 패턴의 지식 베이스 제공

**추가 혁신:**
> "and in which controls have been included as an integrated element. Most existing methodologies do not, however, consider controls or safeguards until the risk management phase, considering it an independent element of assets, threats and vulnerabilities, and thus complicating the development and monitoring of risk analysis."

- Control을 통합 요소로 포함 (CAT 구조)
- 기존 방법론: 위험 관리 단계까지 Control 미고려 → 자산/위협/취약점과 독립적 요소로 간주
- MARISMA: Control을 처음부터 통합 → 위험 분석 개발 및 모니터링 단순화

#### 해결 메커니즘 2: RKL (Reuse Knowledge and Learning)

**문제 해결:**
> "Furthermore, the ability to learn from these patterns, along with the concept of legacy, which is implemented through the use of inter-pattern relationships, both make it possible to fulfil the need for 'RKL - Reuse of Knowledge and Learning', since this structure allows this knowledge to be stored and the patterns to evolve over time."

**해결책:**
- 패턴으로부터 학습하는 능력
- Legacy 개념 (패턴 간 관계를 통해 구현)
- 지식 저장 가능
- 시간 경과에 따른 패턴 진화

#### 해결 메커니즘 3: DY (Dynamic and Evolutionary)

**복잡한 상호작용:**

**3개 프로세스 간 정보 교환:**
> "The 'DY - Dynamic and evolutionary' problem is solved by using the three processes of the methodology. These processes exchange information in order to make the system learn and evolve:"

**단계별 동작:**

**(i) 이벤트 생성:**
> "The generation of an event in the DRM process causes:"

**(ii) 인스턴스 진화:**
> "The instance associated with the event to evolve by changing aspects such as the level of coverage of a control, or the probability of occurrence of a threat associated with the RAMG process"

- DRM 프로세스에서 이벤트 생성
- RAMG 프로세스 관련 인스턴스 진화
- Control 커버리지 수준 변경
- 위협 발생 확률 변경

**(iii) 패턴 변화:**
> "Changes in the pattern associated with the instance that was created by the RPG process, thus allowing it to readjust the relationships between its elements, and to readjust elements associated with the temporary external risk, thereby helping to create a global security shield among the companies that use that pattern"

- RPG 프로세스가 생성한 인스턴스 관련 패턴 변화
- 요소 간 관계 재조정
- 임시 외부 위험 관련 요소 재조정
- 해당 패턴 사용 기업들 간 글로벌 보안 실드 생성 지원

**(iv) Legacy를 통한 지식 전파:**
> "Furthermore, when a pattern undergoes changes as a result of the learning of the instances, these also evolve by means of the legacy principle, and the acquired knowledge is transmitted"

- 인스턴스 학습 결과로 패턴 변화
- Legacy 원칙으로 진화
- 획득한 지식 전파

**(v) 모든 인스턴스로 진화 전파:**
> "The changes that produce evolution in the patterns are eventually transmitted to all the instances in order to help them to improve, thus producing an evolution in them."

- 패턴의 진화를 생성하는 변화가 모든 인스턴스에 전송
- 인스턴스 개선 지원
- 인스턴스에서 진화 생성

#### 해결 메커니즘 4: LLS (Low Level of Subjectivity)

**두 가지 접근:**
> "The problem of 'LLS - Low Level of Subjectivity' has been solved by implementing different methods: on the one hand, in the RAMG process we perform a pre-audit with a higher level of accuracy that reduces the initial level of ambiguity"

**방법 1: Pre-audit (RAMG 프로세스)**
- 더 높은 정확도의 사전 감사 수행
- 초기 모호성 수준 감소

**방법 2: Expert System (DRM 프로세스)**
> "and on the other, in the DRM process we have implemented an expert system of suggestions that learns from the events in order to make the system tend towards reality as security events occur."

- 제안 전문가 시스템 구현
- 이벤트로부터 학습
- 보안 이벤트 발생 시 시스템이 현실에 가깝게 경향

#### 해결 메커니즘 5: CC (Collaborative Capacity)

**패턴 Legacy 활용:**
> "The 'CC - Collaborative Capacity' problem is solved through the use of pattern legacy, along with the ability to acquire and share the information obtained in the DRM process among the different instances of a pattern, or its ascendants-descendants."

**해결책:**
- Pattern Legacy 사용
- DRM 프로세스에서 얻은 정보를 패턴의 서로 다른 인스턴스 간 획득 및 공유
- 또는 조상-자손 간 공유

#### 해결 메커니즘 6: SLC & TS (Simplicity, Low Cost, Tool Support)

**통합 해결:**
> "In order to automate all the tasks and take advantage of the learning and dynamism capabilities, the eMARISMA tool has been implemented, thus providing a solution to the problems of 'SLC - Simplicity and Low Cost' and 'TS - Supported by Tools'."

**해결책:**
- eMARISMA 도구 구현
- 모든 작업 자동화
- 학습 및 동적 특성 활용
- **SLC와 TS 문제 동시 해결**

#### 해결 메커니즘 7: AE & DM (Valuation of Elements, Dynamic Metrics)

**RAMG 프로세스 기능:**
앞서 명시됨 - RAMG 프로세스가 동적 메트릭 정의 허용
- 자산 가치 평가
- 위험 계산 공식 자체
- **AE와 DM 문제 해결**

#### 해결 메커니즘 8: GS & PC (Global Scope, Practical Cases)

**Knowledge Base와 Tool의 역할:**
> "The tool also makes it possible to support the knowledge base, allowing specialised patterns to be obtained for different application scopes. This, therefore, provides a solution to the problem of 'GS - Scope of application', in addition to having a wide base of practical cases that allow the system to learn and evolve in the face of changing circumstances and technologies. A solution to the problem of 'PC - Practical Cases' is, therefore, provided."

**해결책:**
- 도구가 지식 베이스 지원
- 다양한 적용 범위를 위한 특화 패턴 획득 가능
- **GS 문제 해결**
- 변화하는 상황과 기술에 직면하여 시스템이 학습하고 진화할 수 있는 광범위한 실무 사례 기반
- **PC 문제 해결**

### 4. 실무 적용 현황

#### 적용 규모

**지리적 범위:**
> "We are specifically applying MARISMA in order to carry out the risk analysis and management of dozens of companies in Spain, Colombia, Ecuador, and Argentina"

- 스페인, 콜롬비아, 에콰도르, 아르헨티나
- 수십 개 기업

**산업 섹터:**
> "and from different sectors, such as government, critical infrastructures, hydrocarbons, chemical, and naval."

- 정부
- 중요 기반시설 (Critical Infrastructures)
- 석유화학 (Hydrocarbons)
- 화학 (Chemical)
- 조선 (Naval)

#### 지속적 개선 프로세스

**피드백 루프:**
> "This has allowed us to evaluate and improve each component of the risk analysis and management framework."

- 위험 분석 및 관리 프레임워크의 각 구성 요소 평가
- 각 구성 요소 개선

**개발 방식:**
> "It has been developed using an iterative and incremental process"

- 반복적이고 점진적인 프로세스

### 5. 약점 해결 매핑 요약

| 약점 | 해결 구성 요소 | 해결 메커니즘 |
|------|----------------|---------------|
| **AC** | Meta-Pattern | 진화 가능한 패턴 지식 베이스, Control 통합 |
| **HA** | *논문에 명시적 언급 없음* | *CAT 구조로 암묵적 지원 추정* |
| **RKL** | Meta-Pattern, Knowledge Base | 패턴으로부터 학습, Legacy 개념, 지식 저장 및 진화 |
| **DY** | 3 Processes (RPG, RAMG, DRM) | 프로세스 간 정보 교환, 이벤트 기반 재계산, Legacy 전파 |
| **CC** | Pattern Legacy, DRM Process | 패턴 인스턴스 간 정보 공유, 조상-자손 간 공유 |
| **AE** | RAMG Process | 동적 메트릭으로 자산 가치 평가 정의 |
| **DM** | RAMG Process | 위험 계산 공식 동적 정의 |
| **LLS** | RAMG (Pre-audit), DRM (Expert System) | 사전 감사로 모호성 감소, 전문가 시스템으로 현실 경향 |
| **SLC** | eMARISMA Tool | 작업 자동화 |
| **TS** | eMARISMA Tool | 작업 자동화, 학습/동적 특성 활용 |
| **GS** | Knowledge Base, Tool | 다양한 적용 범위를 위한 특화 패턴 |
| **PC** | Knowledge Base, Real Deployment | 광범위한 실무 사례 기반, 4개국 수십 개 기업 적용 |

**주목할 점:**
- HA(Hierarchy & Associativity)에 대한 명시적 해결 메커니즘 설명이 Section 6에 없음
- 그러나 CAT Meta-Pattern 구조 자체가 Control-Asset-Threat 간 관계를 다루므로 암묵적으로 지원하는 것으로 해석 가능

### 6. MARISMA의 핵심 혁신

#### 혁신 1: Control의 통합

**기존 방법론의 문제:**
> "Most existing methodologies do not, however, consider controls or safeguards until the risk management phase, considering it an independent element of assets, threats and vulnerabilities"

- Control을 위험 관리 단계까지 미고려
- 자산/위협/취약점과 독립적 요소로 간주
- 위험 분석 개발 및 모니터링 복잡화

**MARISMA의 접근:**
- CAT 구조로 Control을 처음부터 통합
- 자산, 위협과 동등한 1급 요소로 취급
- 위험 분석 개발 및 모니터링 단순화

#### 혁신 2: 동적 학습 순환

**5단계 순환:**
```
[DRM: 이벤트 발생]
    ↓
[RAMG: 인스턴스 진화]
    ↓
[RPG: 패턴 변화]
    ↓
[Legacy: 지식 전파]
    ↓
[모든 인스턴스로 진화 전파]
    ↓
[DRM으로 순환]
```

이 순환이 **DY 문제의 핵심 해결 메커니즘**

#### 혁신 3: 글로벌 보안 실드

**개념:**
> "thereby helping to create a global security shield among the companies that use that pattern"

- 동일 패턴 사용 기업들 간 지식 공유
- 한 기업의 보안 이벤트가 다른 기업의 위험 평가에 기여
- 집단 지성을 통한 보안 강화

이것이 **CC 문제의 핵심 해결 메커니즘**

#### 혁신 4: 이중 불확실성 감소

**방법 1: RAMG의 Pre-audit**
- 초기 모호성 감소
- 더 높은 정확도

**방법 2: DRM의 Expert System**
- 이벤트로부터 학습
- 시간 경과에 따라 현실에 수렴

두 방법의 조합이 **LLS 문제 해결**

### 7. 한계 및 미해결 영역

**논문이 명시하지 않은 것:**

1. **HA 해결 메커니즘:** 논문 Section 6에서 HA를 어떻게 해결하는지 명시적 설명 없음

2. **정량적 성능 평가:** 실무 적용 현황은 언급되나, MARISMA의 정량적 성능 비교 (예: 위험 탐지율, 오탐율, 적용 시간 등) 없음

3. **비용 분석:** "Low Cost"를 해결한다고 주장하나, 실제 도입 비용, 운영 비용에 대한 구체적 수치 없음

4. **비교 평가:** MARISMA를 Table 3의 12가지 기준으로 평가한 결과 미제시

5. **한계 인정:** 논문이 MARISMA의 한계를 명시적으로 논의하지 않음

### 8. Future Work

**논문의 명시적 언급:**
> "As future work, we intend to continue evolving the framework in order to further optimise the solutions to each of the shortcomings identified. This will be done by employing the knowledge base that is being obtained using current implementations, which will be achieved through the use of artificial intelligence techniques."

**향후 계획:**
- 프레임워크 지속 진화
- 식별된 각 약점에 대한 솔루션 최적화
- 현재 구현에서 얻어지는 지식 베이스 활용
- **인공지능 기법 사용**

---

**Day 4 마무리:**  
MARISMA 프레임워크는 체계적 문헌 고찰에서 식별된 10가지 약점에 대한 통합 솔루션이다. 4대 구성 요소(Meta-Pattern, 3 Processes, Knowledge Base, eMARISMA Tool)는 각각 특정 약점을 타겟한다. 특히 3개 프로세스 간 정보 교환을 통한 5단계 동적 학습 순환은 DY 문제의 핵심 해결책이며, Pattern Legacy를 통한 기업 간 지식 공유는 CC 문제를 해결한다. Control을 CAT 구조로 통합한 것은 기존 방법론과의 근본적 차별점이다. 4개국 수십 개 기업에 실제 적용되어 지속적으로 개선되고 있다는 점에서 PC(실무 사례) 문제도 해결했다. 그러나 HA 해결 메커니즘은 명시적으로 설명되지 않았으며, 정량적 성능 평가와 한계 논의는 부재하다. 향후 AI 기법을 활용한 추가 최적화가 계획되어 있다.