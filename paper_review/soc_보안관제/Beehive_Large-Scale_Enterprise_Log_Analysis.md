# Research Review: Beehive: Large-Scale Log Analysis for Detecting Suspicious Activity in Enterprise Networks
> **Analyzed Date:** 2024.12.30  
> **Keywords:** SOC, Log Analysis, Enterprise Security, Anomaly Detection, Clustering  
> **Source:** ACSAC '13, 2013, pp.199-208 [Link](https://doi.org/10.1145/2523649.2523670)

---

## Why This Paper?

### 선정 배경
**도메인 탐색 결과:**  
8주간 보안 컨설팅, OT/ICS, 클라우드 등 8개 도메인 논문을 읽은 결과, **SOC(Security Operations Center)** 가 나의 강점과 흥미에 가장 부합함을 확인. 이제부터는 SOC 전문성 심화를 위한 체계적 학습 단계.

**이 논문을 선택한 이유:**  
- **단일 시스템에서 네트워크 전체로 시야 확장**: Lou et al. (2010)과 DeepLog은 단일 시스템의 로그 분석에 집중했다면, Beehive는 대규모 엔터프라이즈 네트워크 환경에서의 로그 분석을 다룸
- **실무 SOC 환경과 직결**: 실제 EMC의 대규모 환경(일일 14억 건의 로그, 1TB/day)에서 검증된 시스템
- **이질적 로그 소스 통합 분석**: Web proxy, DHCP, VPN, 도메인 컨트롤러, 안티바이러스 등 다양한 소스를 통합하는 실무 문제 해결
- **행위 기반 탐지**: 시그니처 기반이 아닌 비정상 행위 패턴 탐지로 미지의 위협(APT, 제로데이) 식별 가능

**학습 목표:**  
1. 대규모 이질적 로그 데이터의 정규화 및 전처리 기법 습득
2. 엔터프라이즈 특화 피처 설계 방법론 이해
3. 비지도 학습(클러스터링) 기반 이상탐지 접근법과 SOC 실무 적용 전략 파악

---

## Day 1 – Research Context & Motivation
*(대규모 더러운 로그에서 실제 위협 찾아내기)*

### 1. 연구 배경: 엔터프라이즈 네트워크의 보안 가시성 문제

**엔터프라이즈 환경의 복잡성 증가**
- 전통적 경계 방어 무너짐: BYOD, 계약자, 지리적 분산
- 기존 안티바이러스 무력화: 일반 멀웨어 + APT 공격 고도화
- 다양한 보안 제품 난립: 벤더별로 상이한 로그 포맷, 불완전하고 모순된 데이터

**로그 데이터의 잠재력과 한계**
- 잠재력: 공격 발생 시 최초로 참고하는 데이터 소스 (인증 로그로 계정 탈취 감지, 웹 프록시 로그로 Drive-by Download 추적)
- 한계: 로그가 "dirty"함 - 포맷 비일관성, 누락/모순, 대용량(TB/day), 타임존 불일치

**현재 로그 분석의 문제점**
- 수동 분석 중심: 보안 전문가가 수작업으로 의심 활동 조사
- 시그니처 의존: 알려진 위협만 탐지, 신규/변종 위협 놓침
- 확장성 부족: 대규모 데이터 처리 불가

**연구 문제의식**
엔터프라이즈의 더러운 로그 데이터에서 자동으로 지식을 추출하고, 시그니처가 아닌 행위 기반으로 의심스러운 호스트 활동을 탐지할 수 있는가?

### 2. 핵심 개념

| 개념 | 정의 | SOC 맥락에서의 의미 |
|------|------|---------------------|
| **Dirty Logs** | 포맷 불일치, 누락, 모순, 대용량의 로그 데이터 | 실무 SOC가 직면하는 현실적 데이터 품질 문제 |
| **Behavioral Detection** | 시그니처가 아닌 호스트 행위 패턴 기반 탐지 | 미지의 위협(APT, 제로데이) 식별 가능 |
| **Security Incidents** | 정책 위반 또는 공격 가능성이 있는 의심 활동 | SOC 분석가가 추가 조사할 대상 |
| **Dedicated Hosts** | 단일 사용자가 주로 사용하는 호스트 | 행위 프로파일링의 기준선 설정 가능 |
| **Enterprise-Specific Features** | 엔터프라이즈 환경의 제약(정책, 일반 직원 행위)을 활용한 피처 | 일반 인터넷과 달리 예측 가능한 행위 패턴 활용 |

