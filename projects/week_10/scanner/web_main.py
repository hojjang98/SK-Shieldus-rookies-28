import json
import os
import sys
import argparse
from datetime import datetime

# -------------------------------------------------------------------------
# 설정 및 리포트 관련 함수
# -------------------------------------------------------------------------

def parse_arguments():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description='DNA Lab Security Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                                    # Use default target (http://127.0.0.1:8080)
  python main.py -t http://localhost:8080          # Specify custom target
  python main.py --target http://192.168.1.100:80  # Specify custom target (long option)
        '''
    )
    
    parser.add_argument(
        '-t', '--target',
        type=str,
        default='http://127.0.0.1:8080',
        help='Target URL (default: http://127.0.0.1:8080)'
    )
    
    return parser.parse_args()

def load_config(target_url=None):
    """config.json에서 설정 로드 (target_url 우선순위: CLI args > config.json > default)"""
    config = {
        'target_url': 'http://127.0.0.1:8080',
        'login': {'username': 'guest', 'password': 'guest'},
        'project_path': '.'
    }
    
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            config.update(loaded)
    
    # CLI 인자로 전달된 target_url이 있으면 최우선 적용
    if target_url:
        config['target_url'] = target_url
    
    return config

def generate_html_report(results, config):
    """HTML 리포트 생성"""
    vulnerable_count = sum(1 for r in results if r['vulnerable'])
    safe_count = len(results) - vulnerable_count
    
    # 실제 발견된 취약점 상세 개수 계산
    total_findings = 0
    for r in results:
        if r.get('details'):
            details = r['details'] if isinstance(r['details'], list) else [r['details']]
            total_findings += len(details)
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>DNA Lab Security Scan Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f4f4f4; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 8px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; color: #2c3e50; }}
        .meta {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 30px; font-size: 0.9em; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; text-align: center; }}
        .card {{ padding: 20px; border-radius: 4px; color: white; }}
        .card.total {{ background: #34495e; }}
        .card.vuln {{ background: #e74c3c; }}
        .card.safe {{ background: #27ae60; }}
        .card.findings {{ background: #3498db; }}
        .card h3 {{ margin: 0; font-size: 2em; }}
        .item {{ border: 1px solid #ddd; margin-bottom: 20px; border-radius: 4px; overflow: hidden; }}
        .item-head {{ padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; background: #eee; font-weight: bold; }}
        .item-head.vuln {{ background: #fadbd8; color: #c0392b; border-left: 5px solid #c0392b; }}
        .item-head.safe {{ background: #d5f5e3; color: #27ae60; border-left: 5px solid #27ae60; }}
        .item-body {{ padding: 20px; }}
        .section {{ margin-bottom: 15px; }}
        .section h4 {{ margin-bottom: 5px; color: #555; font-size: 0.9em; text-transform: uppercase; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        ul {{ padding-left: 20px; margin: 0; }}
        li {{ margin-bottom: 5px; font-size: 0.95em; word-break: break-all; }}
        .footer {{ margin-top: 50px; text-align: center; font-size: 0.8em; color: #888; border-top: 1px solid #eee; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DNA Lab Security Scan Report</h1>
        </div>
        
        <div class="meta">
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Target:</strong> {config.get('target_url', 'N/A')}</p>
        </div>
        
        <div class="summary">
            <div class="card total">
                <h3>{len(results)}</h3>
                <p>Total Scans</p>
            </div>
            <div class="card vuln">
                <h3>{vulnerable_count}</h3>
                <p>Vulnerable</p>
            </div>
            <div class="card safe">
                <h3>{safe_count}</h3>
                <p>Safe</p>
            </div>
            <div class="card findings">
                <h3>{total_findings}</h3>
                <p>Total Findings</p>
            </div>
        </div>
"""
    
    for i, result in enumerate(results, 1):
        status_class = 'vuln' if result['vulnerable'] else 'safe'
        status_text = 'VULNERABLE' if result['vulnerable'] else 'SAFE'
        
        html += f"""
        <div class="item">
            <div class="item-head {status_class}">
                <span>{i}. {result['name']}</span>
                <span>{status_text}</span>
            </div>
            <div class="item-body">
"""
        if result.get('details'):
            html += """
                <div class="section">
                    <h4>Details</h4>
                    <ul>"""
            
            details = result['details'] if isinstance(result['details'], list) else [result['details']]
            unique_details = list(dict.fromkeys(details))
            
            for detail in unique_details:
                safe_detail = str(detail).replace('<', '&lt;').replace('>', '&gt;')
                html += f"<li>{safe_detail}</li>"
            
            html += """</ul>
                </div>"""

        if result.get('recommendation'):
            rec = result['recommendation'].replace('<', '&lt;').replace('>', '&gt;')
            html += f"""
                <div class="section">
                    <h4>Recommendation</h4>
                    <p>{rec}</p>
                </div>"""
                
        html += "</div></div>"

    html += """
        <div class="footer">
            Generated by DNA Lab Security Scanner
        </div>
    </div>
</body>
</html>
"""
    return html

def save_report(results, config):
    """TXT, HTML, PDF 리포트 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs('reports', exist_ok=True)
    
    txt_path = f"reports/scan_report_{timestamp}.txt"
    html_path = f"reports/scan_report_{timestamp}.html"
    pdf_path = f"reports/scan_report_{timestamp}.pdf"
    
    # 1. TXT 저장
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("[ DNA Lab Security Scan Report ]\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target: {config.get('target_url')}\n")
        f.write("=" * 60 + "\n")
        
        # 취약점 개수 요약
        vulnerable_count = sum(1 for r in results if r['vulnerable'])
        safe_count = len(results) - vulnerable_count
        
        # 실제 발견된 취약점 상세 개수 계산
        total_findings = 0
        for r in results:
            if r.get('details'):
                details = r['details'] if isinstance(r['details'], list) else [r['details']]
                total_findings += len(details)
        
        f.write(f"\n[Summary]\n")
        f.write(f"Total Scans: {len(results)}\n")
        f.write(f"Vulnerable Scans: {vulnerable_count}\n")
        f.write(f"Safe Scans: {safe_count}\n")
        f.write(f"Total Findings: {total_findings}\n")
        f.write("=" * 60 + "\n\n")
        
        for idx, res in enumerate(results, 1):
            status = "[!]" if res['vulnerable'] else "[+]"
            f.write(f"{idx}. {res['name']} {status}\n")
            if res.get('details'):
                f.write("   [Details]\n")
                details = res['details'] if isinstance(res['details'], list) else [res['details']]
                for d in list(set(details)):
                    f.write(f"   - {d}\n")
            if res.get('recommendation'):
                f.write(f"   [Fix] {res['recommendation']}\n")
            f.write("-" * 60 + "\n")

    # 2. HTML 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(generate_html_report(results, config))
        
    # 3. PDF 저장 (옵션)
    pdf_status = "Skipped"
    try:
        from weasyprint import HTML
        HTML(html_path).write_pdf(pdf_path)
        pdf_status = "Created"
    except ImportError:
        pdf_status = "WeasyPrint not installed"
    except Exception as e:
        pdf_status = f"Error: {str(e)}"
        
    return {'txt': txt_path, 'html': html_path, 'pdf': pdf_path, 'pdf_status': pdf_status}

# -------------------------------------------------------------------------
# 스캔 실행 함수
# -------------------------------------------------------------------------

def run_static_scan(config):
    """정적 스캔 실행"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scanner_dir = os.path.join(base_dir, 'scanners')
    target_path = scanner_dir if os.path.exists(scanner_dir) else base_dir
    
    if target_path not in sys.path:
        sys.path.insert(0, target_path)
        
    results = []
    
    scanners = [
        (1, "XSS", "01_xss_scanner", "xss"),
        (2, "SQL Injection", "02_sqli_scanner", "sqli"),
        (3, "OS Command Injection", "03_os_command_injection_scanner", "os_cmd"),
        (4, "CSRF", "04_csrf_scanner", "csrf"),
        (5, "Weak Password", "05_weak_password", "weak_pwd"),
        (6, "Access Control", "06_access_control_scanner", "access"),
        (7, "Password Recovery", "07_password_recovery", "pwd_recovery"),
        (8, "Session Mgmt", "08_session_scanner", "session"),
        (9, "Cookie Security", "09_cookie_scanner", "cookie"),
        (10, "File Transfer", "10_file_transfer_scanner", "file"),
        (11, "Path Traversal", "11_path_traversal_scanner", "path"),
        (12, "Error Handling", "12_error_page_scanner", "error"),
        (13, "Format String", "13_formatting_scanner", "format"),
        (14, "HTTP Methods", "14_http_method_scanner", "http_method"),
        (15, "SSRF", "15_ssrf_scanner", "ssrf"),
    ]
    
    class DummyCrawl:
        def __init__(self):
            self.forms = []
            self.urls = []
            self.cookies = {}

    for num, name, mod_name, s_type in scanners:
        print(f"[*] Running {name} scanner ({num}/15)...", end=' ', flush=True)
        try:
            import importlib
            module = importlib.import_module(mod_name)
            
            if s_type in ['xss', 'access', 'session', 'cookie', 'format', 'ssrf', 'os_cmd']:
                res = module.scan(config['target_url'], config['login'])
            elif s_type == 'code':
                res = module.scan(config.get('project_path', '.'))
            elif s_type in ['file', 'error', 'http_method']:
                res = module.scan(config['target_url'], DummyCrawl())
            else:
                res = module.scan(config['target_url'])
                
            results.append(res)
            
            if res['vulnerable']:
                print("[!] VULNERABLE")
            else:
                print("[+] Safe")
                
        except ImportError as e:
            print(f"[-] Module not found: {e}")
            if num == 1:
                print(f"    (Check if '{mod_name}.py' is inside '{target_path}')")
        except Exception as e:
            import traceback
            print(f"[-] Error: {str(e)}")
            if num == 10:  # 10번 스캐너만 상세 에러 출력
                traceback.print_exc()
            
    return results

def main():
    # 커맨드라인 인자 파싱
    args = parse_arguments()
    
    print("\n" + "=" * 60)
    print(" DNA Lab Security Vulnerability Scanner")
    print("=" * 60)
    
    # target_url을 CLI 인자에서 가져오기
    config = load_config(args.target)
    print(f" Target: {config['target_url']}")
    print("-" * 60)
    
    print(" Select Scan Mode:")
    print("  1. Static Scan (Whitebox + Basic Blackbox)")
    print("  2. Dynamic Scan (Crawler + Active Scan)")
    print("  3. Full Scan (Static + Dynamic)")
    
    choice = input("\n > Choice [1]: ").strip() or '1'
    
    results = []
    
    try:
        # 정적 스캔
        if choice in ['1', '3']:
            print("\n[ Phase 1: Static Scan ]")
            results.extend(run_static_scan(config))
            
        # 동적 스캔
        if choice in ['2', '3']:
            print("\n[ Phase 2: Dynamic Scan ]")
            try:
                from dynamic_scanner import DynamicScanner
                scanner = DynamicScanner(config['target_url'], config['login'])
                res = scanner.scan_all()
                results.append(res)
            except ImportError:
                print(" [-] Dynamic scanner module not found.")
            except Exception as e:
                print(f" [-] Dynamic scan error: {str(e)}")
        
        # 결과 처리
        if results:
            print("\n" + "=" * 60)
            print(" Scan Complete")
            print("=" * 60)
            
            files = save_report(results, config)
            print(f" Reports generated:")
            print(f"  - TXT:  {files['txt']}")
            print(f"  - HTML: {files['html']}")
            print(f"  - PDF:  {files['pdf']} ({files['pdf_status']})")
            
            vuln_cnt = sum(1 for r in results if r['vulnerable'])
            print(f"\n Summary: {vuln_cnt} Vulnerabilities found.")
            
        else:
            print("\nNo results generated.")
            
    except KeyboardInterrupt:
        print("\n\n[*] Scan interrupted by user.")
    except Exception as e:
        print(f"\n[-] Fatal Error: {str(e)}")

if __name__ == "__main__":
    main()