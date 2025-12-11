# Week 7: AWS 3-Tier 웹 서비스 인프라 완전 구축

## 프로젝트 개요

본 프로젝트는 SK 쉴더스 루키즈에서 배운 지식을 가지고 개인적으로  **프로덕션 수준의 완전한 3-Tier 웹 애플리케이션 인프라**를 처음부터 끝까지 실제로 구축한 프로젝트입니다.

---

## 배경

현대의 웹 서비스는 높은 가용성, 확장성, 그리고 보안성을 동시에 요구합니다. 본 프로젝트는 중소 규모의 **전자상거래 웹사이트**를 가상의 시나리오로 설정하고, 실무에서 요구되는 완전한 3-Tier 아키텍처를 AWS에서 직접 구축했습니다.

---

## 프로젝트 목표

1. **고가용성**: Multi-AZ 구성으로 장애 발생 시에도 서비스 지속
2. **확장성**: Auto Scaling을 통한 트래픽 변동 자동 대응
3. **보안성**: 계층별 네트워크 격리 및 Security Group 적용
4. **로드 밸런싱**: Application Load Balancer를 통한 트래픽 분산
5. **실전 경험**: 완전한 3-Tier 아키텍처 구축 경험

---

## 구축된 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                         사용자 (Users)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    Application Load Balancer
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Amazon VPC (10.0.0.0/16)                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Public Subnet (Multi-AZ)                          │     │
│  │  - ALB (3a, 3b)                                    │     │
│  │  - NAT Gateway (3a, 3b)                            │     │
│  │  - Internet Gateway                                │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Private App Subnet (Multi-AZ)                     │     │
│  │  - EC2 Auto Scaling Group (2+ instances)           │     │
│  │  - web-server-1a (ap-northeast-3a)                 │     │
│  │  - web-server-1b (ap-northeast-3b)                 │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Private DB Subnet (Multi-AZ)                      │     │
│  │  - RDS MySQL                                       │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 실제 구축 리소스

### 구축 환경
- **리전**: ap-northeast-3 (Osaka)
- **구축일**: 2025년 12월 11일
- **소요 시간**: 약 3시간
- **실제 비용**: ~$0.5 (구축 후 즉시 삭제)

### 네트워크 계층
- VPC: 3tier-production-vpc (10.0.0.0/16)
- Subnets 6개 (Public 2, Private App 2, Private DB 2)
- Internet Gateway
- NAT Gateway 2개 (Multi-AZ)
- Route Tables 5개

### 보안 계층
- Security Groups 3개 (alb-sg, web-server-sg, rds-sg)
- 계층별 네트워크 격리
- 최소 권한 원칙 적용

### 컴퓨팅 계층
- Application Load Balancer (Active)
- Target Group (2 healthy targets)
- Launch Template (Amazon Linux 2023 + Nginx)
- Auto Scaling Group (Min 2, Max 4)
- EC2 Instances 2개 (Multi-AZ, t3.micro)

### 데이터베이스 계층
- RDS MySQL 8.0.35 (db.t3.micro)
- DB Subnet Group (Multi-AZ)
- Private Subnet 격리

---

## 프로젝트 구조

```bash
week7_AWS_3Tier_Infrastructure/
├── README.md                          # 프로젝트 개요
├── docs/
│   └── AWS_3Tier_완전구축_프로젝트_보고서.pdf    # 상세 기술 보고서
├── implementation/
│       ├── 01_vpc_created.png
│       ├── 02_subnets_6ea.png  
│       ├── 03_nat_gateways.png 
│       ├── 04_route_tables.png
│       ├── 05_security_groups.png 
│       ├── 06_rds_creating.png 
│       ├── 07_target_group_healthy.png 
│       ├── 08_alb_active.png   
│       ├── 09_ec2_instances_multi_az.png
│       ├── 10_auto_scaling_group.png
│       ├── 11_website_instance1.png 
│       ├── 12_vpc_resource_map.png  
└── scripts/
    └── ec2_user_data.sh            # EC2 User Data 스크립트
```

---

## 핵심 성과

### 1. Multi-AZ 고가용성 구성
- 2개 가용 영역 활용 (ap-northeast-3a, 3b)
- 모든 계층에 걸친 Multi-AZ 배포
- 자동 장애 복구 메커니즘

### 2. 자동 로드 밸런싱
- ALB를 통한 트래픽 분산
- Target Group 헬스 체크
- 2개 인스턴스 모두 Healthy
- 로드밸런싱 작동 확인

### 3. Auto Scaling 구성
- Launch Template 기반 자동 배포
- User data로 웹서버 자동 설치
- 인스턴스 장애 시 자동 교체

### 4. 계층별 보안 격리
- Public/Private Subnet 분리
- Security Groups 최소 권한
- RDS 완전 격리

---

## 학습 성과

| 영역 | 적용 내용 |
|------|----------|
| **네트워크** | VPC, Subnets, Route Tables, NAT Gateway |
| **로드 밸런싱** | ALB, Target Group, 헬스 체크 |
| **Auto Scaling** | Launch Template, ASG, Multi-AZ |
| **데이터베이스** | RDS, Subnet Group, 보안 설정 |
| **보안** | Security Groups, 네트워크 격리 |
| **고가용성** | Multi-AZ 구성, 자동 복구 |

---

## 트러블슈팅 경험

### Private Subnet 인터넷 접근 문제
- 문제: User data 스크립트 실행 실패
- 원인: NAT Gateway 라우팅 미설정
- 해결: NAT Gateway 추가 및 Route Table 설정

### Auto Scaling AZ 불균형
- 문제: 모든 인스턴스가 단일 AZ 배치
- 해결: 수동 EC2 생성 후 Target Group 등록

---

## 비용 분석

### 실제 구축 비용 (3시간)
- NAT Gateway × 2: $0.27
- ALB: $0.07
- EC2/RDS (프리티어): $0
- **총계: ~$0.5**

### 프로덕션 운영 시 (월간)
- EC2, ALB, NAT, RDS 등
- **예상: ~$325/월**

---

## 참고 자료

- AWS Well-Architected Framework
- AWS Architecture Center
- AWS 공식 문서
- SK 쉴더스 루키즈 교육 자료


