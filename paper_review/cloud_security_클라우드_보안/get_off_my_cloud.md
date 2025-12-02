# Research Review: Hey, You, Get Off of My Cloud: Exploring Information Leakage in Third-Party Compute Clouds
> **Analyzed Date:** 2025.12.01
> **Keywords:** Cross-Tenant, Side-Channel_Attack, Hypervisor_Isolation, Multi-tenancy, Co-residency
> **Source:** ACM CCS 2009 (Computer and Communications Security) [Full Text Link](https://rist.tech.cornell.edu/papers/cloudsec.pdf)

---

## Day 1 – Research Context & Motivation
*(클라우드 다중 테넌트 환경에서의 격리(Isolation) 붕괴 위협)*

### 1. 연구 배경: 클라우드 격리의 약속과 신뢰 문제
* **다중 테넌트 환경 (Multi-tenancy):** 클라우드 컴퓨팅의 핵심은 다수의 독립적인 고객(테넌트)이 동일한 물리적 인프라(CPU, RAM, 네트워크)를 공유하며 리소스를 효율적으로 사용하는 데 있습니다.
* **격리 원칙 (Isolation Principle):** 클라우드 서비스 제공자(CSP)는 하이퍼바이저(Hypervisor)를 통해 각 고객의 가상 머신(VM)이 완벽하게 분리되어 상호 간섭이 불가능함을 보장했습니다. 이 **가상화 기반 격리**가 클라우드 보안의 근본적인 신뢰 요소였습니다.
* **연구 문제의식:** 이처럼 강력하게 보장된 논리적 격리에도 불구하고, **공유되는 물리적 자원**을 통해 악의적인 테넌트가 다른 테넌트의 정보를 엿볼 수 있는 **근본적인 위협**이 존재하는가?

### 2. 핵심 위협: 측면 채널 공격 (Side-Channel Attack)
본 논문은 측면 채널 공격(Side-Channel Attack)을 통해 논리적 격리의 취약성을 입증합니다.

* **정의:** 시스템의 주요 입출력 경로(Main Channel)가 아닌, 물리적 구현 과정에서 발생하는 부수적인 정보(Side Channel)를 측정하여 데이터를 유출하는 공격 기법.
* **클라우드에서의 측면 채널:** 공격자가 물리적으로 공유되는 CPU의 캐시(CPU Cache)나 RAM 접근 시간을 측정하여, 같은 물리 서버에 있는 타겟 VM의 암호화 작업(Cryptographic Operation) 패턴이나 입력 행위를 모니터링할 수 있음을 제시합니다.

### 3. 공격의 2단계 구조: Co-residency와 Leakage

본 연구는 공격 성공을 두 가지 단계로 분리하여 정의합니다.

#### A. Co-residency Detection (동일 물리 서버 확인)
* **목표:** 공격자 VM이 타겟 VM과 **동일한 물리적 서버(Physical Host)** 위에서 실행되고 있는지 확인하는 것.
* **기술:** 공격자가 클라우드 환경에서 VM을 생성할 때, 네트워크 레이턴시(지연 시간) 분석이나, CPU의 **캐시 라인(Cache Line)** 경쟁을 유발하여 응답 시간을 측정하는 방식으로 타겟 VM의 '물리적 이웃' 여부를 확인합니다.

#### B. Cross-VM Information Leakage (정보 유출)
* **목표:** Co-residency가 확인된 후, **공유 캐시**의 사용 패턴을 측정하여 타겟 VM 내부의 민감한 정보(예: 암호화 키, 사용자 입력)를 추론하는 것.

### 4. 연구의 주요 기여 및 파급 효과
* **클라우드 보안 신뢰성 재평가:** CSP가 보장하는 하이퍼바이저 격리가 완벽하지 않으며, **공유 자원 관리**가 클라우드 보안의 가장 취약한 경계임을 입증했습니다.
* **산업적 변화 촉발:** 이 연구는 클라우드 벤더들에게 하이퍼바이저 설계, VM 배치 전략(VM Scheduling), 그리고 캐시 자원 관리 방식을 근본적으로 재고하도록 촉발한 전환점(Turning Point)이 되었습니다.

### 5. 개인 인사이트 (Personal Insight)
클라우드 보안의 복잡성은 Zero Trust나 IAM(접근 통제) 같은 논리적 문제뿐 아니라, **물리적인 CPU 레벨의 격리 문제**에서 기인한다는 점을 명확히 이해해야 한다. 이 논문은 논리적 방어가 아무리 잘 되어 있어도, 물리적 자원을 공유하는 한 **항상 '측면'이 뚫릴 수 있다**는 근본적인 경고를 담고 있다. Day 1의 목표는 클라우드 보안의 초점이 API 관리를 넘어 '하드웨어 레벨의 심층 방어'까지 확장되어야 함을 확인하는 것이다.

# Research Review: Hey, You, Get Off of My Cloud: Exploring Information Leakage in Third-Party Compute Clouds
> **Analyzed Date:** 2025.12.02
> **Keywords:** Co-residency_Detection, Cache_Side_Channel, Prime+Probe, Cloud_Cartography
> **Source:** ACM CCS 2009 (Computer and Communications Security) [Full Text Link](https://rist.tech.cornell.edu/papers/cloudsec.pdf)

---

## Day 2 – Core Attack Mechanism (공격 핵심 메커니즘)
*(공격 성공의 두 단계: Co-residency 확보 및 Side-Channel 이용)*

### 1. 공격 모델 및 가정 (Threat Model)
본 논문은 매우 현실적인 공격 모델을 사용한다.
* **공격자 위치:** 악의적인 행위자가 CSP에 등록된 일반 고객(다른 테넌트)이다.
* **공격 목표:** 타겟 VM과 동일한 물리적 서버에 VM을 배치하고, 공유되는 물리 자원을 이용해 정보를 유출한다.
* **제한 사항:** 공격자는 하이퍼바이저나 VM 모니터의 취약점을 이용하지 않으며, CSP의 관리자 권한을 획득하지 않는다. **오직 정상적인 클라우드 API 호출 및 자원 측정**만을 이용한다.

### 2. 단계 1: Co-residency Detection (동일 물리 서버 확인)
공격의 첫 번째이자 가장 어려운 단계는 타겟 VM과 **물리적으로 동일한 호스트**에 배치되는 것이다. 논문은 이를 위한 여러 기술을 제시한다.

#### A. 네트워크 근접성 분석 (Network Proximity)
* **원리:** 동일 물리 서버에 있는 두 VM 간의 네트워크 왕복 시간(RTT)은 매우 짧고(일반적으로 수십 마이크로초, µs 이하), 외부 네트워크상의 VM과 비교하여 확연히 낮은 값을 보인다.
* **활용:** 공격자가 자신의 VM에서 타겟 VM으로 패킷을 보내 RTT를 측정하여 물리적 이웃 여부를 신속하게 판단한다.

#### B. 클라우드 지도 제작 (Cloud Cartography)
* **기술:** 공격자가 수많은 인스턴스를 실행하고 이들의 내부 IP 주소 및 배치 정보를 체계적으로 수집하여 **클라우드 인프라의 내부 구조를 유추**한다. (Amazon EC2의 경우, 특정 IP 주소 범위가 물리적 랙이나 서버 그룹과 관련됨을 파악)
* **결과:** 이 지도를 활용하여 타겟 VM 근처의 IP 범위를 예측하고 해당 범위에 집중적으로 인스턴스를 요청할 수 있게 된다.

#### C. 배치 국소성 악용 (Placement Locality)
* **개념:** CSP의 VM 스케줄러가 리소스 활용을 극대화하기 위해, 새로 켜지는 인스턴스를 기존 인스턴스 근처(동일 물리 서버)에 배치하는 경향이 있음을 악용한다. 이는 **무차별 대입(Brute Force)** 전략의 성공률을 높인다.

### 3. 단계 2: Cross-VM Information Leakage (VM 간 정보 유출)
Co-residency가 확인되면, 공격자는 **공유 CPU 캐시**를 이용해 정보 유출 공격을 실행한다.

#### A. 캐시 기반 측면 채널 (Cache-based Side Channel)
* **공유 자원:** 현대 CPU의 **L2/L3 캐시(Cache)**는 동일 물리 서버에서 실행되는 모든 VM이 공유하는 물리적 자원이다.
* **원리:** 캐시 접근 시간은 메모리 접근 시간보다 훨씬 빠르다. 공격자는 타겟 VM의 캐시 사용 패턴 변화를 측정하여, 타겟 VM 내부에서 어떤 연산이 일어나는지 추론한다.

#### B. Prime+Probe 기법 (프라임+프로브)
이 논문에서 핵심적으로 사용된 기법이다.
1.  **Prime (점령):** 공격자 VM이 공유 캐시의 특정 영역(Cache Set)을 자신의 데이터로 가득 채운다.
2.  **Victim Access (타겟 연산):** 타겟 VM이 암호화 연산(예: RSA, AES)을 수행한다. 이 과정에서 타겟이 사용하는 비밀 키(Secret Key)에 따라 메모리 접근 패턴이 결정되고, 이 패턴에 해당하는 캐시 라인이 공격자의 데이터를 **축출(Evict)** 시킨다.
3.  **Probe (측정):** 공격자가 자신이 Prime 했던 데이터를 다시 접근하여 걸린 시간을 측정한다.
    * **접근이 느린 경우:** 타겟 VM이 캐시를 사용해 데이터를 축출했다는 의미 → **특정 연산(비밀 키에 관련된)**이 일어났음을 추론.
    * **접근이 빠른 경우:** 타겟 VM이 캐시를 사용하지 않았다는 의미.
* **공격 예시:** 논문은 이 기법을 이용해 **AES 암호화 키**를 65밀리초(ms) 만에 추출할 수 있음을 실험적으로 증명했다.

### 4. 개인 인사이트 (Personal Insight)
Day 2 분석을 통해, 클라우드 환경에서 **논리적 방어벽(Hypervisor)**이 완벽하게 작동하더라도 **물리적 공유 자원**이 존재하면 격리가 붕괴될 수 있다는 점을 실감했다. 이 논문 이후 CSP들이 **VM 배치 알고리즘**과 **하드웨어 캐시 관리**에 막대한 투자를 하게 된 배경을 이해할 수 있었다. 보안 컨설팅 시, **하드웨어 레벨의 보안 보증(Hardware-Assisted Security)**을 확인하는 것의 중요성을 인지해야 한다.