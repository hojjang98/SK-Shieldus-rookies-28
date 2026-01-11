## 프로젝트 개요

본 프로젝트는 웹 애플리케이션 보안 취약점을 자동으로 탐지하는 Python 기반 스캐너 도구입니다. 교육 목적으로 의도적으로 취약하게 제작된 Flask 웹 애플리케이션과 이를 진단하는 자동화 스크립트로 구성되어 있습니다.

## 주요 기능

### 1. 취약한 웹 애플리케이션 (Vulnerable Web App)
- **기술 스택**: Flask, SQLite, HTML/CSS (Bootstrap)
- **포함된 취약점**:
  - SQL Injection (로그인, 검색)
  - XSS (Cross-Site Scripting) (게시판)
  - CSRF (Cross-Site Request Forgery) (프로필 수정)
  - File Upload Vulnerability (파일 업로드)

### 2. 자동화 취약점 스캐너
- **SQL Injection Scanner**: 로그인 폼 및 검색 기능의 SQL Injection 취약점 탐지
- **XSS Scanner**: 게시판 및 검색 기능의 XSS 취약점 탐지
- **CSRF Scanner**: CSRF 토큰 누락 여부 확인
- **File Upload Scanner**: 위험한 파일 확장자 업로드 가능 여부 테스트
- **Integrated Scanner**: 모든 스캐너를 통합 실행하여 종합 리포트 생성

## 디렉토리 구조
```
week_9/
├── vulnerable_app/          # 취약한 웹 애플리케이션
│   ├── app.py              # Flask 메인 애플리케이션
│   ├── init_db.py          # 데이터베이스 초기화 스크립트
│   ├── database.db         # SQLite 데이터베이스
│   ├── templates/          # HTML 템플릿
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── board.html
│   │   ├── write_post.html
│   │   ├── search.html
│   │   ├── upload.html
│   │   ├── files.html
│   │   └── profile.html
│   ├── static/             # 정적 파일
│   └── uploads/            # 업로드된 파일 저장
├── scanners/               # 취약점 스캐너
│   ├── sql_injection_scanner.py
│   ├── xss_scanner.py
│   ├── csrf_scanner.py
│   ├── file_upload_scanner.py
│   └── integrated_scanner.py
├── reports/                # 스캔 리포트
│   ├── sql_injection_report.txt
│   ├── xss_report.txt
│   ├── csrf_report.txt
│   ├── file_upload_report.txt
│   └── FINAL_COMPREHENSIVE_REPORT_*.txt
├── screenshots/            # 프로젝트 스크린샷
├── web_security_scanner.ipynb  # 프로젝트 생성 스크립트 (Jupyter Notebook)
└── README.md
```

## 설치 및 실행

### 1. 필요한 패키지 설치
```bash
pip install flask requests beautifulsoup4
```

### 2. 데이터베이스 초기화
```bash
cd web_security_project/vulnerable_app
python init_db.py
```

### 3. Flask 웹 서버 실행
```bash
python app.py
```

웹 브라우저에서 `http://localhost:5000` 접속

### 4. 취약점 스캐너 실행

#### 개별 스캐너 실행
```bash
cd ../scanners

# SQL Injection 스캔
python sql_injection_scanner.py

# XSS 스캔
python xss_scanner.py

# CSRF 스캔
python csrf_scanner.py

# File Upload 스캔
python file_upload_scanner.py
```

#### 통합 스캐너 실행 (모든 스캔을 한 번에)
```bash
python integrated_scanner.py
```

## 테스트 계정

- **관리자**: admin / admin123
- **일반 사용자**: user1 / password1
- **테스트 사용자**: testuser / test123

## 발견된 취약점 요약

### SQL Injection
- **위치**: 로그인 폼, 검색 기능
- **심각도**: HIGH ~ CRITICAL
- **페이로드 예시**: `' OR '1'='1`, `' UNION SELECT username, password FROM users--`

### XSS (Cross-Site Scripting)
- **위치**: 게시판, 검색 결과
- **심각도**: HIGH
- **페이로드 예시**: `<script>alert('XSS')</script>`, `<img src=x onerror=alert('XSS')>`

### CSRF (Cross-Site Request Forgery)
- **위치**: 프로필 수정, 게시글 작성
- **심각도**: HIGH ~ MEDIUM
- **문제점**: CSRF 토큰 미구현

### File Upload Vulnerability
- **위치**: 파일 업로드 기능
- **심각도**: CRITICAL
- **문제점**: 파일 확장자 검증 없음, 위험한 파일 업로드 가능

## 보안 권장사항

> 여기서는 해킹만 연습했지만, 만약 보안을 해야한다면?

### SQL Injection 방어
- Parameterized Queries (Prepared Statements) 사용
- ORM 프레임워크 활용
- 입력값 검증 및 sanitization

### XSS 방어
- Output Encoding/Escaping 구현
- Content Security Policy (CSP) 적용
- Template Engine의 Auto-escaping 활용

### CSRF 방어
- CSRF 토큰 구현
- SameSite 쿠키 속성 사용
- Origin/Referer 헤더 검증

### File Upload 보안
- 화이트리스트 기반 확장자 검증
- 파일 내용 검증 (Magic Bytes)
- 업로드 파일을 웹 루트 외부에 저장
- 파일명 변경 및 크기 제한

## 스캔 리포트

모든 스캔 결과는 `reports/` 디렉토리에 자동 저장됩니다:
- 개별 스캔 리포트 (txt 형식)
- 통합 종합 리포트 (FINAL_COMPREHENSIVE_REPORT_*.txt)

## 주의사항

본 프로젝트는 **교육 목적으로만** 사용되어야 합니다. 

## 학습 목표

1. 웹 애플리케이션의 주요 보안 취약점 이해
2. Python을 활용한 보안 자동화 스크립트 개발
3. 취약점 탐지 및 리포팅 능력 향상
4. 실전 웹 보안 테스트 경험
