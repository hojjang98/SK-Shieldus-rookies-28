# 주간 보안 이슈 분석

SK쉴더스 본사 방문 이후 시작한 보안 시사 학습 프로젝트입니다.  
매주 2~3개의 최신 보안 사고를 선정하여 심층 분석하고, 근본 원인과 실무적 예방 방법을 학습합니다.

## 프로젝트 목적

- **최신 보안 트렌드 파악**: 실시간으로 발생하는 글로벌 보안 사고 추적
- **근본 원인 분석**: 기술적/관리적/인적 측면의 다각도 분석
- **실무 대응 능력 향상**: 예방 및 대응 방안 수립 훈련
- **지속적인 학습**: 주간 루틴으로 보안 감각 유지

## Repository 구조

```
security_issues_analysis/
├── README.md
├── 2025/
│   ├── week51/
│   │   ├── coupang_data_breach.md
│   │   ├── deepfake_interview.md
│   │   └── edge_vulnearabilities.md
│   └── week52/
│       ├── azure_blob_storage_phishing.md
│       ├── skt_usim_breach_analysis.md
│       └── trust_wallet_supply_chain_attack.md
└── 2026/
    ├── week01/
    │   ├── chrome_extension_malware.md
    │   ├── korean_air_breach.md
    │   └── marquis_ransomeware_breach.md
    ├── week02/
    │   ├── ledger_globale_braech.md
    │   ├── esa_data_breach.md
    │   └── blackcat_insider_threat.md
    └── week03/
        ├── ESA_external_server_breach.md
        ├── manage_my_health_randsomware.md
        └── trust_wallet_supply_chain_attack.md
```

## 분석 템플릿

각 보안 사고는 다음 구조로 분석합니다:

### 1. 기사 정보
- 출처, 작성일, 링크, 카테고리

### 2. 핵심 요약
- 2-3줄로 사건의 본질 요약

### 3. 사건/이슈 배경
- **무슨 일이 일어났는가?**: 사건 전개 과정
- **누가 관련되었는가?**: 공격자, 피해자, 관련 당사자

### 4. 원인 분석
- **기술적 원인**: 취약점, 보안 구조적 결함
- **관리적/절차적 원인**: 정책, 프로세스 부재
- **인적 원인**: 보안 인식, 실수, 내부자 위협

### 5. 영향 및 파급효과
- **직접적 영향**: 즉각적 피해 규모
- **간접적 영향**: 신뢰도, 산업 전반 파급
- **예상 피해 규모**: 정량적/정성적 평가

### 6. 예방 및 대응 방안
- **사전 예방 방법**: 기술적/관리적 통제
- **사고 발생 시 대응 방안**: 초기 대응 절차
- **재발 방지 대책**: 근본적 개선 방향

### 7. 개인 인사이트
- **배운 점**: 기술적/전략적 학습 내용
- **느낀 점**: 주관적 의견 및 시사점

## 주간 분석 현황

| 주차 | 분석 기사 수 | 주요 키워드 | 비고 |
|------|-------------|------------|------|
| 2025-51주 | 3건 | 데이터침해, 딥페이크, 브라우저취약점 | 프로젝트 시작 |
| 2025-52주 | 3건 | 피싱, USIM해킹, 공급망공격 | Trust Wallet 분석 |
| 2026-01주 | 3건 | 익스텐션악성코드, 항공사침해, 랜섬웨어 | |
| 2026-02주 | 3건 | 하드웨어지갑, 우주기관침해, 내부자위협 | ESA 침해 분석 |
| 2026-03주 | 3건 | 공급망공격, 의료데이터침해, 외부서버보안 | Manage My Health |

**총 분석 건수**: 15건  
**분석 시작일**: 2025년 12월

## 주요 학습 주제

### 공급망 공격 (Supply Chain Attack)
- Trust Wallet 크롬 익스텐션 공급망 공격 (2025-52주, 2026-03주)
- Shai-Hulud npm 패키지 공격 연관성

### 의료 보안 (Healthcare Security)
- Manage My Health 랜섬웨어 공격 (2026-03주)
- 기본 보안 위생(MFA, 패치관리) 부재 사례

### 외부 시스템 보안
- ESA 외부 서버 침해 (2026-02주, 2026-03주)
- 협업 시스템의 보안 중요성

### 인증 및 접근 제어
- 다단계 인증(MFA) 부재로 인한 피해 사례 다수
- API 키 및 자격 증명 관리 실패

### 공휴일 시즌 공격
- 크리스마스/연말 시즌의 전략적 공격 타이밍
- 보안 인력 축소 기간을 노린 공격

## 주요 참고 소스

### 국내 보안 미디어
- [보안뉴스](https://www.boannews.com/)
- [데일리시큐](https://www.dailysecu.com/)
- [KISA 인터넷 보호나라](https://www.krcert.or.kr/)
- [KISA 보안공지](https://www.krcert.or.kr/data/secNoticeList.do)

### 해외 보안 미디어
- [The Hacker News](https://thehackernews.com/)
- [BleepingComputer](https://www.bleepingcomputer.com/)
- [SecurityWeek](https://www.securityweek.com/)
- [Krebs on Security](https://krebsonsecurity.com/)
- [Dark Reading](https://www.darkreading.com/)

### 위협 인텔리전스
- [CISA Cyber Incidents](https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents)
- [Check Point Research](https://research.checkpoint.com/)
- [Recorded Future](https://www.recordedfuture.com/)