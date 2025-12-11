# 🧠 Projects

이 디렉토리는 **SK Shielders 루키즈 28기 과정 중 스스로 수행하는 개인 실무 프로젝트**를 모아두는 공간이다.  
매주 배운 내용을 토대로 **직접 설계·구현하며**, 이를 통해 **실무에서 어떻게 적용할 수 있는지 체득**하는 것을 목표로 한다.

---

## 🎯 목적 (Purpose)

- 학습한 파이썬 문법과 보안 개념을 **직접 프로젝트 형태로 구현**해 본다.  
- 스스로 아이디어를 구상하고 개발함으로써, **이론이 실제 업무에 어떻게 연결되는지**를 경험한다.  
- 단순한 코드 작성이 아니라, **보안 실무에 응용 가능한 사고방식**을 기르는 데 초점을 둔다.

---

## 📁 프로젝트 목록 (Projects)

| 주차 | 프로젝트명 | 주요 내용 |
|------|-------------|-----------|
| **Week 1** | 🛡️ Mini Security Log Monitor | 로그 파일(`system.log`)의 오류 이벤트를 탐지하고, 접근 결과를 JSON(`access.log`) 형식으로 기록하는 보안 감사 시스템 |
| **Week 2** | 📊 Streamlit Log Dashboard | Week1에서 생성된 로그 데이터를 시각화하여, 보안 이벤트의 발생 추이와 접근 현황을 대시보드 형태로 표현하는 프로젝트 |
| **Week 3 & 4** | 🎬 LLM/RAG 기반 영화 흥행 분석 시스템 | **LangChain, ChromaDB, Streamlit**을 활용하여 RAG 기반 영화 추천/분석 기능 및 흥행 요인 시각화 대시보드를 구축하고 최종 발표. (Week 3의 LLM/RAG 실습 내용을 확장 적용) |
| **Week 5** | 🐧 리눅스 파일 시스템 및 권한 관리 보고서 | 리눅스 파일 시스템의 계층적 디렉토리 구조 및 파일 타입 분석. 소유자/그룹/기타 사용자 기반의 권한 구조와 chmod를 이용한 심볼릭/숫자 모드 권한 변경 실습. 최소 권한 원칙 및 SetUID, Sticky Bit 등 특수 권한의 보안 관점에서의 중요성 분석 |
| **Week 6** | 🌐 TCP/IP 네트워크 프로토콜 분석 보고서 | OSI/TCP-IP 계층 모델 이해 , ARP, ICMP, TCP 3-Way Handshake, HTTPS/TLS 동작 원리 분석 , 그리고 Wireshark를 활용한 패킷 분석 및 방화벽, IDS/IPS 기반 네트워크 보안 기초 학습 |
| **Week 7** | ☁️ AWS 3-Tier 웹 인프라 완전 구축 | 프로덕션 수준의 완전한 3-Tier 아키텍처 구축. Multi-AZ VPC 네트워크 설계 (6개 Subnets, NAT Gateway 2개), Application Load Balancer 및 Auto Scaling Group 구성, RDS MySQL 데이터베이스 구축, Security Groups 계층별 보안 설정. 실제 구축 시간 3시간, 비용 ~$0.5로 고가용성 웹 인프라 완성 |


