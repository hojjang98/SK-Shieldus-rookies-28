import requests
from datetime import datetime
import sys
import os

# 개별 스캐너 import
sys.path.append(os.path.dirname(__file__))
from sql_injection_scanner import SQLInjectionScanner
from xss_scanner import XSSScanner
from csrf_scanner import CSRFScanner
from file_upload_scanner import FileUploadScanner

class IntegratedScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.all_vulnerabilities = []
        self.scan_results = {}
    
    def run_all_scans(self):
        """모든 스캐너 실행"""
        print("\n" + "="*70)
        print("INTEGRATED VULNERABILITY SCANNER")
        print("="*70)
        print(f"Target: {self.base_url}")
        print(f"Scan Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # 1. SQL Injection Scan
        print("\n[1/4] Running SQL Injection Scanner...")
        print("-" * 70)
        sql_scanner = SQLInjectionScanner(self.base_url)
        sql_vulns = sql_scanner.scan()
        self.scan_results['SQL Injection'] = sql_vulns
        self.all_vulnerabilities.extend(sql_vulns)
        
        # 2. XSS Scan
        print("\n[2/4] Running XSS Scanner...")
        print("-" * 70)
        xss_scanner = XSSScanner(self.base_url)
        xss_vulns = xss_scanner.scan()
        self.scan_results['XSS'] = xss_vulns
        self.all_vulnerabilities.extend(xss_vulns)
        
        # 3. CSRF Scan
        print("\n[3/4] Running CSRF Scanner...")
        print("-" * 70)
        csrf_scanner = CSRFScanner(self.base_url)
        csrf_vulns = csrf_scanner.scan()
        self.scan_results['CSRF'] = csrf_vulns
        self.all_vulnerabilities.extend(csrf_vulns)
        
        # 4. File Upload Scan
        print("\n[4/4] Running File Upload Scanner...")
        print("-" * 70)
        upload_scanner = FileUploadScanner(self.base_url)
        upload_vulns = upload_scanner.scan()
        self.scan_results['File Upload'] = upload_vulns
        self.all_vulnerabilities.extend(upload_vulns)
    
    def generate_summary_report(self):
        """종합 리포트 생성"""
        report = "\n" + "="*70 + "\n"
        report += "COMPREHENSIVE SECURITY SCAN REPORT\n"
        report += "="*70 + "\n"
        report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Target URL: {self.base_url}\n"
        report += "="*70 + "\n\n"
        
        # 취약점 요약
        report += "VULNERABILITY SUMMARY\n"
        report += "-" * 70 + "\n"
        report += f"Total Vulnerabilities Found: {len(self.all_vulnerabilities)}\n\n"
        
        for scan_type, vulns in self.scan_results.items():
            report += f"  - {scan_type}: {len(vulns)} vulnerabilities\n"
        
        report += "\n" + "="*70 + "\n\n"
        
        # 심각도별 분류
        critical = [v for v in self.all_vulnerabilities if v.get('severity') == 'CRITICAL']
        high = [v for v in self.all_vulnerabilities if v.get('severity') == 'HIGH']
        medium = [v for v in self.all_vulnerabilities if v.get('severity') == 'MEDIUM']
        
        report += "SEVERITY BREAKDOWN\n"
        report += "-" * 70 + "\n"
        report += f"  CRITICAL: {len(critical)}\n"
        report += f"  HIGH: {len(high)}\n"
        report += f"  MEDIUM: {len(medium)}\n"
        report += "\n" + "="*70 + "\n\n"
        
        # 상세 취약점 목록
        report += "DETAILED VULNERABILITY LIST\n"
        report += "="*70 + "\n\n"
        
        for i, vuln in enumerate(self.all_vulnerabilities, 1):
            report += f"{i}. [{vuln.get('severity', 'N/A')}] {vuln.get('type', 'Unknown')}\n"
            report += f"   Location: {vuln.get('location', 'N/A')}\n"
            if 'payload' in vuln:
                report += f"   Payload: {vuln['payload']}\n"
            if 'extension' in vuln:
                report += f"   Extension: .{vuln['extension']}\n"
            report += f"   Description: {vuln.get('description', 'N/A')}\n\n"
        
        # 권장 사항
        report += "="*70 + "\n"
        report += "SECURITY RECOMMENDATIONS\n"
        report += "="*70 + "\n\n"
        
        recommendations = [
            "1. SQL Injection Prevention:",
            "   - Use parameterized queries (prepared statements)",
            "   - Implement input validation and sanitization",
            "   - Use ORM frameworks with built-in protections\n",
            
            "2. XSS Prevention:",
            "   - Implement output encoding/escaping",
            "   - Use Content Security Policy (CSP)",
            "   - Validate and sanitize user inputs\n",
            
            "3. CSRF Prevention:",
            "   - Implement CSRF tokens for all state-changing operations",
            "   - Use SameSite cookie attribute",
            "   - Verify Origin and Referer headers\n",
            
            "4. File Upload Security:",
            "   - Validate file extensions (whitelist approach)",
            "   - Verify file content (magic bytes)",
            "   - Store uploaded files outside web root",
            "   - Implement file size limits",
            "   - Rename uploaded files\n"
        ]
        
        for rec in recommendations:
            report += rec + "\n"
        
        report += "\n" + "="*70 + "\n"
        report += "End of Report\n"
        report += "="*70 + "\n"
        
        return report
    
    def save_report(self):
        """리포트 저장"""
        report = self.generate_summary_report()
        
        # 콘솔 출력
        print(report)
        
        # 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'../reports/comprehensive_report_{timestamp}.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[+] Comprehensive report saved to: {filename}")
        
        return filename

if __name__ == '__main__':
    scanner = IntegratedScanner('http://localhost:5000')
    scanner.run_all_scans()
    scanner.save_report()