### 3. 이론적 기반: Beehive 시스템 3계층 구조

```
[Layer 1: Data Normalization]
- 타임스탬프 정규화 (UTC 통일)
- IP-to-Host 매핑 (DHCP 바인딩)
- 정적 IP 자동 탐지
         ↓
[Layer 2: Feature Generation]
- Destination-based (4개)
- Host-based (1개)
- Policy-based (6개)
- Traffic-based (4개)
→ 총 15개 피처/호스트/일
         ↓
[Layer 3: Detection via Clustering]
- PCA로 차원 축소
- 변형 K-means 클러스터링
- Outlier 식별 → Incident 보고
```

### 4. 연구의 핵심 기여

**학술적 기여**
- 대규모 실제 엔터프라이즈 로그 데이터의 "Big Data" 보안 분석 최초 연구
- 이질적 로그 통합을 위한 체계적 전처리 방법론 제시
- 엔터프라이즈 특화 행위 피처 설계 프레임워크

**SOC 실무 기여**
- 일일 1.4억 건(1TB) 로그 → 8천만 건으로 74% 감축하면서도 탐지 정확도 유지
- 2주간 평가에서 784건 인시던트 탐지, 이 중 25.25%가 멀웨어 또는 추가 조사 필요
- 기존 보안 도구가 놓친 위협 식별: 784건 중 단 8건만 기존 도구가 탐지

### 5. SOC 관점 인사이트

**실무 적용 가능성**
- SIEM 데이터를 활용한 자동화된 이상탐지 파이프라인 구축 가능
- 시그니처 업데이트 없이도 신규 위협 탐지 (DGA 기반 멀웨어 등)
- 정책 위반(스트리밍, 파일 공유, 성인 콘텐츠 등) 자동 식별로 컴플라이언스 강화

**기존 학습과의 연결**
- Lou et al. (2010): 단일 시스템 불변성 → Beehive: 네트워크 전체 행위 패턴
- DeepLog: 딥러닝 블랙박스 → Beehive: 설명 가능한 피처 기반 클러스터링
- 두 접근법 모두 필요: DeepLog는 정확도, Beehive는 대규모 확장성 + 설명력

**현실적 고려사항**
- Ground Truth 부재 문제: 실제 엔터프라이즈는 이미 방어 중이므로 알려진 위협 흔적이 적음 → 수동 레이블링 불가피
- 오탐 관리: 784건 중 35.33%가 비악성 자동화 프로세스 → 추가 필터링 필요

---

## Day 2 – Research Model, Hypotheses, and Methodology
*(Beehive의 설계: 더러운 데이터를 깨끗한 인텔리전스로)*

### 1. 연구 모델 개요

Beehive는 가설 검증 방식이 아닌 **엔지니어링 시스템 설계 연구**로, 대규모 로그 분석 문제를 해결하기 위한 3계층 파이프라인을 제안한다.

```
[입력: Raw Logs from Multiple Sources]
        ↓
[Layer 1: Data Normalization & Preprocessing]
  - Timestamp Normalization
  - IP-to-Host Mapping (Dynamic + Static)
  - Dedicated Host Identification
        ↓
[Layer 2: Feature Extraction]
  - 15 enterprise-specific features per host/day
        ↓
[Layer 3: Unsupervised Detection]
  - PCA (dimensionality reduction)
  - Modified K-means clustering
  - Outlier identification
        ↓
[출력: Security Incidents for SOC Investigation]
```

**설계 철학**
- 시그니처 불필요: 알려지지 않은 위협도 행위 패턴으로 탐지
- 확장성 우선: 일일 TB급 데이터 처리 가능한 효율적 알고리즘
- 실무 중심: SOC 분석가가 즉시 조사 가능한 actionable intelligence 제공

### 2. 연구 가설

이 논문은 전통적인 가설 검증 연구가 아니므로 명시적 가설이 없으나, **암묵적 가정(Assumptions)**을 다음과 같이 정리할 수 있다:

