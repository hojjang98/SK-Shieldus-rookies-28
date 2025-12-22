# Paper Review — 보안 분야별 논문 리뷰 모음

이 디렉토리는 **SK Shieldus 루키즈 28기 활동 중 각 보안 분야별 핵심 논문**을 직접 읽고 정리하는 공간이다.  
논문은 실무와의 연계성을 중심으로 선택하며, 단순 요약을 넘어 **실무 적용 가능성**에 초점을 맞춘다.

---

## 왜 논문 리뷰를 시작했는가

**문제 인식:**  
루키즈 과정을 시작하며 다른 동기들에 비해 보안 도메인 지식이 부족하다는 것을 깨달았다.

**해결 전략:**  
보안 지식 격차를 메우기 위해 **이론과 실무를 병행하는 학습 방법**을 설계했다.
- **실전 감각:** 주간 보안 시사 3건 분석 (What happened? Why? How to prevent?)
- **이론 깊이:** 주 1편 논문 리뷰 (근본 원리 이해)
- **지식 구조화:** GitHub 문서화를 통한 학습 검증 및 공유

**기대 효과:**  
단순히 "많이 안다"가 아닌, **"왜 그런지 설명할 수 있고, 실무에 적용할 수 있는"** 보안 전문가로 성장하기 위함이다.

---

## 학습 로드맵

### Week 1-8: 도메인 탐색 (Domain Exploration)
8개 보안 분야별로 각 1편의 대표 논문을 읽으며 **나에게 맞는 분야**를 탐색했다.
- 보안 컨설팅
- 침해대응 (CERT)
- 모의해킹 (Penetration Testing)
- 취약점 진단
- OT/ICS 보안
- 클라우드 보안
- 보안 SI
- **보안관제 (SOC)** ← 최종 선택

### Week 9 이후: SOC 집중 심화 (SOC Deep Dive)
8주간의 도메인 탐색 결과, **SOC(Security Operations Center)** 가 나의 강점과 흥미에 가장 부합함을 확인했다.  
**Week 9부터는 SOC 관련 논문을 집중적으로 읽으며 전문성을 심화**한다.

---

## 폴더 구성
```bash
paper_review/
├── consulting/          # 보안 컨설팅 (Security Consulting & Risk Management)
├── cert/               # 침해대응 (Computer Emergency Response Team)
├── pentest/            # 모의해킹 (Penetration Testing)
├── vuln_assessment/    # 취약점 진단 (Vulnerability Assessment)
├── ot_security/        # OT/ICS 보안 (Operational Technology Security)
├── cloud_security/     # 클라우드 보안 (Cloud Security)
├── si_integration/     # 보안 SI (Security Integration / Architecture)
└── soc/                # 보안관제 (Security Operations Center) ⭐ Week 9 이후 집중
```