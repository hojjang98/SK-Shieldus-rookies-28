import sqlite3

def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 사용자 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'user'
    )
    ''')
    
    # 게시판 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 파일 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        uploader TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 기본 사용자 데이터 삽입
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('admin', 'admin123', 'admin@test.com', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('user1', 'password1', 'user1@test.com', 'user'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('testuser', 'test123', 'test@test.com', 'user'))
    
    # 기본 게시글 데이터
    cursor.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)",
                   ('Welcome Post', 'This is a test post', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)",
                   ('Security Notice', 'Please keep your password safe', 'admin'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
