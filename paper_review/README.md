# 📄 Paper Review — 보안 분야별 논문 리뷰 모음

이 디렉토리는 **SK Shieldus 루키즈 28기 활동 중 각 보안 분야(field)** 와 관련된 핵심 논문을 직접 읽고 정리하는 공간이다.  
논문은 실무와의 연계성을 중심으로 선택하며,  
수식이 많거나 구조 분석이 필요한 경우에는 `.ipynb` 형식으로,  
요약 위주이거나 개념 정리 중심이라면 `.md` 형식으로 작성한다.

---

## 🎯 목적
- 각 보안 분야별 최신 연구를 이해하고, 실무 적용 가능성을 탐색한다.  
- 단순 요약이 아닌, **"이 논문에서 얻은 인사이트를 실제 보안 업무나 프로젝트에 어떻게 연결할 수 있을까"** 에 초점을 맞춘다.  
- 논문 이해 → 정리 → 응용 아이디어 도출의 흐름으로 구성한다.

---

## 📂 폴더 구성

```bash

- **soc/** — 보안관제 (Security Operation Center)  
  로그 기반 이상 탐지 및 SIEM 자동화 관련 논문  

- **cert/** — 침해대응 (Computer Emergency Response Team)  
  사고 대응 프로세스 및 포렌식 관련 논문  

- **pentest/** — 모의해킹 (Penetration Testing)  
  웹/시스템 취약점 공격 및 방어 관련 논문  

- **vuln_assessment/** — 취약점 진단 (Vulnerability Assessment)  
  취약점 스캐닝 및 CVSS 평가 관련 논문  

- **ot_security/** — OT/ICS 보안 (Operational Technology Security)  
  산업제어시스템(ICS) 보안 및 네트워크 이상탐지 관련 논문  

- **cloud_security/** — 클라우드 보안 (Cloud Security)  
  Zero Trust, IAM, CSP 설정 취약점 관련 논문  

- **consulting/** — 보안 컨설팅 (Security Consulting & Risk Management)  
  보안 정책, 위험 관리, 거버넌스 관련 논문  

- **si_integration/** — 보안 SI (Security Integration / Architecture)  
  통합 보안 아키텍처, 시스템 설계 관련 논문  

```

---

## 🧭 작성 원칙

1. **형식 선택은 자유**
   - 수식, 모델 구조, 실험이 포함된 논문은 `.ipynb`로 정리  
   - 개념적/서술 중심 논문은 `.md`로 정리  
   - 한 논문이라도 필요한 경우 두 형식 병행 가능 (예: md 요약 + ipynb 시각화)

2. **파일명 규칙**
   - 소문자 + 핵심 키워드 중심  
   - 예: `deeplog.md`, `zero_trust_cloud.ipynb`, `owasp_top10.md`

3. **내용 구성**
   - 논문 배경 → 제안 방법 → 주요 결과 → 실무적 시사점  
   - 논문 속 수식이나 모델 다이어그램은 가능하면 직접 재작성하지 않고 핵심 아이디어로 요약  
   - 실무 연결 가능성은 반드시 포함할 것  

---

## 🗓️ 진행 방식

| 단계 | 내용 | 산출물 |
|------|------|--------|
| ① 논문 선정 | 각 분야별 대표 논문 1편 선택 | 논문명 및 링크 |
| ② 정독 및 요약 | 논문의 핵심 구조, 모델, 결과 정리 | `.md` or `.ipynb` |
| ③ 실무 적용 아이디어 | 루키즈 프로젝트나 보안 실무 관점에서 해석 | 섹션 “실무 적용” |
| ④ 업로드 | `paper_review/[분야]/` 경로에 파일 저장 및 커밋 | 완성된 리뷰 파일 |

---

## 💬 작성 팁
- 논문 이해의 목적은 **‘암기’가 아니라 ‘응용’**이다.  
- 인용 수가 많거나 산업 적용이 활발한 논문부터 시작하자.  
- 리뷰 파일 내에는 “이 논문에서 배운 점”을 최소 3줄 이상 작성한다.  
- Markdown에서는 간결히, Notebook에서는 시각적·수식적 표현을 적극 활용한다.  

---

> ✍️ *This directory serves as a research log for SK Shieldus Rookies 28 —  
> bridging academic security studies with real-world cybersecurity practice.*
