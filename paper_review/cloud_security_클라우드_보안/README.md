## Cloud Security (클라우드 보안) — 논문 리뷰

이 공간은 **클라우드 환경(IaaS, PaaS, SaaS)** 및 **클라우드 네이티브 보안(Cloud-Native Security)** 분야의 주요 논문을 분석하고 정리하기 위한 기록소입니다. 실습 위주의 학습보다는 이론적 개념 정립과 학술적 사고 확장을 목표로 하며, **공유 책임 모델(Shared Responsibility)**, **다중 테넌트 격리(Multi-tenancy Isolation)**, 그리고 **Cloud API 기반 접근 통제** 연구 흐름을 중점적으로 다룹니다.

---

### 논문 목록

* Hey, You, Get Off of My Cloud: Exploring Information Leakage in Third-Party Compute Clouds (ACM CCS 2009)

---

### 목적

* **책임 소재 규명**: 서비스 모델(IaaS, PaaS, SaaS)별 공유 책임 모델을 분석하여 보안 책임의 경계를 명확히 정의한다.
* **격리 메커니즘 분석**: 하이퍼바이저 및 컨테이너의 격리 원리를 파악하고, 측면 채널(Side-Channel) 공격 등 클라우드 환경의 근본적인 위협을 이해한다.
* **접근 통제 원리 학습**: 클라우드 기반 권한 관리(IAM)의 작동 원리를 체득하고, API 오용 및 설정 오류(Misconfiguration)로 인한 취약성을 학습한다.
* **보안 패러다임 전환**: 전통적인 경계 보안의 한계를 넘어서는 제로 트러스트(Zero Trust) 기반의 클라우드 보안 아키텍처 사고를 확립한다.

---

> 본 자료의 모든 내용은 논문을 통한 **클라우드 환경의 보안 원리 및 구조 분석**을 목적으로 합니다. 따라서 특정 클라우드 서비스 제공자(AWS, Azure, GCP 등)의 콘솔 설정이나 세부 명령어와 같은 실무적 요소는 다루지 않습니다.

