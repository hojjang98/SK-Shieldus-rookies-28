# Rookies Vulnerable Web App

이 프로젝트는 **주요정보통신기반시설 기술적 취약점 분석·평가** 실습을 목적으로 제작된 테스트용 웹 애플리케이션입니다.

교육 및 실습을 위해 의도적으로 다양한 보안 취약점을 포함하고 있습니다.

> ** 경고 (WARNING)**
>
> 이 소프트웨어는 **심각한 보안 취약점**을 포함하고 있습니다.
> * 절대로 실제 운영 환경(Production)이나 공용 네트워크에 배포하지 마십시오.
> * 반드시 외부와 차단된 로컬 환경(Localhost) 또는 폐쇄망에서만 실행하십시오.
> * 이 프로그램을 이용한 불법적인 해킹 행위의 책임은 사용자 본인에게 있습니다.

---

## 사전 요구사항 (Prerequisites)

이 프로젝트를 실행하기 위해 다음 도구들이 설치되어 있어야 합니다.

* **Spring Boot 3.5.9**
* **Java 21 이상 (JDK 21)**
* **Docker Desktop** (MariaDB 컨테이너 실행용)
* **IntelliJ IDEA Community**
* **Git** (선택 사항)

---

## 설치 및 실행 가이드 (Installation)

데이터베이스를 구축하고 애플리케이션을 실행하는 방법입니다.

### 1. 데이터베이스 초기화 스크립트 작성

프로젝트 최상위 경로(루트 폴더)에 `init.sql` 파일이 없다면 파일을 생성하고 아래 내용을 붙여넣으세요.
(이 스크립트는 컨테이너 실행 시 자동으로 데이터베이스와 테이블, 초기 데이터를 생성합니다.)

**파일명:** `init.sql`

```sql
CREATE DATABASE IF NOT EXISTS web;
USE web;

CREATE TABLE IF NOT EXISTS tb_user_profile (
    user_id BIGINT PRIMARY KEY,
    birth_date DATE,
    phone VARCHAR(30),
    address VARCHAR(255),
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW()
);

CREATE TABLE IF NOT EXISTS tb_family_relations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    relation_type VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_dna_app_status (
    board_id BIGINT PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT '접수',
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW()
);

CREATE TABLE IF NOT EXISTS tb_dna_results (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    board_id BIGINT NOT NULL,
    category VARCHAR(30) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- 초기 데이터 
INSERT IGNORE INTO tb_users (username, password, nickname, email, role)
VALUES
('admin', 'admin1234', '관리자', 'admin@test.com', 'admin'),
('guest', 'guest', '방문자', 'guest@test.com', 'user');

INSERT IGNORE INTO tb_user_profile (user_id, birth_date, phone, address)
SELECT u.id, '1990-01-01', '010-0000-0000', '서울특별시 (샘플 주소)'
FROM tb_users u
WHERE u.username = 'admin';

INSERT IGNORE INTO tb_user_profile (user_id, birth_date, phone, address)
SELECT u.id, '1996-05-15', '010-1111-2222', '경기도 (샘플 주소)'
FROM tb_users u
WHERE u.username = 'guest';

INSERT IGNORE INTO tb_family_relations (user_id, relation_type, name, birth_date)
SELECT u.id, '부모', '홍길동', '1965-03-20'
FROM tb_users u
WHERE u.username = 'guest';

INSERT IGNORE INTO tb_family_relations (user_id, relation_type, name, birth_date)
SELECT u.id, '자녀', '홍가영', '2020-09-10'
FROM tb_users u
WHERE u.username = 'guest';

INSERT IGNORE INTO tb_boards (title, content, writer, read_count)
VALUES (
  '검사 신청 안내',
  'DNA 검사 신청은 ''DNA 검사 신청'' 메뉴에서 진행할 수 있습니다.<br>검사 결과는 ''검사 결과 조회''에서 확인하세요.',
  'admin',
  0
);

INSERT IGNORE INTO tb_dna_app_status (board_id, status)
SELECT b.id, '접수'
FROM tb_boards b;

INSERT IGNORE INTO tb_tickets (subject, result_log)
VALUES
('검사 진행 문의', '검사 상태 확인 요청'),
('결과 재발급 요청', 'PDF 재발급 요청');
```

### 2. MariaDB 실행 (Docker)
터미널(CMD, PowerShell 등)을 열고 init.sql 파일이 있는 위치에서 아래 명령어를 실행하여 DB를 띄웁니다.

Windows (PowerShell)
```sh
docker run -d --name rookies-db `
  -p 3306:3306 `
  -e MARIADB_ROOT_PASSWORD=9999 `
  -e MARIADB_DATABASE=web `
  -e TZ=Asia/Seoul `
  -v ${PWD}/init.sql:/docker-entrypoint-initdb.d/init.sql `
  mariadb:latest `
  --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

