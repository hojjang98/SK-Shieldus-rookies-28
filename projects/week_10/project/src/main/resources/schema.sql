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
