import requests
from datetime import datetime
from bs4 import BeautifulSoup

class CSRFScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.vulnerabilities = []
        self.session = requests.Session()
    
    def login(self):
        """로그인"""
        print("[*] Logging in...")
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.session.post(f"{self.base_url}/login", data=data)
        if 'dashboard' in response.url or response.status_code == 302:
            print("  [+] Login successful")
            return True
        return False
    
    def check_csrf_token(self, url, form_data=None):
        """CSRF 토큰 존재 여부 확인"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 폼 찾기
            forms = soup.find_all('form')
            
            for form in forms:
                # CSRF 토큰 관련 input 필드 찾기
                csrf_inputs = form.find_all('input', {'name': lambda x: x and 'csrf' in x.lower()})
                
                if not csrf_inputs:
                    # 폼의 action 속성 확인
                    action = form.get('action', 'unknown')
                    method = form.get('method', 'GET').upper()
                    
                    if method == 'POST':
                        return False, action
            
            return True, None
            
        except Exception as e:
            print(f"  [-] Error checking CSRF token: {str(e)}")
            return None, None
    
    def test_profile_csrf(self):
        """프로필 수정 CSRF 테스트"""
        print("\n[*] Testing Profile Update for CSRF protection...")
        
        has_token, action = self.check_csrf_token(f"{self.base_url}/profile")
        
        if has_token is False:
            # CSRF 토큰 없이 요청 시도
            try:
                # 새로운 세션(공격자)으로 요청
                attacker_session = requests.Session()
                data = {'email': 'hacked@attacker.com'}
                
                # CSRF 공격 시뮬레이션 (쿠키 없이)
                response = attacker_session.post(
                    f"{self.base_url}/profile",
                    data=data,
                    timeout=10
                )
                
                self.vulnerabilities.append({
                    'type': 'CSRF (Cross-Site Request Forgery)',
                    'location': '/profile',
                    'severity': 'HIGH',
                    'description': 'No CSRF token found in profile update form. Vulnerable to CSRF attacks.'
                })
                print(f"  [!] CSRF VULNERABLE: No CSRF token in profile form")
                
            except Exception as e:
                print(f"  [-] Error: {str(e)}")
        else:
            print(f"  [+] CSRF token found - Protected")
    
    def test_post_creation_csrf(self):
        """게시글 작성 CSRF 테스트"""
        print("\n[*] Testing Post Creation for CSRF protection...")
        
        has_token, action = self.check_csrf_token(f"{self.base_url}/board/write")
        
        if has_token is False:
            self.vulnerabilities.append({
                'type': 'CSRF (Cross-Site Request Forgery)',
                'location': '/board/write',
                'severity': 'MEDIUM',
                'description': 'No CSRF token found in post creation form.'
            })
            print(f"  [!] CSRF VULNERABLE: No CSRF token in post creation form")
        else:
            print(f"  [+] CSRF token found - Protected")
    
    def generate_report(self):
        """리포트 생성"""
        report = "\n" + "="*60 + "\n"
        report += "CSRF SCAN REPORT\n"
        report += "="*60 + "\n"
        report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Target: {self.base_url}\n"
        report += f"Total Vulnerabilities Found: {len(self.vulnerabilities)}\n"
        report += "="*60 + "\n\n"
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                report += f"{i}. [{vuln['severity']}] {vuln['type']}\n"
                report += f"   Location: {vuln['location']}\n"
                report += f"   Description: {vuln['description']}\n\n"
        else:
            report += "No CSRF vulnerabilities found.\n"
        
        return report
    
    def scan(self):
        """전체 스캔 실행"""
        print(f"\n[*] Starting CSRF Scan on {self.base_url}")
        print("="*60)
        
        if self.login():
            self.test_profile_csrf()
            self.test_post_creation_csrf()
        else:
            print("[!] Login failed. Cannot test authenticated features.")
        
        report = self.generate_report()
        print(report)
        
        # 리포트 파일 저장
        with open('../reports/csrf_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[+] Report saved to: ../reports/csrf_report.txt")
        
        return self.vulnerabilities

if __name__ == '__main__':
    scanner = CSRFScanner('http://localhost:5000')
    scanner.scan()
