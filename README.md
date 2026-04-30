# 🛡️ SK Shieldus Rookies 28기 — Cybersecurity Study & Projects

이 리포지토리는 **SK Shieldus 루키즈 28기** 활동 기간 동안 배운 내용을 체계적으로 기록하고,  
각 분야별 학습을 기반으로 한 **실습 프로젝트**와 **논문 리뷰**를 정리하기 위한 공간입니다.

---

## 📚 Repository Overview

| 구분 | 설명 |
|------|------|
| `daily_logs/` | 교육 과정 중 매일 학습한 보안 개념, 도구, 실습 결과를 정리 |
| `projects/` | 주차(week)별로 수행하는 실습 프로젝트 모음 |
| `paper_review/` | 보안관제, 침해대응, 모의해킹 등 각 분야별 핵심 논문 리뷰 |
| `security_issues_analysis/` | 주간 보안 이슈 분석 - 최신 보안 사고 및 취약점 사례 분석 |


---

## 🧭 Learning Goals

1. **보안 실무 지식의 체계적 정리**
   - 교육 중 다루는 주요 개념·도구·프로세스를 매일 정리
2. **각 분야별 실습 프로젝트 수행**
   - 배운 내용을 기반으로 직접 문제를 정의하고, 미니 프로젝트 형태로 구현
3. **핵심 논문 리뷰 및 요약**
   - 분야별 대표 논문을 직접 읽고 정리하여 연구적 이해력 강화
4. **보안 시사 분석**
   - 주간 1~3개 최신 보안 사고/취약점 기사를 분석하여 트렌드 파악

---

## 🧩 Focus Areas

| 분야 | 설명 | 예시 프로젝트 |
|------|------|----------------|
| **SOC (보안관제)** | 로그 기반 이상행위 탐지 및 대응 프로세스 | LSTM 기반 로그 이상탐지 모델 |
| **Security Integration (SI)** | 보안 시스템 설계 및 통합 | 소규모 기업용 보안 아키텍처 설계 |
| **CERT (침해대응)** | 사고 대응 절차 및 포렌식 기초 | 랜섬웨어 대응 플레이북 설계 |
| **Security Consulting** | 리스크 분석 및 보안정책 제안 | 스타트업 대상 리스크 매트릭스 작성 |
| **Penetration Testing** | 웹 및 시스템 모의해킹 | OWASP Juice Shop 취약점 분석 |
| **Vulnerability Assessment** | 자동 스캐닝 및 CVSS 평가 | OpenVAS 기반 취약점 진단 |
| **OT/ICS Security** | 산업제어시스템 보안 | Modbus 트래픽 이상 탐지 |
| **Cloud Security** | 클라우드 보안 정책 및 IAM 설계 | AWS IAM 최소 권한 정책 구축 |

---

## 🗓️ Study Plan (구성 방식)

이 리포지토리의 학습 흐름은 **매일의 학습 정리 → 주차별 실습 프로젝트 → 분야별 논문 리뷰 → 주간 보안 이슈 분석**로 구성되어 있습니다.  
루키즈 활동 중 각 주차의 학습 내용이나 과제 주제에 따라 유동적으로 조정됩니다.

| 구성 요소 | 설명 | 예시 |
|------------|------|------|
| **Daily Log** | 교육 중 배운 개념, 실습 결과, 도구 사용법 등을 매일 정리 | 예: "2025-10-27 · ELK 기반 로그 수집 구조 이해" |
| **Field Project** | 주차별 혹은 분야별로 배운 내용을 실제로 적용한 미니 프로젝트 | 예: "Week 1 · LSTM 기반 로그 이상탐지 실습" |
| **Paper Review** | 각 분야(SOC, CERT, Pentest 등)와 연계된 핵심 논문을 선정해 읽고 요약 | 예: "DeepLog: Anomaly Detection and Diagnosis from System Logs" |
| **Security Issues Analysis** | 주간 1~3개 최신 보안 기사를 선정하여 근본 원인과 대응 방안 분석 | 예: "2025-12주차 · 쿠팡 개인정보 유출 사건 분석" |

> 💡 **진행 방식 예시:**  
> 1. 매주 초, 학습 분야(예: SOC, CERT 등)와 실습 목표를 설정  
> 2. 주중에는 Daily Log를 통해 배운 내용을 정리  
> 3. 주말에는 Field Project와 Paper Review를 마무리하여 GitHub에 업로드  
> 4. 주간 보안 이슈 1~3개를 분석하여 최신 트렌드 파악
> 5. 모든 내용은 실제 실무 감각을 키우는 방향으로 작성  

이 구조는 루키즈 과정 중 배운 내용을 단순 기록에 그치지 않고  
'이해 → 실습 → 정리 → 확장'의 순환 학습이 이루어지도록 설계되어 있습니다.

---

## 🧠 Study Methodology

> **"Learn → Apply → Review → Reflect"**  
> 배운 것을 즉시 실습으로 연결하고, 결과를 기록하며 회고한다.

| 단계 | 내용 | 산출물 |
|------|------|--------|
| Learn | 교육·논문을 통해 개념 이해 | `daily_logs/날짜.md` |
| Apply | 직접 실습 또는 프로젝트 수행 | `projects/weekXX/` |
| Review | 논문/자료 정리, 개념 재정리 | `paper_review/논문명.md` |
| Analyze | 최신 보안 사고 및 취약점 분석 | `security_issues_analysis/weekXX/` |
| Reflect | 배운 점 및 개선점 회고 | 주간 회고 로그 |

---

## 🏆 파이널 프로젝트 — 개인정보 수탁사 점검 (Week 20~24)

> **주제:** 개인정보 위·수탁 관리체계 구축 및 수탁사 현장 점검  
> **팀:** 5조 (리베로 컨설팅) · **위탁사:** 하랑항공 · **수탁사:** 6개사  
> **기간:** Week 20 ~ Week 24 (5주)

| 주차 | 주제 | 핵심 산출물 |
|------|------|-------------|
| [Week 20](projects/week_20/) | 착수 및 계획 수립 | WBS, 수행계획서, 사업제안서 초안, 수탁사 목록 |
| [Week 21](projects/week_21/) | 수탁사 분석 및 점검 계획 | 수탁사 현황(6개사), 점검계획서, 위탁계약서, 등급산정표 |
| [Week 22](projects/week_22/) | 현장 점검 실시 | 점검 체크리스트, 증적자료(6개사) |
| [Week 23](projects/week_23/) | 결과 분석 및 보고서 작성 | 점검결과보고서, 개선방안보고서, 수탁사 교육자료 |
| [Week 24](projects/week_24/) | 최종 발표 및 마무리 | 최종 PPT/PDF, 발표 진행 |

---

## 📦 Repository Structure

```bash
skshielders-rookies-28/
┣ 📂 daily_logs/
┣ 📂 projects/
┃  ┣ 📂 week_01 ~ week_19/       # 주차별 실습 프로젝트
┃  ┣ 📂 week_20/                  # [파이널] 착수·계획 수립
┃  ┣ 📂 week_21/                  # [파이널] 수탁사 분석·점검 계획
┃  ┣ 📂 week_22/                  # [파이널] 현장 점검·증적 수집
┃  ┣ 📂 week_23/                  # [파이널] 결과 보고서·개선방안
┃  ┗ 📂 week_24/                  # [파이널] 최종 발표·마무리
┣ 📂 paper_review/
┣ 📂 security_issues_analysis/
┗ README.md
```

---


## 🪄 License
This repository is intended for educational and research purposes only.  
All project implementations and datasets comply with ethical security research guidelines.