# DNA Lab Security Scanner

> 유전자 검사 웹 애플리케이션을 위한 종합 취약점 진단 도구

## 개요

**DNA Lab Security Scanner**는 민감한 유전 정보를 다루는 웹 애플리케이션을 위한 자동화된 보안 취약점 진단 프레임워크입니다. Team Helix가 DNA Lab 사이버보안 프로젝트의 일환으로 개발한 이 도구는 정적 코드 분석과 동적 모의 침투 테스트를 결합하여 바이오인포매틱스 플랫폼의 치명적인 보안 결함을 식별합니다.

### 프로젝트 배경

2023년, 유전자 검사 기업 23andMe는 690만 명의 사용자에게 영향을 미친 대규모 데이터 유출 사고를 겪었습니다. 이 사건은 유전 정보를 다루는 플랫폼에 강력한 보안 조치가 얼마나 중요한지 보여주었습니다. 우리 프로젝트는 취약한 DNA 검사 서비스("Rookies DNA")를 시뮬레이션하고, 보안 취약점을 식별하고 개선할 수 있는 종합적인 스캐닝 도구를 제공합니다.

## 주요 기능

### 종합 취약점 탐지 (웹 15개 + OS 50개 스캐너)

### 종합 취약점 탐지 (웹 15개 + OS 50개 스캐너)

#### 웹 애플리케이션 스캐너 (15개)

1. **XSS (Cross-Site Scripting)** - Stored, Reflected, DOM 기반 XSS 탐지
2. **SQL Injection** - MyBatis XML 분석 및 동적 페이로드 테스트
3. **Code Injection** - Thymeleaf 템플릿 취약점 스캔
4. **CSRF** - 토큰 검증 및 SameSite 쿠키 확인
5. **Weak Password Policy** - 복잡도 및 무차별 대입 방어 테스트
6. **Access Control** - 인증 우회 및 권한 취약점 (IDOR, 권한 상승)
7. **Password Recovery** - 취약한 비밀번호 재설정 메커니즘 탐지
8. **Session Management** - 세션 고정 및 로그아웃 검증
9. **Cookie Security** - 쿠키 변조 및 플래그 확인
10. **File Transfer** - 악성 파일 업로드 및 경로 조작 테스트
11. **Path Traversal** - 디렉토리 순회 취약점 탐지
12. **Error Handling** - 에러 메시지를 통한 정보 노출
13. **Format String** - 포맷 스트링 인젝션 취약점
14. **HTTP Methods** - 불필요한 메서드 노출 (TRACE, PUT, DELETE)
15. **SSRF** - 서버측 요청 위조 및 명령어 인젝션

#### 운영체제 보안 스캐너 (50개)

**인증 및 계정 관리 (12개)**
- Root 원격 로그인 허용
- 비밀번호 정책 미흡
- 계정 잠금 정책 부재
- 패스워드 파일 보호 미흡
- Root UID 0 확인
- Root su 제한 미흡
- 유효하지 않은 GID
- 중복 UID
- 사용자 쉘 점검
- 세션 타임아웃 설정
- 패스워드 해싱 알고리즘
- Root 홈 디렉토리 경로

**파일 및 디렉토리 권한 (10개)**
- 파일 소유권 확인
- passwd 파일 권한
- 시작 스크립트 권한
- Shadow 파일 권한
- Hosts 파일 권한
- inetd 설정 권한
- Syslog 권한
- services 파일 권한
- SUID/SGID 파일 점검
- 사용자 시작 파일 권한

**네트워크 서비스 (20개)**
- 홈 디렉토리 존재 확인
- Finger 서비스
- 익명 FTP 접근
- r 계열 서비스
- Crontab 권한
- DoS 서비스
- NFS 서비스
- NFS 접근 제어
- Automount 서비스
- RPC 서비스
- NIS 서비스
- TFTP/TALK 서비스
- Sendmail 버전
- FTP 배너
- FTP 서비스 비활성화
- FTP 쉘 제한
- ftpusers 권한
- ftpusers root 접근
- SNMP 서비스
- SNMP community string

