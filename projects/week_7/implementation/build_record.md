# Week 7: AWS 3-Tier Infrastructure - 구축 완료 기록

## 구축 정보

- **프로젝트명**: Week 7 - AWS 3-Tier 웹 인프라 구축
- **구축일**: 2025년 12월 10일
- **소요 시간**: 약 1시간
- **비용**: $0 (프리티어 활용 후 즉시 삭제)
- **리전**: ap-northeast-3 (오사카)
- **교육 기관**: SK 쉴더스 루키즈

---

## 구축 완료 항목

### 1. VPC 네트워크 구성
- **VPC 생성**: `3tier-vpc` (10.0.0.0/16)
- **Subnet 생성**: `public-subnet-1` (10.0.1.0/24, ap-northeast-3a)
- **Internet Gateway 연결**: `3tier-igw`
- **라우팅 테이블 설정**: 인터넷 연결 활성화 (0.0.0.0/0 → IGW)

### 2. EC2 인스턴스 배포
- **인스턴스 타입**: t2.micro (프리티어)
- **AMI**: Amazon Linux 2023
- **인스턴스 이름**: `3tier-web-server`
- **퍼블릭 IP**: 13.208.187.129 (구축 당시)
- **키 페어**: `3tier-key` (생성 및 다운로드)

### 3. 보안 구성
- **보안 그룹**: `3tier-web-sg`
- **인바운드 규칙**:
  - HTTP (80): 0.0.0.0/0 (전체 허용)
  - SSH (22): 특정 IP만 허용

### 4. 웹서버 구축
- **웹서버**: Nginx
- **설치 방법**: SSH 수동 설치 (User Data 스크립트 미실행)
- **웹 페이지**: AWS 3-Tier Infrastructure 소개 페이지 배포
- **접속 확인**: http://13.208.187.129 정상 작동

---

## 구축 증빙 자료

### 스크린샷 목록

본 프로젝트의 실제 구축 과정을 증명하는 스크린샷 4장:

**1. VPC 생성 완료** (`screenshots/01_vpc_created.png`)
- VPC 대시보드에서 VPC, Subnet, Internet Gateway, Route Table 생성 확인
- VPC ID, CIDR 블록 (10.0.0.0/16) 표시
- 네트워크 구성 완료 상태

**2. EC2 인스턴스 실행 중** (`screenshots/02_ec2_running.png`)
- EC2 인스턴스 목록에서 `3tier-web-server` 실행 중 확인
- 인스턴스 상태: Running (초록색)
- 상태 검사: 2/2 checks passed
- 퍼블릭 IPv4 주소: 13.208.187.129

**3. 웹사이트 접속 성공** (`screenshots/03_website_live.png`)
- 브라우저에서 http://13.208.187.129 접속 화면
- AWS 3-Tier Infrastructure 페이지 정상 표시
- 시스템 상태: Operational
- 프로젝트 정보 표시

**4. 보안 그룹 규칙** (`screenshots/04_security_groups.png`)
- `3tier-web-sg` 보안 그룹 인바운드 규칙 확인
- HTTP (80): 0.0.0.0/0
- SSH (22): 특정 IP

---

## 구축 과정 요약

### Phase 1: 네트워크 구성 (10분)
1. VPC 생성 (10.0.0.0/16, 이름: 3tier-vpc)
2. Public Subnet 생성 (10.0.1.0/24, AZ: ap-northeast-3a)
3. Internet Gateway 생성 및 VPC 연결
4. 라우팅 테이블 설정 (0.0.0.0/0 → IGW)
5. Subnet 연결

### Phase 2: 컴퓨팅 리소스 배포 (20분)
1. EC2 인스턴스 시작 (t2.micro, Amazon Linux 2023)
2. 키 페어 생성 (3tier-key) 및 다운로드
3. 네트워크 설정 (VPC, Subnet, 퍼블릭 IP 자동 할당)
4. 보안 그룹 생성 (HTTP 80, SSH 22)
5. User Data 스크립트 입력 (실행 실패)
6. 인스턴스 시작 및 실행 확인

