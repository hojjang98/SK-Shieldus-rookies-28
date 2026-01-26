# Week 13: 보안 컨설팅 프로젝트 - 취약점 진단

## Week 2/4: 취약점 진단 단계

Week 12에서 구축한 취약한 E-Commerce 시스템을 대상으로 실제 보안 컨설턴트처럼 취약점 진단을 수행한다.

---

## 진단 목표

1. 자동화 도구를 활용한 전체 취약점 스캔
2. 수동 점검을 통한 심화 취약점 발굴
3. 실제 공격 시연 (PoC)
4. 종합 취약점 진단 보고서 작성

---

## 진단 범위

### 대상 시스템
- Week 12에서 구축한 E-Commerce 웹 애플리케이션
- URL: http://localhost:5000

### 점검 항목
1. **SQL Injection**
   - 로그인 페이지
   - 상품 검색 기능
   
2. **XSS (Cross-Site Scripting)**
   - 상품 후기 (댓글)
   - 프로필 정보
   
3. **인증/세션 관리**
   - 세션 토큰 예측 가능성
   - 인증 우회 가능성
   
4. **파일 업로드**
   - 프로필 이미지 업로드
   - 파일 타입 검증 우회

---

## 사용 도구

- **OWASP ZAP**: 자동화 취약점 스캐너
- **Python Scripts**: 수동 점검용 테스트 스크립트
- **Burp Suite**: HTTP 요청/응답 분석 (선택)
- **SQLMap**: SQL Injection 자동화 도구 (선택)

---

## 폴더 구조
```
security_assessment/
├── reports/                       # 진단 보고서
│   ├── vulnerability_report.md    # 종합 보고서
│   └── screenshots/               # 공격 성공 증거
├── tools/                         # 테스트 스크립트
│   ├── sql_injection_test.py
│   ├── xss_test.py
│   └── file_upload_test.py
├── scan_results/                  # 스캔 결과물
│   └── zap_scan_result.html
└── README.md
```

---

## 진단 프로세스

### 1단계: 자동화 스캔
- OWASP ZAP을 사용한 전체 애플리케이션 스캔
- 발견된 취약점 목록 확보

### 2단계: 수동 점검
- SQL Injection 테스트 스크립트 작성 및 실행
- XSS 공격 시연
- 파일 업로드 취약점 검증

### 3단계: 보고서 작성
- 취약점별 심각도 분류 (Critical/High/Medium/Low)
- 공격 시연 스크린샷 첨부
- 비즈니스 영향도 분석
- 개선 권고안 제시

---

## 진단 완료 내역

### 자동화 스캔
- OWASP ZAP baseline 스캔 완료
- 결과: `scan_results/zap_scan_result.html`
- 발견 취약점: Medium 3개, Low 5개, Info 6개

### 수동 진단
1. SQL Injection 로그인 우회 테스트 완료
2. SQL Injection 검색 필터 우회 테스트 완료
3. XSS 공격 시연 완료
4. 파일 업로드 취약점 검증 완료

### 산출물
- 종합 취약점 진단 보고서: `reports/vulnerability_report.md`
- 공격 시연 스크린샷: `reports/screenshots/` (6장)
- 테스트 스크립트:
  - `tools/sql_injection_test.py`
  - `tools/sql_data_extraction.py`

### 발견 취약점 요약
- Critical: 2개 (SQL Injection)
- High: 2개 (XSS, 파일 업로드)
- Medium: 3개 (CSRF, CSP, Clickjacking)
- Low: 5개 (보안 헤더 누락)

---

## 다음 주 계획

Week 14에서는 발견된 취약점을 실제로 수정하고 보안을 강화합니다.

## 다음 주 계획

Week 14에서는 이번 주에 발견한 취약점들을 실제로 수정하고 보안을 강화한다.