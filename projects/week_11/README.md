# ISO 27001 보안 컨설팅 보고서 프로젝트

## [프로젝트 개요]

**클라이언트**: DNA Lab (유전자 검사 헬스케어 스타트업)  
**컨설팅사**: SK Shields 보안 컨설팅팀  
**목표**: ISO 27001 인증 취득을 위한 보안 취약점 분석 및 개선 로드맵 제시

## [시나리오]

DNA Lab은 유전자 검사 서비스를 제공하는 헬스케어 스타트업으로, 고객의 민감한 개인정보와 의료정보를 다루고 있습니다. 최근 Series B 투자를 유치하고 대형 병원/보험사와의 B2B 계약을 추진 중이나, 계약 조건으로 **ISO 27001 인증**을 요구받았습니다.

내부 보안팀의 자체 스캐닝 결과 심각한 취약점들이 발견되어, 6개월 내 ISO 27001 인증 취득을 목표로 외부 보안 컨설팅을 의뢰하였습니다.

## [주요 발견사항]

### 취약점 통계
- **총 취약점**: 27개
- **총 발견사항**: 102개
- **Critical**: 4개
- **High**: 12개
- **Medium**: 10개
- **Low**: 1개
- **평균 CVSS 스코어**: 7.10 / 10.0

### 심각도별 분포
```
Critical (4개):
- WEB-002: SQL Injection (CVSS 9.8, 28개 발견사항)
- WEB-003: OS Command Injection (CVSS 9.8, 4개 발견사항)
- WEB-009: 쿠키 변조 (CVSS 9.1, 3개 발견사항)
- WEB-010: 파일 전송 취약점 (CVSS 9.8, 2개 발견사항)

High (12개):
- XSS, CSRF, IDOR, SSRF 등
- OS 보안 설정 미흡 (비밀번호 정책, 계정 잠금 등)
- 불필요한 서비스 활성화 (NFS, FTP 등)
```

## [ISO 27001:2022 준수성 평가]

### Gap Analysis 결과
- **평가된 통제항목**: 14개
- **Compliant**: 0개
- **Partially Compliant**: 10개
- **Non-Compliant**: 2개
- **Critical Gap**: 2개

### 주요 미충족 통제항목
1. **A.8.3 (정보 접근 제한)**: 9개 취약점 - Critical Gap
2. **A.8.16 (모니터링 활동)**: 7개 취약점 - Critical Gap
3. **A.8.8 (기술적 취약점 관리)**: 4개 취약점 - Non-Compliant
4. **A.5.17 (인증 정보)**: 4개 취약점 - Non-Compliant

## [개선 로드맵]

### Phase 1: Quick Win (즉시, 1주 이내)
**4개 항목 - Critical 취약점 긴급 패치**
- SQL Injection 완전 제거 (28개 지점)
- OS Command Injection 차단
- 쿠키 변조 방어 구현
- 파일 업로드 보안 강화

### Phase 2: Short-term (1-2개월)
**12개 항목 - High 취약점 해결**
- 접근 제어 강화 (IDOR 방어)
- 세션 관리 개선
- OS 보안 설정 강화
- 불필요한 서비스 비활성화

### Phase 3: Mid-term (2-4개월)
**10개 항목 - Medium 취약점 해결**
- 로깅 및 모니터링 체계 구축
- 보안 정책 수립 및 적용
- 파일 권한 정비

### Phase 4: Long-term (4-6개월)
**1개 항목 - 지속적 개선**
- 보안 교육 프로그램
- 정기 취약점 진단 체계

## [예상 비용 및 일정]

- **총 소요 기간**: 6개월
- **ISO 27001 인증 신청 가능 시점**: Phase 2 완료 후 (약 3개월)

### 예상 투입 인력
- 보안 엔지니어: 2명 (전담)
- 백엔드 개발자: 3명 (파트타임)
- 인프라 엔지니어: 1명 (파트타임)
- 컨설턴트: 1명 (주간 리뷰)

### 예상 비용
- Phase 1 (긴급): 약 3,000만원
- Phase 2 (단기): 약 5,000만원
- Phase 3-4 (중장기): 약 4,000만원
- **총 예상 비용**: 약 1억 2,000만원

## [프로젝트 구조]

```
iso27001_consulting_report/
├── README.md                          # 프로젝트 개요 및 가이드
├── iso27001_consulting_report.ipynb  # Jupyter Notebook (전체 분석 프로세스)
├── all_vulnerabilities.csv            # 전체 취약점 데이터
├── gap_analysis.csv                   # ISO 27001 Gap Analysis
├── remediation_roadmap.csv            # 개선 로드맵
├── executive_summary.txt              # 경영진용 요약 보고서
├── technical_report.txt               # 기술 상세 보고서
└── vulnerability_analysis.png         # 취약점 분석 차트
```

