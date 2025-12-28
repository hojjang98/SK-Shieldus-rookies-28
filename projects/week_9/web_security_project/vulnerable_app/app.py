from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key_123'  # 취약: 하드코딩된 시크릿 키
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 홈페이지
@app.route('/')
def index():
    return render_template('index.html')

# 로그인 (SQL Injection 취약)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 취약: SQL Injection 가능
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                         (username, password, email))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    
    return render_template('register.html')

# 대시보드
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# 게시판 (XSS 취약)
@app.route('/board')
def board():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('board.html', posts=posts)

# 게시글 작성 (XSS 취약)
@app.route('/board/write', methods=['GET', 'POST'])
def write_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db()
        cursor = conn.cursor()
        # 취약: XSS 방어 없음
        cursor.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
                     (title, content, session['username']))
        conn.commit()
        conn.close()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('board'))
    
    return render_template('write_post.html')

# 검색 (SQL Injection 취약)
@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    conn = get_db()
    cursor = conn.cursor()
    # 취약: SQL Injection 가능
    search_query = f"SELECT * FROM posts WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
    cursor.execute(search_query)
    results = cursor.fetchall()
    conn.close()
    
    return render_template('search.html', results=results, query=query)

# 파일 업로드 (File Upload 취약)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        # 취약: 파일 확장자 검증 없음
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO files (filename, filepath, uploader) VALUES (?, ?, ?)",
                     (filename, filepath, session['username']))
        conn.commit()
        conn.close()
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('files'))
    
    return render_template('upload.html')

# 파일 목록
@app.route('/files')
def files():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files ORDER BY uploaded_at DESC")
    file_list = cursor.fetchall()
    conn.close()
    return render_template('files.html', files=file_list)

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# 프로필 수정 (CSRF 취약)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 취약: CSRF 토큰 없음
        email = request.form['email']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE id=?",
                     (email, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Profile updated successfully!', 'success')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