| 가정 | 내용 | 근거 |
|------|------|------|
| **A1: Enterprise Behavior Constraint** | 엔터프라이즈 환경의 호스트 행위는 정책과 직원 업무 패턴으로 인해 일반 인터넷보다 훨씬 제약적이다 | 대부분 직원이 유사한 직무 수행 → 정상 행위 클러스터 형성 가능 |
| **A2: Outliers Indicate Threats** | 정상 행위에서 크게 벗어난 outlier는 멀웨어 감염 또는 정책 위반일 가능성이 높다 | 비지도 학습으로 사전 레이블 없이도 의심 활동 식별 가능 |
| **A3: Log Correlation Feasibility** | 타임스탬프 정규화와 IP-Host 매핑을 통해 이질적 로그를 호스트 단위로 통합 가능하다 | SIEM 수신 시각과 DHCP 로그를 활용한 시간적 상관관계 분석 |
| **A4: Feature Sufficiency** | 15개 피처(destination/host/policy/traffic-based)가 호스트의 보안 관련 행위를 충분히 표현한다 | EMC 내부 멀웨어 사례 및 정책 위반 패턴 관찰 기반 설계 |

### 3. 연구 방법론

#### A. 데이터 수집 (Data Collection)

**로그 소스**
| 로그 타입 | 수집 정보 | 용도 |
|-----------|----------|------|
| **Web Proxy** | 모든 외부 연결 (IP, 도메인, URL, HTTP 헤더, User-Agent, 평판 점수) | 외부 통신 행위 분석의 핵심 |
| **DHCP** | IP 할당/해제 이력 | IP-to-Host 매핑 |
| **VPN** | 원격 접속 로그 | 비정상 위치 접근 탐지 |
| **Windows Domain Controllers** | 인증 시도 로그 | Dedicated Host 식별, 계정 탈취 의심 |
| **Antivirus** | 멀웨어 스캔 결과 | 기존 도구와 비교 검증 |

**데이터 규모 (EMC 기준)**
- 일일 평균 14억 건의 로그 메시지
- 일일 약 1TB의 로그 데이터
- 웹 프록시 로그: 일일 3억 건 (600GB)

**로그의 특성 및 문제점**
- 비표준 타임스탬프: 장비별로 로컬 시간, UTC 등 혼재
- 식별자 불일치: IP 주소, 호스트명, 사용자명 혼용
- 데이터 누락/순서 뒤바뀜: 네트워크 지연, 버퍼링
- 웹 프록시 경고 페이지: 알려지지 않은 사이트 접속 시 사용자가 정책 동의해야 접근 가능 (Challenged → Consented)

#### B. 데이터 정규화 (Data Normalization)

**B1. 타임스탬프 정규화**

문제: 글로벌 엔터프라이즈에서 장비들이 다른 타임존 사용
```
해결책:
1. SIEM이 로그 수신 시각 t_siem 기록 (UTC)
2. 각 장비별로 Δ_i = t_siem,i - t_device,i 계산 (30분 단위로 반올림)
3. 다수를 차지하는 Δ_correction 값 식별
4. 정규화: t_normalized,i = t_device,i + Δ_correction
```
효과: 모든 로그를 UTC 기준으로 통일하여 시간적 상관관계 분석 가능

**B2. IP-to-Host 매핑 (DHCP 기반)**

문제: DHCP로 동적 IP 할당 → 같은 IP가 시간에 따라 다른 호스트에 할당됨

해결책:
```
1. DHCP 서버 로그 분석
2. 바인딩 DB 구축: {IP, hostname, MAC, start_time, end_time}
3. 로그의 (IP, timestamp) → hostname 매핑
4. 매일 업데이트하여 최신 바인딩 유지
```

**B3. 정적 IP 자동 탐지**

문제: 정적 IP 목록이 없거나 오래됨

Bootstrap 알고리즘:
```
1. A = 모든 로그에서 발견된 IP 집합
2. D = DHCP/VPN 로그의 동적 IP 집합
3. S = A - D (잠재적 정적 IP)
4. S의 각 IP에 대해 역방향 DNS 조회 → hostname 저장
```

정제 알고리즘 (매일 실행):
```
1. 새로운 로그로 A, D 업데이트
2. S = A - D 재계산
3. S의 각 IP 역방향 DNS 조회
4. 이전 hostname과 비교:
   - 변경됨 → S에서 제거 (동적 IP였음)
   - 동일함 → S에 유지 (정적 IP 확률 높음)
```

**B4. Dedicated Host 식별**

목적: 단일 사용자가 주로 사용하는 호스트만 분석 (공용 호스트 제외)

