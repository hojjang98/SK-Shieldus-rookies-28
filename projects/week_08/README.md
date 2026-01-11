# Week 8: 웹 해킹 기초 - 취약한 웹 애플리케이션 구축 및 공격 실습

## 프로젝트 개요

본 프로젝트는 **의도적으로 취약한 웹 애플리케이션**을 직접 개발하고, SQL Injection과 XSS 공격을 실제로 수행하여 웹 보안 취약점을 이해하는 실습 프로젝트입니다.

---

## 배경

웹 애플리케이션의 보안 취약점은 실제 서비스에서 치명적인 피해를 발생시킬 수 있습니다. 본 프로젝트는 **OWASP Top 10**에 포함된 대표적인 취약점인 SQL Injection과 Cross-Site Scripting(XSS)을 직접 구현하고 공격해봄으로써, 보안의 중요성을 체험합니다.

---

## 프로젝트 목표

1. **취약점 이해**: SQL Injection, XSS의 작동 원리 파악
2. **공격 실습**: 실제 공격 기법 직접 수행
3. **보안 인식**: 안전한 코딩의 필요성 체감
4. **실전 경험**: Flask 기반 웹 애플리케이션 개발

---

## 구축된 시스템

### 웹 애플리케이션 구조
```
┌─────────────────────────────────────┐
│         사용자 (브라우저)             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    Flask Web Application             │
│    (로그인 + 게시판)                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    SQLite Database                   │
│    - users 테이블                    │
│    - posts 테이블                    │
└─────────────────────────────────────┘
```

---

## 구현된 취약점

### 1. SQL Injection (로그인 우회)
- **위치**: 로그인 페이지
- **취약 코드**: 사용자 입력을 직접 SQL 쿼리에 삽입
- **공격 방법**: `admin' --`
- **결과**: 비밀번호 없이 관리자 로그인 성공

### 2. Cross-Site Scripting (XSS)
- **위치**: 게시판 글 작성
- **취약 코드**: HTML 필터링 없이 출력 (`|safe`)
- **공격 방법**: `<script>alert('XSS 공격 성공!')</script>`
- **결과**: 악성 스크립트 실행

---

## 프로젝트 구조
```bash
week8_web_hacking/
├── README.md
├── docs/
│   └── Web_Hacking_실습_보고서.md
├── vulnerable_webapp/
│   ├── templates/
│   │   ├── login.html
│   │   └── board.html
│   └── users.db
├── screenshots/
│   ├── 01_sql_injection.png
│   ├── 02_login_approved.png
│   ├── 03_xss.png
│   └── 04_xss_success.png
└── notebook/
    └── web_hacking_lab.ipynb
```

---

## 실습 환경

- **개발 환경**: Jupyter Notebook
- **프레임워크**: Flask 2.2.2
- **데이터베이스**: SQLite3
- **실습일**: 2025년 12월 23일
- **소요 시간**: 약 1시간

---

## 핵심 성과

### SQL Injection 공격 성공
- 로그인 인증 우회
- 데이터베이스 쿼리 조작
- 공격 원리 완전 이해

### XSS 공격 성공
- 악성 스크립트 삽입
- JavaScript 코드 실행
- 실제 위협 시나리오 학습

---

## 학습 내용

| 영역 | 학습 내용 |
|------|----------|
| **웹 개발** | Flask, HTML, SQLite |
| **보안 취약점** | SQL Injection, XSS |
| **공격 기법** | 인증 우회, 스크립트 삽입 |
| **방어 기법** | Prepared Statement, Input Validation |

---

## 방어 방법 (요약)

### SQL Injection 방어
- Prepared Statement 사용
- 사용자 입력 검증
- ORM 프레임워크 활용

### XSS 방어
- HTML Escape 처리
- Content Security Policy (CSP)
- `|safe` 필터 제거

---

## 참고 자료

- OWASP Top 10
- Flask 공식 문서
- SQL Injection 가이드
- XSS Prevention Cheat Sheet