**시스템 설정 (8개)**
- Sudoers 권한
- NTP 설정
- 로깅 정책
- 로그 디렉토리 권한
- 콘솔 로그인 제한

### 하이브리드 스캔 방식

### 하이브리드 스캔 방식

- **화이트박스 분석** - Java, XML, Thymeleaf 템플릿의 정적 코드 검사
- **블랙박스 테스트** - 인증/비인증 세션을 통한 동적 모의 침투 테스트
- **지능형 크롤링** - 엔드포인트 및 폼 자동 탐색

### 전문 리포팅

- **TXT 리포트** - 빠른 검토를 위한 일반 텍스트 요약
- **HTML 리포트** - 색상 코드로 구분된 결과가 포함된 대화형 대시보드
- **PDF 리포트** - 이해관계자를 위한 전문 문서
- **상세 개선 방안** - 각 취약점에 대한 구체적인 수정 권장사항

## 빠른 시작

### 사전 요구사항

```bash
# Python 3.8 이상
python --version

# 의존성 설치
pip install -r requirements.txt --break-system-packages
```

### 설치

```bash
# 저장소 클론
git clone https://github.com/sk28project/project
cd dna-lab-security-scanner

# 대상 설정 구성
cp config.json.example config.json
# config.json 파일을 편집하여 대상 URL 및 자격 증명 입력
```

### 구성

`config.json` 편집:

```json
{
    "target_url": "http://localhost:8080",
    "project_path": "/path/to/your/project",
    "admin_login": {
        "username": "admin",
        "password": "your_password"
    },
    "guest_login": {
        "username": "guest",
        "password": "guest"
    }
}
```

### 스캔 실행

```bash
# 스캐너 실행
python main.py

# 스캔 모드 선택:
# 1. 정적 스캔 (화이트박스 + 기본 블랙박스)
# 2. 동적 스캔 (크롤러 + 능동 테스트)
# 3. 전체 스캔 (정적 + 동적)
```

## 프로젝트 구조

```
dna-lab-security-scanner/
├── main.py                          # 메인 스캐너 오케스트레이터
├── config.json                      # 대상 구성
├── crawler.py                       # 엔드포인트 탐색을 위한 웹 크롤러
├── dynamic_scanner.py               # 동적 취약점 테스트
│
├── 01_xss_scanner.py               # XSS 취약점 탐지
├── 02_sqli_scanner.py              # SQL 인젝션 테스트
├── 03_code_injection_scanner.py    # 코드 인젝션 분석
├── 04_csrf_scanner.py              # CSRF 보호 검증
├── 05_weak_password.py             # 비밀번호 정책 테스트
├── 06_access_control_scanner.py    # 권한 결함 탐지
├── 07_password_recovery.py         # 비밀번호 재설정 보안
├── 08_session_scanner.py           # 세션 관리 테스트
├── 09_cookie_scanner.py            # 쿠키 보안 검증
├── 10_file_transfer_scanner.py     # 파일 업로드/다운로드 테스트
├── 11_path_traversal_scanner.py    # 디렉토리 순회 탐지
├── 12_error_page_scanner.py        # 에러 처리 분석
├── 13_formatting_scanner.py        # 포맷 스트링 취약점
├── 14_http_method_scanner.py       # HTTP 메서드 보안
├── 15_ssrf_scanner.py              # SSRF 및 명령어 인젝션
│
└── reports/                         # 생성된 스캔 리포트
    ├── scan_report_YYYYMMDD_HHMMSS.txt
    ├── scan_report_YYYYMMDD_HHMMSS.html
    └── scan_report_YYYYMMDD_HHMMSS.pdf
```

## 기술 아키텍처

### 스캐너 설계 패턴

각 취약점 스캐너는 일관된 API를 따릅니다:

