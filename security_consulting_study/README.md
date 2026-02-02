# Security Consulting Study

> SK쉴더스 루키즈 28기 출신 보안 컨설턴트 지망생의 체계적인 보안 학습 여정

## About This Repository

이 레포지토리는 보안 컨설팅 실무에 필요한 핵심 지식을 체계적으로 정리하는 공간입니다.
매일 조금씩, 꾸준히 학습하며 이론과 실무를 연결하는 것을 목표로 합니다.

---

## 학습 목표

- [ ] ISMS-P 인증기준 104개 통제항목 완전 이해
- [ ] OWASP Top 10 취약점 분석 및 대응 방안 마스터
- [ ] 정보보안 관련 법령(개인정보보호법, 정보통신망법) 실무 적용 능력
- [ ] 실제 컨설팅 프로젝트 수행 능력 함양
- [ ] 보안 사고 사례 분석 및 개선 제안 역량

---

## 학습 로드맵

### Phase 1: Foundation (Week 1-2)
**목표:** 전체 프레임워크 이해 및 기초 다지기

- **ISMS-P 인증기준 개요**
  - 관리체계 수립 및 운영 (12개 통제항목)
  - 보호대책 요구사항 (64개 통제항목)
  - 개인정보 처리단계별 요구사항 (28개 통제항목)

- **OWASP Top 10 (2021)**
  - A01: Broken Access Control
  - A02: Cryptographic Failures
  - A03: Injection
  - A04: Insecure Design
  - A05: Security Misconfiguration
  - A06: Vulnerable and Outdated Components
  - A07: Identification and Authentication Failures
  - A08: Software and Data Integrity Failures
  - A09: Security Logging and Monitoring Failures
  - A10: Server-Side Request Forgery (SSRF)

### Phase 2: Legal Framework (Week 3-4)
**목표:** 법령 이해 및 ISMS-P 연계

- **개인정보보호법**
  - 개인정보 생명주기별 의무사항
  - 안전조치 의무
  - 침해사고 대응 및 신고
  - 주요 과징금 사례

- **정보통신망법**
  - 개보법과의 차이점
  - 암호화 의무
  - 정보통신서비스 제공자 의무

- **법령-ISMS-P 매핑**
  - 통제항목별 법적 근거
  - Compliance 체크리스트

### Phase 3: Practical Application (Week 5-6)
**목표:** 실전 프로젝트 및 사례 분석

- **가상 컨설팅 프로젝트**
  - 회사 시나리오 설정
  - 현황 진단 (Gap Analysis)
  - 위험 평가 (Risk Assessment)
  - 개선 계획 수립
  - 컨설팅 보고서 작성

- **실제 보안 사고 사례 분석**
  - 사고 원인 분석 (기술적/관리적)
  - ISMS-P 관점 미흡 사항 도출
  - 예방 대책 제시
  - 컨설팅 제안서 작성

### Phase 4: Advanced Topics (Ongoing)
**목표:** 심화 학습 및 최신 트렌드

- 클라우드 보안 (AWS, Azure, GCP)
- 제로트러스트 아키텍처
- DevSecOps
- AI/ML 보안
- 공급망 보안

---

## Repository Structure
```
security-consulting-study/
├── README.md                          # 이 파일
├── 01-ISMS-P/                         # ISMS-P 인증기준
│   ├── README.md
│   ├── 01-관리체계-수립-운영/
│   ├── 02-보호대책-요구사항/
│   ├── 03-개인정보-처리단계별-요구사항/
│   ├── 법령-매핑.md
│   └── 실습-프로젝트/
├── 02-OWASP-Top10/                    # OWASP Top 10 취약점
│   ├── README.md
│   ├── A01-Broken-Access-Control.md
│   ├── A02-Cryptographic-Failures.md
│   ├── ...
│   └── 실습-시나리오/
├── 03-Laws/                           # 정보보안 법령
│   ├── README.md
│   ├── 개인정보보호법.md
│   ├── 정보통신망법.md
│   ├── 법령-비교표.md
│   └── 주요-판례-사례/
├── 04-Case-Studies/                   # 실제 사례 분석
│   ├── README.md
│   └── [회사명]-사고-분석.md
├── 05-Practical-Projects/             # 실습 프로젝트
│   ├── README.md
│   └── [프로젝트명]/
└── 06-Resources/                      # 참고 자료
    ├── 추천-도서.md
    ├── 유용한-링크.md
    └── 용어-정리.md
```
---

## 학습 원칙

1. **매일 조금씩** - 하루 1-2시간, 꾸준히
2. **이해 우선** - 암기보다 개념 이해와 실무 연결
3. **문서화 습관** - 배운 내용은 반드시 문서로 정리
4. **실습 병행** - 이론만이 아닌 실제 적용 경험
5. **컨설팅 관점** - 항상 "고객사에 어떻게 설명할까?" 고민

---

## 주요 참고 자료

### 공식 문서
- [ISMS-P 인증기준 (한국인터넷진흥원)](https://isms.kisa.or.kr)
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [개인정보보호위원회](https://www.pipc.go.kr)
- [법제처 국가법령정보센터](https://www.law.go.kr)

### 가이드라인
- KISA 정보보호 및 개인정보보호 관리체계 인증 안내서
- KISA 개인정보의 기술적·관리적 보호조치 기준 해설서
- 개인정보보호위원회 각종 가이드라인

### 커뮤니티
- [보안프로젝트](https://www.boannews.com)
- [KISA 보안공지](https://www.boho.or.kr)


---

## License

이 레포지토리의 모든 내용은 학습 목적으로 작성되었으며, 출처가 명시된 자료는 해당 저작권자에게 권리가 있습니다.