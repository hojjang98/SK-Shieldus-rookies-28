import re
from datetime import datetime
from collections import Counter

class SecurityLogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.security_events = []
        self.sql_injection_attempts = []
        self.xss_attempts = []
        self.failed_logins = []
        
    def analyze(self):
        print("보안 로그 분석 시작...\n")
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
        except FileNotFoundError:
            print(f"로그 파일을 찾을 수 없습니다: {self.log_file}")
            return
        
        for line in logs:
            self.detect_sql_injection(line)
            self.detect_xss(line)
            self.detect_failed_login(line)
        
        self.print_report()
    
    def detect_sql_injection(self, log_line):
        sql_patterns = [
            r"'.*OR.*'.*=.*'",
            r"'.*--",
            r"UNION.*SELECT",
            r"';.*DROP",
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, log_line, re.IGNORECASE):
                self.sql_injection_attempts.append(log_line.strip())
                break
    
    def detect_xss(self, log_line):
        xss_patterns = [
            r"<script>",
            r"javascript:",
            r"onerror=",
            r"onload=",
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, log_line, re.IGNORECASE):
                self.xss_attempts.append(log_line.strip())
                break
    
    def detect_failed_login(self, log_line):
        if "Invalid credentials" in log_line or "login failed" in log_line.lower():
            self.failed_logins.append(log_line.strip())
    
    def print_report(self):
        print("=" * 60)
        print("보안 로그 분석 결과")
        print("=" * 60)
        print(f"\n분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"SQL Injection 시도: {len(self.sql_injection_attempts)}건")
        if self.sql_injection_attempts:
            print("\n최근 5건:")
            for attempt in self.sql_injection_attempts[:5]:
                print(f"  - {attempt}")
        
        print(f"\nXSS 공격 시도: {len(self.xss_attempts)}건")
        if self.xss_attempts:
            print("\n최근 5건:")
            for attempt in self.xss_attempts[:5]:
                print(f"  - {attempt}")
        
        print(f"\n로그인 실패: {len(self.failed_logins)}건")
        if self.failed_logins:
            print("\n최근 5건:")
            for attempt in self.failed_logins[:5]:
                print(f"  - {attempt}")
        
        print("\n" + "=" * 60)
        print("분석 완료")
        print("=" * 60)

def create_sample_log():
    sample_log = """2026-02-01 10:15:23 - INFO - User login attempt: admin
2026-02-01 10:15:25 - WARNING - Invalid credentials for user: admin' OR '1'='1
2026-02-01 10:16:01 - INFO - Search query: laptop
2026-02-01 10:17:32 - WARNING - Suspicious search: ' OR 1=1--
2026-02-01 10:18:45 - INFO - Comment posted: Great product!
2026-02-01 10:19:12 - WARNING - XSS attempt detected: <script>alert('XSS')</script>
2026-02-01 10:20:33 - INFO - File upload attempt: image.png
2026-02-01 10:21:05 - WARNING - Invalid file type: shell.php
2026-02-01 10:22:18 - INFO - User logout: admin
"""
    
    with open('logs/sample_security.log', 'w', encoding='utf-8') as f:
        f.write(sample_log)
    
    print("샘플 로그 파일 생성 완료: logs/sample_security.log\n")

if __name__ == '__main__':
    create_sample_log()
    
    analyzer = SecurityLogAnalyzer('logs/sample_security.log')
    analyzer.analyze()