### 3. 애플리케이션 설정 확인
src/main/resources/application.yaml 파일의 설정이 자신의 환경과 맞는지 확인합니다.

```yaml
spring:
  datasource:
    url: jdbc:mariadb://localhost:3306/web
    username: root
    password: 9999  # Docker 실행 시 설정한 비밀번호

file:
  # [중요] 파일 업로드 경로 (해당 폴더는 앱 시작 시 자동 생성됨)
  # Mac/Linux 사용자는 /tmp/upload/ 등으로 변경 필요
  upload-dir: C:/rookies/upload/
```

### 4. 애플리케이션 실행
IntelliJ IDEA: RookiesApplication.java 파일 실행 (Run)

### 5. 실습 가능한 취약점 
1. SQL Injection (SQL 삽입)
    - 위치: 로그인 페이지 (/login), 게시판 검색창 (/board/list)

    - 설명: MyBatis 매퍼 XML에서 #{} 대신 ${}를 사용하여 사용자 입력값이 쿼리문에 그대로 결합됨.

    - 실습: - 로그인 ID에 admin' or 1=1 # 입력 시 비밀번호 없이 관리자 권한으로 로그인 성공.

    - 게시판 검색어에 ' UNION SELECT ... 구문 입력하여 DB 정보 탈취.

2. OS Command Injection (운영체제 명령어 삽입)
    - 위치: 관리자 서버 점검 페이지 - Ping 테스트 (/admin/system, /admin/system/ping)

    - 설명: Runtime.getRuntime().exec() 실행 시 사용자가 입력한 IP 주소(target)에 대한 검증 없이 cmd.exe 명령어로 전달됨.

    - 실습: IP 입력란에 127.0.0.1 & dir 또는 127.0.0.1 & calc.exe 입력 시 서버의 파일 목록 출력 또는 계산기 실행.

3. Stored XSS (저장형 크로스 사이트 스크립트)
    - 위치: 게시글 작성 (/board/write) 및 상세 조회 (/board/view)

    - 설명: 게시글 본문(content) 저장 및 출력 시 HTML 태그에 대한 이스케이프(Escape) 처리가 되어 있지 않음.

    - 실습: 본문에 <script>alert('Hacked')</script> 작성 후 저장 시, 해당 글을 열람하는 모든 사용자의 브라우저에서 스크립트 실행.

4. Unrestricted File Upload (파일 업로드 취약점)
    - 위치: 게시글 작성 시 파일 첨부 (/board/write)

    - 설명: 파일 업로드 시 확장자나 파일 타입에 대한 검증 로직이 없어 실행 가능한 웹 쉘(JSP 등) 업로드 가능.

    - 실습: cmd.jsp와 같은 웹 쉘 파일을 업로드한 뒤, /admin/system에서 접근하여 command injection을 통해 원격에서 서버 제어.

5. Path Traversal (경로 조작 및 파일 다운로드)
    - 위치: 자료실 조회 (/libs/archive)

    - 설명: 파일 경로 생성 시 ../와 같은 상위 디렉터리 이동 문자를 필터링하지 않아, 지정된 업로드 폴더 밖의 시스템 파일에 접근 가능.

    - 실습: 다운로드 요청 시 파라미터를 ?path=../../../ 등으로 조작하여 서버 파일 시스템 접근.

6. Broken Access Control (취약한 접근 제어 & 쿠키 변조)
    - 위치: 관리자 페이지 (/admin/system)

    - 설명: 세션 검증 없이 오직 클라이언트 측 Cookie: role=admin 값만 확인하여 관리자 페이지 접근을 허용함.

    - 실습: 브라우저 개발자 도구(F12)에서 role 쿠키 값을 user에서 admin으로 수정 후 새로고침하여 관리자 페이지 뚫기.

7. Format String Vulnerability (포맷 스트링 취약점)
    - 위치: IT 지원 티켓 생성 (/support/ticket)

    - 설명: String.format() 함수 사용 시 사용자의 입력값(subject)을 포맷 문자열 패턴으로 인식하게 하여 에러 유발 또는 메모리 참조 가능.

    - 실습: - %x 입력 시 System Error 발생 (DoS 시도).

    - %2$s 입력 시 서버 메모리에 숨겨진 SECRET_KEY 값 노출.

8. CSRF (사이트 간 요청 위조)
    - 위치: 마이페이지 개인정보 수정 (/user/update)

    - 설명: 정보 수정 요청 시 CSRF 토큰 검증이나 비밀번호 재확인 절차가 없음.

    - 실습: 공격자가 만든 가짜 페이지(버튼)를 로그인된 사용자가 클릭하게 하여, 사용자 몰래 비밀번호나 이메일을 강제로 변경시킴.