방법:
```
1. Windows 도메인 컨트롤러의 인증 로그 3개월간 수집
2. 각 호스트별로 사용자별 인증 빈도 계산
3. 단일 사용자 인증이 95% 이상 → Dedicated Host로 분류
```

결과: EMC에서 78,000대 이상의 Dedicated Host 식별

#### C. 피처 추출 (Feature Extraction)

**피처 설계 원칙**
- EMC 내부의 알려진 멀웨어 행위 및 정책 위반 패턴 관찰 기반
- 엔터프라이즈 환경 특성 활용: 엄격한 방화벽, 업무 중심 활동, 동질적 소프트웨어 구성
- 호스트별 일일 15개 피처 벡터 생성

**15개 피처 상세**

**C1. Destination-Based Features (4개)**

핵심 아이디어: 새롭거나 드문 외부 목적지 접속은 의심스러움 (C&C 서버, 손상된 사이트)

| 피처 | 설명 | 계산 방법 |
|------|------|-----------|
| **F1: New Destinations** | 처음 접속하는 외부 목적지 수 | 1개월 히스토리에 없는 도메인 수 |
| **F2: New Dests w/o Whitelisted Referer** | Whitelisted Referer 없이 접속한 새 목적지 수 | F1 중 HTTP Referer가 화이트리스트에 없는 경우 |
| **F3: Unpopular Raw IP Dests** | Unpopular한 IP 주소 목적지 수 | 화이트리스트 외 IP 주소 접속 수 |
| **F4: Fraction of Unpopular Raw IP** | 전체 unpopular 목적지 중 IP 주소 비율 | F3 / (total unpopular destinations) |

화이트리스트 구축:
- 1주일 학습 기간 동안 100대 이상 호스트가 접속한 도메인/서브넷
- 결과: 일일 3억 건 로그 → 8천만 건으로 74% 감축

도메인 "Folding":
- 2nd-level 도메인으로 통합 (random subdomain 필터링)
- favicon 요청 무시
- Raw IP는 해석하지 않고 항상 "new"로 간주
- 최적화 후: 일일 처리 시간 15시간 → 5시간, 히스토리 크기 4.3M → 2.7M (4개월)

**C2. Host-Based Feature (1개)**

| 피처 | 설명 | 계산 방법 |
|------|------|-----------|
| **F5: New User-Agent Strings** | 새로운 User-Agent 문자열 수 | 호스트별 UA 히스토리(1개월)에서 Edit Distance로 비교 |

근거: 엔터프라이즈는 소프트웨어 구성이 동질적 → 새 UA는 무단 소프트웨어 설치 의심

**C3. Policy-Based Features (6개)**

웹 프록시 정책 단계:
1. **Blocked**: 낮은 평판 또는 금지 카테고리 → 자동 차단
2. **Challenged**: 미분류 사이트 → 경고 페이지 표시
3. **Consented**: 사용자가 정책 동의 클릭 후 접속

| 피처 | 설명 |
|------|------|
| **F6: Blocked Domains** | 차단된 도메인 수 |
| **F7: Blocked Connections** | 차단된 연결 수 |
| **F8: Challenged Domains** | 경고 받은 도메인 수 |
| **F9: Challenged Connections** | 경고 받은 연결 수 |
| **F10: Consented Domains** | 동의 후 접속한 도메인 수 |
| **F11: Consented Connections** | 동의 후 접속한 연결 수 |

**C4. Traffic-Based Features (4개)**

정의:
- **Spike**: 1분 동안 비정상적으로 높은 트래픽 발생
- **Burst**: 연속된 spike 구간

임계값 설정 (1주일 전체 Dedicated Host 분석):
```
Connection Spike 임계값: 101 connections/min (90% 백분위수)
Domain Spike 임계값: 17 domains/min (90% 백분위수)
Burst 내부 Spike 임계값 (완화): 26 connections/min, 6 domains/min (75% 백분위수)
```

| 피처 | 설명 |
|------|------|
| **F12: Connection Spikes** | Connection spike 발생 횟수 |
| **F13: Domain Spikes** | Domain spike 발생 횟수 |
| **F14: Connection Bursts** | 가장 긴 connection burst 지속 시간 |
| **F15: Domain Bursts** | 가장 긴 domain burst 지속 시간 |

#### D. 탐지 알고리즘 (Detection via Clustering)

