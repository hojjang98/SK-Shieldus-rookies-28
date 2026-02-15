# 🧠 Projects

이 디렉토리는 **SK Shielders 루키즈 28기 과정 중 스스로 수행하는 개인 실무 프로젝트**를 모아두는 공간이다.  
매주 배운 내용을 토대로 **직접 설계·구현하며**, 이를 통해 **실무에서 어떻게 적용할 수 있는지 체득**하는 것을 목표로 한다.

---

## 🎯 목적 (Purpose)

- 매주 학습한 내용을 **직접 프로젝트 형태로 구현**하여 이론과 실무의 연결고리를 만든다.
- 스스로 문제를 정의하고 해결하는 과정을 통해 **실전 역량**을 기른다.
- 단순한 지식 습득을 넘어, **보안 전문가로서의 사고방식과 업무 프로세스**를 체득한다.

---

## 📁 프로젝트 목록 (Projects)

| 주차 | 프로젝트명 | 주요 내용 |
|------|-------------|-----------|
| **Week 1** | 🛡️ Mini Security Log Monitor | 로그 파일(`system.log`)의 오류 이벤트를 탐지하고, 접근 결과를 JSON(`access.log`) 형식으로 기록하는 보안 감사 시스템 |
| **Week 2** | 📊 Streamlit Log Dashboard | Week1에서 생성된 로그 데이터를 시각화하여, 보안 이벤트의 발생 추이와 접근 현황을 대시보드 형태로 표현하는 프로젝트 |
| **Week 3 & 4** | 🎬 LLM/RAG 기반 영화 흥행 분석 시스템 | **LangChain, ChromaDB, Streamlit**을 활용하여 RAG 기반 영화 추천/분석 기능 및 흥행 요인 시각화 대시보드를 구축하고 최종 발표. (Week 3의 LLM/RAG 실습 내용을 확장 적용) |
| **Week 5** | 🐧 리눅스 파일 시스템 및 권한 관리 보고서 | 리눅스 파일 시스템의 계층적 디렉토리 구조 및 파일 타입 분석. 소유자/그룹/기타 사용자 기반의 권한 구조와 chmod를 이용한 심볼릭/숫자 모드 권한 변경 실습. 최소 권한 원칙 및 SetUID, Sticky Bit 등 특수 권한의 보안 관점에서의 중요성 분석 |
| **Week 6** | 🌐 TCP/IP 네트워크 프로토콜 분석 보고서 | OSI/TCP-IP 계층 모델 이해, ARP, ICMP, TCP 3-Way Handshake, HTTPS/TLS 동작 원리 분석, 그리고 Wireshark를 활용한 패킷 분석 및 방화벽, IDS/IPS 기반 네트워크 보안 기초 학습 |
| **Week 7** | ☁️ AWS 3-Tier 웹 인프라 완전 구축 | 프로덕션 수준의 완전한 3-Tier 아키텍처 구축. Multi-AZ VPC 네트워크 설계 (6개 Subnets, NAT Gateway 2개), Application Load Balancer 및 Auto Scaling Group 구성, RDS MySQL 데이터베이스 구축, Security Groups 계층별 보안 설정. 실제 구축 시간 3시간, 비용 ~$0.5로 고가용성 웹 인프라 완성 |
| **Week 8** | 🕷️ 웹 해킹 기초 - 취약한 웹 애플리케이션 구축 및 공격 실습 | **OWASP Top 10** 기반 의도적으로 취약한 Flask 웹 애플리케이션 개발. SQL Injection 로그인 우회 (`admin' --`), XSS 공격 (`<script>alert('XSS')</script>`) 직접 시연. Prepared Statement 및 HTML Escape 방어 기법 학습. 로그인 + 게시판 기능 구현, SQLite DB 사용. 보안의 중요성 체감 및 안전한 코딩 실전 경험 |
| **Week 9** | 🔍 웹 보안 자동화 스캐너 개발 | Python 기반 취약점 자동 탐지 도구 개발. SQL Injection, XSS, CSRF, File Upload 취약점을 자동으로 스캔하는 통합 스캐너 구축. 취약한 Flask 애플리케이션 + 4개 개별 스캐너 + 통합 스캐너 개발. 보안 테스트 자동화 및 리포팅 능력 향상 |
| **Week 10 & 11** | 🧬 DNA Lab 종합 보안 진단 프로젝트 (팀 프로젝트) | 유전자 검사 웹 애플리케이션 **Team Helix** 보안 컨설팅. 웹 취약점 15개 + OS 보안 50개 = 총 65개 스캐너 개발. 화이트박스(정적 분석) + 블랙박스(동적 테스트) 하이브리드 진단 방식. MyBatis XML, Thymeleaf 템플릿, Java 소스 코드 분석. TXT/HTML/PDF 리포트 자동 생성. 23andMe 데이터 유출 사례 기반 시나리오. ISO 27001 Gap Analysis 및 개선 로드맵 제시 |
| **Week 10** | 📋 ISO 27001 보안 컨설팅 보고서 작성 | DNA Lab 진단 결과 기반 ISO 27001:2022 준수성 평가. 총 27개 취약점 (Critical 4개, High 12개), 평균 CVSS 7.10. 14개 통제항목 Gap Analysis, 4단계 개선 로드맵 (Quick Win → Short-term → Mid-term → Long-term) 수립. 예상 비용 1억 2천만원, 6개월 일정. 경영진용 Executive Summary + 기술팀용 Technical Report 작성. Before/After 코드 예시 포함 |
| **Week 12-15** | 🛒 보안 컨설팅 전체 프로세스 (4주 프로젝트) | 실무 보안 컨설턴트처럼 **취약한 시스템 구축 → 진단 → 개선 → 모니터링**까지 A to Z 경험. Week 12: 의도적으로 취약한 E-Commerce 웹 애플리케이션 구축 (SQL Injection, XSS, 인증 우회, 파일 업로드). Week 13: OWASP ZAP 자동 스캔 + Python 스크립트 수동 진단, Critical 2개/High 2개 발견. Week 14: Prepared Statement, HTML Escape, 파일 검증, CSRF 토큰 적용하여 6개 취약점 해결. Week 15: 로그 분석 시스템 + 보안 대시보드 구축, 최종 컨설팅 보고서 작성 |
| **Week 16** | 📑 파이널 프로젝트 준비 - 개인정보 위·수탁 관리체계 컨설팅 | 파이널 프로젝트 사전 조사 및 기획. 위탁자 1개 + 수탁사 N개 구조 이해, 전기수 참고 사례 분석 (S카드 → 18개 수탁사). 팀원별 업종 조사 (이커머스, 금융, AI 기업 등), AI 기업 위·수탁 관계 심화 분석. 수탁사 20개 유형 리스트업 (클라우드, 데이터 라벨링, 고객센터 등), AI 관련 보안 사건 6건 조사 (이루다 개인정보 유출, ChatGPT 데이터 유출, 삼성 기밀 유출 등). 5차 멘토링 계획 및 산출물 6개 파악 (프로젝트 수행계획서, 정보보호협약서, 진단 체크리스트, 현황관리 양식, 진단결과 보고서, 최종 보고서) |