### Phase 3: 웹서버 구성 (15분)
1. SSH 접속 (ssh -i 3tier-key.pem ec2-user@13.208.187.129)
2. Nginx 수동 설치
   ```bash
   sudo yum update -y
   sudo yum install nginx -y
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```
3. HTML 페이지 생성 및 배포
4. 브라우저 접속 테스트 (http://13.208.187.129)
5. 정상 작동 확인

### Phase 4: 검증 및 정리 (15분)
1. 웹사이트 접속 최종 확인
2. 보안 그룹 규칙 검증
3. 스크린샷 4장 촬영
   - VPC 대시보드
   - EC2 인스턴스 목록
   - 웹사이트 접속 화면
   - 보안 그룹 규칙
4. 리소스 삭제
   - EC2 인스턴스 종료
   - VPC 삭제

---

## 구현 범위 및 제약사항

### 프로젝트 목표

본 프로젝트는 **설계 역량 강화 및 핵심 개념 검증**을 목표로 하는 교육 프로젝트입니다.

### 설계 범위 (완전한 3-Tier 아키텍처)

프로덕션 수준의 완전한 아키텍처를 설계했습니다:
- Multi-AZ VPC (Public/Private/Database Subnet)
- Application Load Balancer + Auto Scaling
- RDS Multi-AZ + ElastiCache
- S3 + CloudFront CDN
- WAF + IAM 보안 구성
- CloudWatch 모니터링

**설계 산출물:**
- 기술 문서 작성
- 네트워크 구성도
- 보안 설계
- 비용 분석 ($318/월)

### 실제 구현 범위 (핵심 검증)

설계한 아키텍처의 핵심 개념을 실제로 구현하여 검증했습니다:
- VPC 네트워크 구성 (Single-AZ, Public Subnet)
- Subnet 및 라우팅 설정
- EC2 인스턴스 배포 (단일 인스턴스)
- 보안 그룹 설정
- 웹서버 운영

**구현 목적:**
- AWS 콘솔 실습 경험
- 설계한 네트워크 구성의 실제 작동 확인
- 보안 정책 적용 검증
- 클라우드 리소스 관리 경험

### 제약 사항 및 판단 근거

**교육 목적:**
본 프로젝트의 핵심 목표는 "AWS 클라우드 아키텍처 설계 역량 강화"입니다. 완전한 설계 문서를 작성함으로써 프로덕션 환경의 요구사항을 이해하고, 실제 구현을 통해 AWS 서비스의 작동 방식을 체득했습니다.

**비용 효율:**
- 프리티어 범위 내 학습
- 실습 후 즉시 리소스 삭제
- 실제 비용 $0 달성

**학습 효과:**
완전한 구현(RDS, ALB, NAT Gateway 등)은 동일한 개념의 반복이며, 본 교육 과정의 목표인 "클라우드 인프라 설계 및 구축 이해"는 현재 범위로 충분히 달성했습니다.

---

## 구축 과정에서 배운 점

### 기술적 인사이트

**1. VPC 네트워크 구성**
- VPC CIDR 블록 설계의 중요성
- Internet Gateway와 라우팅 테이블의 관계
- Public/Private Subnet 개념 이해
- 가용 영역(AZ) 선택의 의미

**2. EC2 인스턴스 관리**
- 인스턴스 유형 선택 (프리티어 고려)
- 보안 그룹의 방화벽 역할
- 키 페어를 통한 SSH 인증
- 인스턴스 상태 확인 방법

**3. 웹서버 운영**
- Nginx 설치 및 설정
- 정적 콘텐츠 배포 방법
- SSH를 통한 원격 관리
- 시스템 서비스 관리 (systemctl)

**4. 문제 해결 능력**
- User Data 스크립트 미실행 문제 진단
- Amazon Linux 2023 명령어 차이 파악
- 수동 설치로 대안 마련
- 트러블슈팅 프로세스 경험

**5. 비용 관리**
- 프리티어 활용 전략
- 리소스 사용 후 즉시 삭제의 중요성
- 실제 비용 $0 달성

### 실무 적용 가능성

이번 실습을 통해 구축한 기본 인프라는 다음과 같이 확장 가능:
- Private Subnet 추가로 애플리케이션 계층 분리
- RDS 추가로 데이터 계층 구성
- Auto Scaling 그룹으로 고가용성 확보
- Application Load Balancer로 트래픽 분산
- CloudWatch로 모니터링 체계 구축

---

## 비용 분석

### 실제 구현 비용

| 항목 | 사양 | 월간 비용 |
|------|------|----------|
| EC2 t2.micro | 프리티어 750시간 | $0 |
| VPC | 기본 제공 | $0 |
| 데이터 전송 | 최소 사용량 | $0 |
| **총계** | | **$0** |

**참고:** 실습 완료 후 약 1시간 이내에 모든 리소스를 삭제하여 비용 발생을 완전히 방지했습니다.

### 완전 구현 시 예상 비용 (설계 기준)

| 서비스 | 사양 | 월간 비용 |
|--------|------|----------|
| EC2 (t3.medium × 2) | Multi-AZ | $60 |
| Application Load Balancer | | $25 |
| RDS MySQL (db.t3.medium) | Multi-AZ | $120 |
| NAT Gateway | 2개 | $45 |
| ElastiCache (Redis) | | $25 |
| S3 + CloudFront | | $88 |
| **총계** | | **$318/월** |

---

## 성과 요약

### 달성한 목표
- AWS 클라우드 아키텍처 설계 능력 함양
- VPC 네트워크 구성 경험
- EC2 인스턴스 생성 및 관리
- 보안 그룹 설정 및 검증
- 웹서버 설치 및 배포
- 실제 작동하는 웹 인프라 구축
- 구축 과정 문서화
- 비용 관리 (프리티어 활용, $0)

### 학습 성과
- 클라우드 인프라의 실제 구축 경험
- AWS 콘솔 사용법 숙지
- 네트워크 보안 개념 적용
- Linux 서버 관리 실습
- 문제 해결 능력 향상
- 기술 문서 작성 능력
- 비용 대비 효과적인 학습 달성

---

## 참고 자료

- **설계 문서**: `docs/AWS_3Tier_인프라_구축_가이드.docx` - 완전한 아키텍처 설계
- **구축 절차**: `implementation/SETUP_GUIDE.md` - 단계별 구축 절차 기록
- **웹서버 스크립트**: `scripts/setup_webserver.sh` - 웹서버 설치 스크립트
- **웹 애플리케이션**: `app/index.html` - 배포한 웹 페이지
- **증빙 자료**: `implementation/screenshots/` - 구축 과정 스크린샷 4장

---

## 결론

본 프로젝트를 통해 AWS 클라우드 환경에서 프로덕션 수준의 3-Tier 아키텍처를 설계하고, 핵심 구성요소를 실제로 구축하여 클라우드 인프라의 작동 원리를 체득했습니다.

완전한 설계 문서 작성을 통해 실무에서 요구되는 아키텍처 설계 능력을 함양했으며, 실제 구축을 통해 AWS 서비스의 통합 방식과 운영 방법을 학습했습니다.

특히 비용과 학습 효과를 고려한 합리적인 범위 설정을 통해, 실무에서 중요한 기술적 의사결정 능력도 향상시킬 수 있었습니다.
