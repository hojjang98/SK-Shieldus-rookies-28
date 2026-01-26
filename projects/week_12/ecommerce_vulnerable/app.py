from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key_123'  # 취약한 시크릿 키
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 메인 페이지 (상품 목록)
@app.route('/')
def index():
    conn = get_db()
    
    # SQL Injection 취약점: 검색 파라미터 직접 쿼리에 삽입
    search = request.args.get('search', '')
    if search:
        query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
        products = conn.execute(query).fetchall()
    else:
        products = conn.execute('SELECT * FROM products').fetchall()
    
    conn.close()
    return render_template('index.html', products=products)

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        
        # SQL Injection 취약점: 사용자 입력 직접 쿼리에 삽입
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = conn.execute(query).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                        (username, password, email))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            flash('Username already exists')
            conn.close()
    
    return render_template('register.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 상품 상세
@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
    
    # XSS 취약점: 댓글을 그대로 출력
    comments = conn.execute('''
        SELECT c.*, u.username FROM comments c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.product_id=?
    ''', (product_id,)).fetchall()
    
    conn.close()
    return render_template('product.html', product=product, comments=comments)

# 댓글 작성
@app.route('/product/<int:product_id>/comment', methods=['POST'])
def add_comment(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    comment = request.form['comment']
    
    conn = get_db()
    conn.execute('INSERT INTO comments (product_id, user_id, comment) VALUES (?, ?, ?)',
                (product_id, session['user_id'], comment))
    conn.commit()
    conn.close()
    
    return redirect(url_for('product', product_id=product_id))

# 장바구니
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cart_items = conn.execute('''
        SELECT c.*, p.name, p.price, p.image 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id=?
    ''', (session['user_id'],)).fetchall()
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# 장바구니 추가
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    existing = conn.execute('SELECT * FROM cart WHERE user_id=? AND product_id=?',
                           (session['user_id'], product_id)).fetchone()
    
    if existing:
        conn.execute('UPDATE cart SET quantity=quantity+1 WHERE id=?', (existing['id'],))
    else:
        conn.execute('INSERT INTO cart (user_id, product_id) VALUES (?, ?)',
                    (session['user_id'], product_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

# 프로필
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        # 파일 업로드 취약점: 파일 타입 검증 없음
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename:
                # 취약점: 파일 확장자 검증 없음
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                conn.execute('UPDATE users SET profile_image=? WHERE id=?',
                           (filename, session['user_id']))
                conn.commit()
    
    user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)