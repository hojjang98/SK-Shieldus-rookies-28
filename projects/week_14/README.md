# Week 14: 보안 컨설팅 프로젝트 - 보안 개선

## Week 3/4: 보안 개선 단계

Week 13에서 발견한 취약점들을 실제로 수정하고 보안이 강화된 시스템을 구축한다.

---

## 개선 목표

1. Critical/High 취약점 완전 제거
2. Medium 취약점 보완
3. Low 취약점 개선
4. Before/After 비교 검증

---

## 폴더 구조
```
week_14/
├── README.md
├── ecommerce_secure/           # 보안 강화 버전 코드
│   ├── app.py
│   ├── init_db.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── product.html
│   │   ├── cart.html
│   │   └── profile.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── uploads/
│
└── security_assessment/        # 검증 결과
    ├── before_attack/          # Week 12 공격 성공
    ├── after_defense/          # Week 14 방어 성공
    └── scan_results/           # ZAP 스캔 결과
```

---

## 개선 범위

### Critical 취약점 수정
1. **SQL Injection 방어**
   - Prepared Statement 적용
   - 파라미터 바인딩 사용
   - 검증: 로그인 우회 차단, 검색 필터 우회 차단

2. **XSS 방어**
   - HTML 자동 이스케이프 처리
   - |safe 필터 제거
   - 검증: 스크립트가 텍스트로 표시됨

### High 취약점 수정
3. **파일 업로드 검증**
   - 화이트리스트 방식 (png, jpg, jpeg, gif만 허용)
   - secure_filename() 사용
   - 검증: txt 파일 업로드 차단

### Medium 취약점 수정
4. **CSRF 방어**
   - Flask-WTF 적용
   - 모든 POST 폼에 CSRF 토큰 추가

5. **보안 헤더 설정**
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - Content-Security-Policy 적용
   - X-XSS-Protection 적용

---

## 실행 방법
```bash
cd week_14/ecommerce_secure
pip install -r requirements.txt
python init_db.py
python app.py
```

포트: 5001 (Week 12와 동시 실행 가능)

---

## 검증 결과

### Before/After 수동 테스트

모든 취약점에 대해 공격 시도 후 방어 확인 완료

**스크린샷:**
- `security_assessment/before_attack/` - Week 12 공격 성공 화면
- `security_assessment/after_defense/` - Week 14 방어 성공 화면

### ZAP 자동 스캔 결과

| 구분 | Week 12 (취약) | Week 14 (개선) | 변화 |
|------|----------------|----------------|------|
| High | 0 | 0 | - |
| Medium | 3개 | 2개 | 1개 감소 |
| Low | 5개 | 4개 | 1개 감소 |
| Info | 6개 | 6개 | - |

**개선 확인:**
- CSRF 토큰 적용으로 Medium 취약점 1개 해결
- 보안 헤더 추가로 Low 취약점 1개 해결
- 총 2개 취약점 자동 스캔으로 개선 확인

**스캔 결과:** `security_assessment/scan_results/`

**참고:** SQL Injection, XSS 같은 Critical/High 취약점은 자동 스캔으로 탐지되지 않았으나, 수동 테스트를 통해 모두 차단됨을 확인했습니다.

---

## 다음 주 계획

Week 15에서는 모니터링 체계 구축 및 최종 컨설팅 보고서 작성