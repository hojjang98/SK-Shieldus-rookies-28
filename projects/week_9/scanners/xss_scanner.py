import requests
from datetime import datetime
from bs4 import BeautifulSoup

class XSSScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.vulnerabilities = []
        self.session = requests.Session()
        
        # XSS 테스트 페이로드
        self.payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<body onload=alert('XSS')>",
        ]
    
    def login(self):
        """로그인 (게시판 작성을 위해)"""
        print("[*] Logging in...")
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.session.post(f"{self.base_url}/login", data=data)
        if 'dashboard' in response.url or response.status_code == 302:
            print("  [+] Login successful")
            return True
        return False
    
    def test_board_xss(self):
        """게시판 XSS 테스트"""
        print("\n[*] Testing Board for XSS vulnerabilities...")
        
        for payload in self.payloads:
            try:
                # 게시글 작성
                data = {
                    'title': f'XSS Test: {payload[:30]}',
                    'content': payload
                }
                response = self.session.post(
                    f"{self.base_url}/board/write",
                    data=data,
                    allow_redirects=True,
                    timeout=10
                )
                
                # 게시판 확인
                board_response = self.session.get(f"{self.base_url}/board", timeout=10)
                
                # 페이로드가 그대로 HTML에 삽입되었는지 확인
                if payload in board_response.text:
                    self.vulnerabilities.append({
                        'type': 'Reflected XSS',
                        'location': '/board',
                        'payload': payload,
                        'severity': 'HIGH',
                        'description': f"XSS payload reflected in board: {payload}"
                    })
                    print(f"  [!] XSS VULNERABLE: {payload[:50]}")
                else:
                    print(f"  [-] Payload filtered: {payload[:50]}")
                    
            except Exception as e:
                print(f"  [-] Error testing payload: {str(e)}")
    
    def test_search_xss(self):
        """검색 기능 XSS 테스트"""
        print("\n[*] Testing Search for XSS vulnerabilities...")
        
        for payload in self.payloads:
            try:
                response = self.session.get(
                    f"{self.base_url}/search",
                    params={'q': payload},
                    timeout=10
                )
                
                # 페이로드가 반영되는지 확인
                if payload in response.text:
                    self.vulnerabilities.append({
                        'type': 'Reflected XSS',
                        'location': '/search',
                        'payload': payload,
                        'severity': 'MEDIUM',
                        'description': f"XSS payload reflected in search: {payload}"
                    })
                    print(f"  [!] XSS VULNERABLE: {payload[:50]}")
                    
            except Exception as e:
                print(f"  [-] Error: {str(e)}")
    
    def generate_report(self):
        """리포트 생성"""
        report = "\n" + "="*60 + "\n"
        report += "XSS SCAN REPORT\n"
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
            report += "No XSS vulnerabilities found.\n"
        
        return report
    
    def scan(self):
        """전체 스캔 실행"""
        print(f"\n[*] Starting XSS Scan on {self.base_url}")
        print("="*60)
        
        if self.login():
            self.test_board_xss()
            self.test_search_xss()
        else:
            print("[!] Login failed. Cannot test authenticated features.")
        
        report = self.generate_report()
        print(report)
        
        # 리포트 파일 저장
        with open('../reports/xss_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[+] Report saved to: ../reports/xss_report.txt")
        
        return self.vulnerabilities

if __name__ == '__main__':
    scanner = XSSScanner('http://localhost:5000')
    scanner.scan()
