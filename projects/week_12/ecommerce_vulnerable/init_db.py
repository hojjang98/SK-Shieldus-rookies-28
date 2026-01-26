import sqlite3

def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Users 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT,
        profile_image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Products 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER DEFAULT 0,
        image TEXT
    )
    ''')
    
    # Cart 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')
    
    # Orders 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_price REAL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Comments 테이블 (XSS 취약점용)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        user_id INTEGER,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # 테스트 데이터 삽입
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
                   ('admin', 'admin123', 'admin@shop.com'))
    
    products = [
        ('노트북', '고성능 게이밍 노트북', 1500000, 10, 'laptop.jpg'),
        ('무선마우스', '인체공학적 무선마우스', 35000, 50, 'mouse.jpg'),
        ('키보드', '기계식 RGB 키보드', 120000, 30, 'keyboard.jpg'),
        ('모니터', '27인치 4K 모니터', 450000, 15, 'monitor.jpg'),
        ('헤드셋', '게이밍 헤드셋', 80000, 25, 'headset.jpg')
    ]
    
    for product in products:
        cursor.execute('''
        INSERT OR IGNORE INTO products (name, description, price, stock, image) 
        VALUES (?, ?, ?, ?, ?)
        ''', product)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == '__main__':
    init_database()