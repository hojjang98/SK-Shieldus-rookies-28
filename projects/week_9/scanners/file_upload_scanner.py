import requests
from datetime import datetime
import os
import io

class FileUploadScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.vulnerabilities = []
        self.session = requests.Session()
        
        # 위험한 파일 확장자 리스트
        self.dangerous_extensions = [
            'php', 'jsp', 'asp', 'aspx', 'exe', 'bat', 
            'sh', 'py', 'rb', 'pl', 'cgi'
        ]
    
    def login(self):
        """로그인"""
        print("[*] Logging in...")
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.session.post(f"{self.base_url}/login", data=data)
        if 'dashboard' in response.url or response.status_code == 302:
            print("  [+] Login successful")
            return True
        return False
    
    def test_file_extension_bypass(self):
        """파일 확장자 검증 우회 테스트"""
        print("\n[*] Testing File Upload Extension Bypass...")
        
        for ext in self.dangerous_extensions:
            try:
                # 악성 파일 생성 (테스트용)
                file_content = b'<?php echo "Malicious Code"; ?>'
                filename = f'malicious.{ext}'
                
                files = {
                    'file': (filename, io.BytesIO(file_content), 'application/octet-stream')
                }
                
                response = self.session.post(
                    f"{self.base_url}/upload",
                    files=files,
                    timeout=10
                )
                
                # 업로드 성공 여부 확인
                if response.status_code == 200 and 'success' in response.text.lower():
                    self.vulnerabilities.append({
                        'type': 'File Upload Vulnerability',
                        'location': '/upload',
                        'extension': ext,
                        'severity': 'CRITICAL',
                        'description': f'Dangerous file extension allowed: .{ext}'
                    })
                    print(f"  [!] VULNERABLE: .{ext} file uploaded successfully")
                else:
                    print(f"  [-] Blocked: .{ext}")
                    
            except Exception as e:
                print(f"  [-] Error testing .{ext}: {str(e)}")
    
    def test_file_size_limit(self):
        """파일 크기 제한 테스트"""
        print("\n[*] Testing File Size Limits...")
        
        try:
            # 큰 파일 생성 (20MB)
            large_content = b'A' * (20 * 1024 * 1024)
            filename = 'large_file.txt'
            
            files = {
                'file': (filename, io.BytesIO(large_content), 'text/plain')
            }
            
            response = self.session.post(
                f"{self.base_url}/upload",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200 and 'success' in response.text.lower():
                print(f"  [!] WARNING: Large file (20MB) accepted")
            else:
                print(f"  [+] File size limit enforced")
                
        except Exception as e:
            print(f"  [-] Error testing file size: {str(e)}")
    
    def test_double_extension(self):
        """이중 확장자 우회 테스트"""
        print("\n[*] Testing Double Extension Bypass...")
        
        test_files = [
            'malicious.php.jpg',
            'malicious.asp.png',
            'shell.php.txt',
        ]
        
        for filename in test_files:
            try:
                file_content = b'<?php echo "Test"; ?>'
                files = {
                    'file': (filename, io.BytesIO(file_content), 'image/jpeg')
                }
                
                response = self.session.post(
                    f"{self.base_url}/upload",
                    files=files,
                    timeout=10
                )
                
                if response.status_code == 200 and 'success' in response.text.lower():
                    self.vulnerabilities.append({
                        'type': 'File Upload Vulnerability (Double Extension)',
                        'location': '/upload',
                        'filename': filename,
                        'severity': 'HIGH',
                        'description': f'Double extension bypass possible: {filename}'
                    })
                    print(f"  [!] VULNERABLE: {filename} uploaded")
                else:
                    print(f"  [-] Blocked: {filename}")
                    
            except Exception as e:
                print(f"  [-] Error: {str(e)}")
    
    def generate_report(self):
        """리포트 생성"""
        report = "\n" + "="*60 + "\n"
        report += "FILE UPLOAD VULNERABILITY SCAN REPORT\n"
        report += "="*60 + "\n"
        report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Target: {self.base_url}\n"
        report += f"Total Vulnerabilities Found: {len(self.vulnerabilities)}\n"
        report += "="*60 + "\n\n"
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                report += f"{i}. [{vuln['severity']}] {vuln['type']}\n"
                report += f"   Location: {vuln['location']}\n"
                if 'extension' in vuln:
                    report += f"   Extension: .{vuln['extension']}\n"
                if 'filename' in vuln:
                    report += f"   Filename: {vuln['filename']}\n"
                report += f"   Description: {vuln['description']}\n\n"
        else:
            report += "No file upload vulnerabilities found.\n"
        
        return report
    
    def scan(self):
        """전체 스캔 실행"""
        print(f"\n[*] Starting File Upload Vulnerability Scan on {self.base_url}")
        print("="*60)
        
        if self.login():
            self.test_file_extension_bypass()
            self.test_double_extension()
            self.test_file_size_limit()
        else:
            print("[!] Login failed. Cannot test authenticated features.")
        
        report = self.generate_report()
        print(report)
        
        # 리포트 파일 저장
        with open('../reports/file_upload_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[+] Report saved to: ../reports/file_upload_report.txt")
        
        return self.vulnerabilities

if __name__ == '__main__':
    scanner = FileUploadScanner('http://localhost:5000')
    scanner.scan()
