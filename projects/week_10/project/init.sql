CREATE DATABASE IF NOT EXISTS web;
USE web;

CREATE TABLE IF NOT EXISTS tb_users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    role VARCHAR(20) DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT NOW(),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tb_boards (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    writer VARCHAR(50),
    filename VARCHAR(255),
    filepath VARCHAR(500),
    read_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tb_tickets (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    result_log TEXT,
    created_at DATETIME DEFAULT NOW()
);

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

-- 초기 데이터 삽입
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