# ☁️ Cloud Security (클라우드 보안) — 논문 리뷰

이 폴더는 **클라우드 환경(IaaS, PaaS, SaaS)** 및 **클라우드 네이티브 보안(Cloud-Native Security)** 분야의 주요 논문을 읽고 정리하기 위한 공간이다.
실습보다는 개념 이해와 사고 확장을 목표로 하며,
**공유 책임 모델(Shared Responsibility)**, **다중 테넌트 격리(Multi-tenancy Isolation)**, 그리고 **Cloud API 기반 접근 통제** 연구 흐름을 중심으로 다룬다.

---

## 📚 논문 목록

- Hey, You, Get Off of My Cloud: Exploring Information Leakage in Third-Party Compute Clouds (ACM CCS 2009)

---

## 🧠 목적

- 공유 책임 모델(Shared Responsibility Model)을 서비스 모델(IaaS, PaaS, SaaS)별로 정확히 이해하고 보안 책임의 경계를 명확히 한다.
- 하이퍼바이저 및 컨테이너 격리 메커니즘을 분석하고, 측면 채널(Side-Channel)과 같은 근본적인 위협을 이해한다.
- 클라우드 기반 접근 통제(IAM)의 원리와 API 오용 및 잘못된 설정(Misconfiguration)의 위험성을 학습한다.
- 전통적인 경계 보안을 넘어선 Zero Trust 기반의 클라우드 보안 아키텍처 사고를 확립한다.

---

> 📌 이 폴더의 모든 내용은 논문을 통한 **클라우드 환경의 보안 원리 및 구조 분석**을 목적으로 하며,
> 특정 클라우드 벤더(AWS, Azure 등)의 콘솔 설정이나 상세 명령어는 포함하지 않는다.