**D1. PCA (Principal Component Analysis)**

목적: 피처 간 의존성 제거 및 차원 축소
- 예: Domain spike 발생 시 connection spike도 발생 (상관관계)

방법:
```
1. 각 호스트를 15차원 벡터 v = (v[1], ..., v[15])로 표현
2. PCA로 주성분 추출
3. 데이터 분산의 95% 이상 보존하는 상위 m개 주성분 선택
4. 원본 벡터를 m차원으로 투영
```

**D2. Modified K-means Clustering**

기존 K-means 문제: 클러스터 수 k를 사전 지정 필요

Beehive의 변형 알고리즘:
```
1. 무작위로 벡터 하나를 첫 클러스터 허브로 선택
   모든 벡터를 이 클러스터에 할당

2. 자신의 허브에서 가장 먼 벡터를 새 허브로 선택
   모든 벡터를 가장 가까운 허브에 재할당

3. 반복 종료 조건:
   모든 벡터가 자신의 허브로부터의 거리 < (평균 허브 간 거리)/2

4. 거리 측정: L1 distance (Manhattan distance)
   L1Dist(v1, v2) = Σ|v1[i] - v2[i]|
```

결과:
- 1회 반복 후: 대다수 호스트 → 하나의 큰 정상 클러스터
- 나머지: 소수의 outlier 클러스터 (의심 활동)

**Extreme Outlier 처리**:
```
IF 클러스터가 2개만 생성됨 (하나는 단일 노드, 나머지는 전부):
  가장 큰 클러스터에 PCA + 클러스터링 재적용
  최소 50개 outlier 호스트 식별될 때까지 반복
```

**인시던트 생성**:
- 클러스터는 outlier 정도에 따라 자연스럽게 순서화됨 (가장 먼 노드부터 식별)
- 상위 outlier 호스트들을 인시던트로 보고
- SOC 분석가에게 전달

### 4. SOC 관점 인사이트

**방법론의 실무 적용성**

장점:
1. **확장성**: 일일 TB급 데이터를 5시간 내 처리 (타임스탬프 정규화 + 화이트리스팅 최적화)
2. **설명 가능성**: 15개 명확한 피처 → SOC 분석가가 왜 의심스러운지 즉시 이해 가능 (vs. DeepLog 블랙박스)
3. **레이블 불필요**: 비지도 학습으로 사전 학습 데이터 없이도 적용 가능
4. **엔터프라이즈 특화**: 일반 인터넷 환경에서는 작동 안 함 → 기업 정책/행위 제약 활용

한계:
1. **Ground Truth 부재**: 실제 평가는 수동 검증 의존 (다음 Day 3에서 다룰 예정)
2. **초기 학습 기간**: 히스토리 구축에 1개월, 화이트리스트에 1주일 필요
3. **정적 환경 가정**: 조직 구조/정책 급변 시 재학습 필요

**기존 SOC 툴과의 차별점**

| 도구 | 탐지 방식 | 강점 | 약점 |
|------|-----------|------|------|
| **SIEM (기존)** | 시그니처 + 룰 기반 | 알려진 위협 정확히 탐지 | 신규/변종 놓침 |
| **Antivirus** | 시그니처 기반 | 알려진 멀웨어 차단 | 제로데이 무력 |
| **Beehive** | 행위 기반 클러스터링 | 미지의 위협 탐지, 정책 위반 식별 | 오탐 가능성 (수동 검증 필요) |

**SOC Workflow 통합 전략**
```
[Tier 1: Automated Detection]
SIEM Alerts + AV Alerts + Beehive Daily Incidents
            ↓
[Tier 2: Triage & Investigation]
- Beehive 클러스터 컨텍스트 확인 (평균 피처, 호스트 수)
- 원본 로그 조회 (UA, HTTP status, referer, 타이밍)
- 외부 평판 체크 (McAfee SiteAdvisor, URLVoid, DomainTools)
            ↓
[Tier 3: Incident Response]
- 악성 확인 → 격리/치료
- 정책 위반 → HR 통보
- 의심 활동 → 상위 SOC로 에스컬레이션
```

**다음 학습 방향 (Day 3 Preview)**
- Beehive가 실제 EMC 환경에서 2주간 생성한 784건의 인시던트 분석 결과
- 멀웨어, 정책 위반, 오탐 분류 비율
- 기존 보안 도구와의 비교 검증