## [핵심 취약점 개선 예시]

### 1. SQL Injection (WEB-002)
**Before (취약한 코드):**
```xml
<!-- MyBatis Mapper -->
<select id="login" resultType="User">
    SELECT * FROM users 
    WHERE username = '${username}' 
    AND password = '${password}'
</select>
```

**After (개선된 코드):**
```xml
<!-- MyBatis Mapper -->
<select id="login" resultType="User">
    SELECT * FROM users 
    WHERE username = #{username} 
    AND password = #{password}
</select>
```

### 2. OS Command Injection (WEB-003)
**Before (취약한 코드):**
```java
@PostMapping("/ping")
public String ping(@RequestParam String host) {
    String command = "ping " + host;
    Runtime.getRuntime().exec(command);
    return "success";
}
```

**After (개선된 코드):**
```java
@PostMapping("/ping")
public String ping(@RequestParam String host) {
    // 화이트리스트 검증
    if (!host.matches("^[0-9.]+$")) {
        throw new IllegalArgumentException("Invalid host");
    }
    
    // ProcessBuilder 사용 (인수 분리)
    ProcessBuilder pb = new ProcessBuilder("ping", "-c", "4", host);
    pb.start();
    return "success";
}
```

## [데이터 분석 프로세스]

1. **취약점 데이터 구조화**: PDF 리포트에서 취약점 데이터 추출 및 DataFrame 생성
2. **CVSS 스코어링 및 심각도 분류**: 각 취약점의 위험도 평가
3. **ISO 27001:2022 통제항목 매핑**: 취약점을 ISO 표준과 연결
4. **Gap Analysis**: 현재 상태 vs 요구사항 비교
5. **우선순위 기반 로드맵 생성**: 개선 작업 단계별 계획
6. **시각화 및 보고서 작성**: 경영진/기술팀용 문서 생성

## [시각화]

### 생성된 차트 (vulnerability_analysis.png)
- **Severity Distribution**: 심각도별 취약점 분포
- **CVSS Score Distribution**: CVSS 스코어 히스토그램
- **Vulnerability Type Distribution**: 웹/OS 취약점 비율
- **Top 10 ISO Controls Affected**: 영향받는 ISO 통제항목

## [보고서 종류]

### 1. Executive Summary (executive_summary.txt)
- 경영진용 요약 보고서
- 비즈니스 리스크 관점 작성
- 예상 비용 및 일정 포함

### 2. Technical Report (technical_report.txt)
- 기술팀용 상세 보고서
- Critical 취약점별 Before/After 코드 예시
- 구체적인 개선 방안 제시

### 3. Data Files (CSV)
- all_vulnerabilities.csv: 전체 취약점 원본 데이터
- gap_analysis.csv: ISO 27001 통제항목별 준수성 평가
- remediation_roadmap.csv: 단계별 개선 계획

## [실행 방법]

### Jupyter Notebook에서 실행
```bash
jupyter notebook iso27001_consulting_report.ipynb
```

### Python 스크립트로 실행
모든 분석과 보고서는 이미 생성되어 있으며, 각 파일을 직접 확인할 수 있습니다.

## [주요 인사이트]

1. **Critical/High 취약점이 59.3%**: 즉각적인 조치 필요
2. **SQL Injection이 가장 심각**: 28개 지점에서 발견, 데이터 유출 위험
3. **A.8.3, A.8.16 통제항목이 Critical Gap**: 접근 제어 및 모니터링 강화 필요
4. **3개월 내 인증 신청 가능**: 체계적 개선 시 현실적인 목표

## [결론]

DNA Lab은 현재 ISO 27001 인증이 불가능한 상태이나, 제시된 로드맵에 따라 체계적으로 개선할 경우 **3개월 내 인증 신청이 가능**합니다.

특히 Quick Win 단계의 Critical 취약점들은 비즈니스 연속성과 고객 신뢰에 직결되므로 **즉시 조치**를 권고합니다.

보안 개선은 단순한 비용이 아닌, **기업 가치를 높이고 B2B 계약을 성사시키는 투자**입니다.

---

**작성일**: 2026-01-11  
**작성자**: SK Shields 보안 컨설팅팀  
**문의**: SK Shieldus Rookies AWS Cloud Training Program - Week 10 Project