```python
def scan(target_url, login_info=None):
    return {
        'name': '취약점 이름',
        'vulnerable': True/False,
        'details': ['발견사항 1', '발견사항 2'],
        'recommendation': '수정 제안'
    }
```

### 정적 분석 기법

- **MyBatis XML 파싱** - 안전하지 않은 `${}` 파라미터 바인딩 탐지
- **Thymeleaf 템플릿 분석** - `th:utext` 및 인라인 표현식 식별
- **Java 소스 코드 스캔** - 보안 결함에 대한 정규식 기반 패턴 매칭
- **구성 파일 검토** - 보안 설정 검증

### 동적 테스트 방법

- **페이로드 인젝션** - XSS, SQLi, 명령어 인젝션 페이로드
- **인증 테스트** - 로그인 우회 및 세션 관리
- **권한 확인** - IDOR, 수평/수직 권한 상승
- **응답 분석** - 에러 메시지 및 헤더 검사

## 샘플 출력

### 콘솔 출력

```
============================================================
 DNA Lab Security Vulnerability Scanner
============================================================
 Target: http://localhost:8080
------------------------------------------------------------
 Select Scan Mode:
  1. Static Scan (Whitebox + Basic Blackbox)
  2. Dynamic Scan (Crawler + Active Scan)
  3. Full Scan (Static + Dynamic)

 > Choice [1]: 3

[ Phase 1: Static Scan ]
[*] Running XSS scanner (1/15)... [!] VULNERABLE
[*] Running SQL Injection scanner (2/15)... [!] VULNERABLE
[*] Running Code Injection scanner (3/15)... [+] Safe
...

============================================================
 Scan Complete
============================================================
 Reports generated:
  - TXT:  reports/scan_report_20260111_143022.txt
  - HTML: reports/scan_report_20260111_143022.html
  - PDF:  reports/scan_report_20260111_143022.pdf (Created)

 Summary: 12 Vulnerabilities found.
```

### HTML 리포트 미리보기

HTML 리포트에는 다음이 포함됩니다:
- 취약점 통계가 포함된 경영진 요약
- 색상 코드로 구분된 발견사항 (취약한 항목은 빨간색, 안전한 항목은 녹색)
- 상세한 기술 설명
- 실행 가능한 개선 단계

## 보안 고려사항

이 도구는 **승인된 보안 테스트 전용**으로 설계되었습니다. 주요 원칙:

- 소유하고 있거나 명시적인 테스트 권한이 있는 시스템에만 사용
- 무단 접근을 피하기 위해 자격 증명을 신중하게 구성
- 공유하기 전에 생성된 리포트에서 민감한 정보를 검토
- 적절한 승인 없이 프로덕션 시스템에 대해 절대 사용 금지
- 악의적인 목적으로 사용 금지

## Team Helix

- **호짱** - 리드 보안 엔지니어, 스캐너 개발 
- **김기남** - 백엔드 및 프론트엔드 개발 및 os 스캐너 개발
- **신동원** - 서비스 스캐너 개발
- **이진주** - os 스캐너 개발
- **최호준** - 시스템 통합

## 참고 자료

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [MyBatis Security Best Practices](https://mybatis.org/mybatis-3/sqlmap-xml.html)
- [Thymeleaf Security](https://www.thymeleaf.org/doc/articles/springsecurity.html)

## 라이센스

이 프로젝트는 MIT 라이센스에 따라 라이센스가 부여됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.

## 감사의 말

- 2023년 23andMe 데이터 유출 사건에서 영감을 받음
- 사이버 보안 모범 사례의 지침을 바탕으로 구축
- 교육 및 보안 연구 목적으로 개발

---

**주의사항**: 이 도구는 교육 및 승인된 보안 테스트 목적으로만 사용됩니다. 개발자는 이 프로그램으로 인한 오용이나 손상에 대해 책임을 지지 않습니다. 시스템을 테스트하기 전에 항상 적절한 승인을 받으세요.