import json
import os
import sys
from datetime import datetime

# -------------------------------------------------------------------------
# 설정 및 리포트 관련 함수
# -------------------------------------------------------------------------

def load_config():
    """config.json에서 설정 로드"""
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'target_url': 'http://127.0.0.1:8080/',
        'login': {'username': 'guest', 'password': 'guest'},
        'project_path': '.'
    }

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
    <title>DNA Lab OS Security Scan Report</title>
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
            <h1>DNA Lab OS Security Scan Report</h1>
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
            Generated by DNA Lab OS Security Scanner
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
    
    txt_path = f"reports/os_scan_report_{timestamp}.txt"
    html_path = f"reports/os_scan_report_{timestamp}.html"
    pdf_path = f"reports/os_scan_report_{timestamp}.pdf"
    
    # 1. TXT 저장
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("[ DNA Lab OS Security Scan Report ]\n")
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


def run_os_scan(config, os_scan_mode="remote"):
    """OS 스캔 실행 (웹 스캔 제외)"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scanner_path = os.path.join(base_dir, 'scanners')
    
    print(f"\n[DEBUG] 스캐너 폴더 경로: {scanner_path}")
    
    if not os.path.exists(scanner_path):
        print("오류: 'scanners' 폴더를 찾을 수 없습니다.")
        return []

    if scanner_path not in sys.path:
        sys.path.append(scanner_path)
        
    results = []
    target_url = config['target_url']
    login_info = config['login']
    
    # OS 스캐너만 추가
    os_scanners = []
    
    try:
        from scanners.os_scan import utils as os_utils
        os_utils.set_scan_mode(os_scan_mode)
        session = os_utils.get_session_with_admin_auth(target_url, login_info, mode=os_scan_mode)
        os_type = os_utils.detect_os(target_url, session, mode=os_scan_mode)
        
        if os_type != "Windows":
            os_scanners = [
                (1, "OS: Root 원격 로그인 제한", "scanners.os_scan.01_root_remote_login", "os"),
                (2, "OS: 비밀번호 관리정책 설정", "scanners.os_scan.02_password_policy", "os"),
                (3, "OS: 계정 잠금 임계값 설정", "scanners.os_scan.03_account_lockout", "os"),
                (4, "OS: 비밀번호 파일 보호", "scanners.os_scan.04_password_file_protection", "os"),
                (5, "OS: root 이외 UID 0 금지", "scanners.os_scan.05_root_uid_zero", "os"),
                (6, "OS: 사용자 계정 su 기능 제한", "scanners.os_scan.06_root_su_restriction", "os"),
                (7, "OS: 계정이 존재하지 않는 GID", "scanners.os_scan.07_invalid_gid", "os"),
                (8, "OS: 동일한 UID 금지", "scanners.os_scan.08_duplicate_uid", "os"),
                (9, "OS: 사용자 shell 점검", "scanners.os_scan.09_user_shell_check", "os"),
                (10, "OS: 세션 종료 시간 설정", "scanners.os_scan.10_session_timeout", "os"),
                (11, "OS: 안전한 비밀번호 암호화 알고리즘", "scanners.os_scan.11_password_hashing", "os"),
                (12, "OS: Root 홈, PATH 설정", "scanners.os_scan.12_root_home_path", "os"),
                (13, "OS: 파일 및 디렉터리 소유자 설정", "scanners.os_scan.13_file_ownership", "os"),
                (14, "OS: /etc/passwd 권한 설정", "scanners.os_scan.14_passwd_permissions", "os"),
                (15, "OS: 시스템 시작 스크립트 권한", "scanners.os_scan.15_startup_script_permissions", "os"),
                (16, "OS: /etc/shadow 권한 설정", "scanners.os_scan.16_shadow_permissions", "os"),
                (17, "OS: /etc/hosts 권한 설정", "scanners.os_scan.17_hosts_permissions", "os"),
                (18, "OS: /etc/inetd.conf 권한 설정", "scanners.os_scan.18_inetd_permissions", "os"),
                (19, "OS: /etc/(r)syslog.conf 권한 설정", "scanners.os_scan.19_syslog_permissions", "os"),
                (20, "OS: /etc/services 권한 설정", "scanners.os_scan.20_services_permissions", "os"),
                (21, "OS: SUID/SGID 설정 파일 점검", "scanners.os_scan.21_suid_sgid", "os"),
                (22, "OS: 사용자 환경변수 파일 권한", "scanners.os_scan.22_user_startup_files", "os"),
                (23, "OS: .rhosts/hosts.equiv 사용 금지", "scanners.os_scan.23_rhosts_hosts_equiv", "os"),
                (24, "OS: 접속 IP 및 포트 제한", "scanners.os_scan.24_access_ip_port_restriction", "os"),
                (25, "OS: hosts.lpd 권한 설정", "scanners.os_scan.25_hosts_lpd_permissions", "os"),
                (26, "OS: UMASK 설정 관리", "scanners.os_scan.26_umask_settings", "os"),
                (27, "OS: 홈디렉토리 소유자 및 권한", "scanners.os_scan.27_home_dir_permissions", "os"),
                (28, "OS: 홈 디렉토리 존재 여부", "scanners.os_scan.28_home_dir_existence", "os"),
                (29, "OS: Finger 서비스 비활성화", "scanners.os_scan.29_finger_service", "os"),
                (30, "OS: 공유 서비스 익명 접근 제한", "scanners.os_scan.30_anonymous_access", "os"),
                (31, "OS: r 계열 서비스 비활성화", "scanners.os_scan.31_r_services", "os"),
                (32, "OS: crontab 설정파일 권한", "scanners.os_scan.32_crontab_permissions", "os"),
                (33, "OS: DoS 서비스 비활성화", "scanners.os_scan.33_dos_services", "os"),
                (34, "OS: 불필요한 NFS 서비스", "scanners.os_scan.34_nfs_service", "os"),
                (35, "OS: NFS 접근 통제", "scanners.os_scan.35_nfs_access_control", "os"),
                (36, "OS: automountd 비활성화", "scanners.os_scan.36_automount_service", "os"),
                (37, "OS: RPC 서비스 비활성화", "scanners.os_scan.37_rpc_services", "os"),
                (38, "OS: NIS/NIS+ 점검", "scanners.os_scan.38_nis_services", "os"),
                (39, "OS: tftp/talk 서비스 비활성화", "scanners.os_scan.39_tftp_talk_services", "os"),
                (40, "OS: Telnet 서비스 비활성화", "scanners.os_scan.40_telnet_service", "os"),
                (41, "OS: FTP 배너 정보 노출 제한", "scanners.os_scan.41_ftp_banner", "os"),
                (42, "OS: 암호화되지 않는 FTP 비활성화", "scanners.os_scan.42_ftp_service_disabled", "os"),
                (43, "OS: FTP 계정 shell 제한", "scanners.os_scan.43_ftp_shell_restriction", "os"),
                (44, "OS: FTP 접근 제어 설정", "scanners.os_scan.44_ftpusers_permissions", "os"),
                (45, "OS: Ftpusers root 설정", "scanners.os_scan.45_ftpusers_root_access", "os"),
                (46, "OS: SNMP 서비스 비활성화", "scanners.os_scan.46_snmp_service", "os"),
                (47, "OS: sudo 권한 설정", "scanners.os_scan.47_sudoers_permissions", "os"),
                (48, "OS: NTP 시각 동기화", "scanners.os_scan.48_ntp_settings", "os"),
                (49, "OS: 시스템 로깅 정책", "scanners.os_scan.49_logging_policy", "os"),
                (50, "OS: 로그 디렉터리 권한", "scanners.os_scan.50_log_dir_permissions", "os"),
            ]
            print(f"[*] OS 감지 완료: {os_type} - OS 스캐너 {len(os_scanners)}개 실행")
        else:
            print(f"[*] OS 감지 완료: {os_type} - OS 스캐너 스킵 (Windows는 지원하지 않음)")
            return []
    except Exception as e:
        print(f"[!] OS 감지 실패: {str(e)}")
        return []
    
    total_scanners = len(os_scanners)
    for idx, (num, name, mod_name, s_type) in enumerate(os_scanners, 1):
        print(f"[*] Running {name} ({idx}/{total_scanners})...", end=' ', flush=True)
        try:
            # 프로젝트 루트를 sys.path에 추가
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            
            module = __import__(mod_name, fromlist=[''])
            res = module.scan(target_url, login_info)
            results.append(res)
            
            if res['vulnerable']:
                print("[!] 취약점 발견")
            else:
                print("[+] 안전")
                
        except ImportError as e:
            print(f"\n   [-] 불러오기 실패: {e}")
        except Exception as e:
            print(f"\n   [-] 실행 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            
    return results


def main():
    print("\n" + "=" * 60)
    print(" DNA Lab OS Security Scanner")
    print("=" * 60)
    
    config = load_config()
    default_target = "http://127.0.0.1:8080/"
    change_target = input("\n Change target URL? [y/N]: ").strip().lower()
    if change_target in ['y', 'yes']:
        new_target = input(f" Target URL [{default_target}]: ").strip()
        config['target_url'] = new_target if new_target else default_target
    else:
        config['target_url'] = default_target
    print(f" Target: {config['target_url']}")
    print("-" * 60)
    
    print(" Select OS Scan Mode:")
    print("  1. Local  (직접 OS 접근 - SSH 등)")
    print("  2. Remote (OS Command Injection 취약점 이용)")
    
    choice = input("\n > Choice [2]: ").strip() or '2'
    os_scan_mode = "local" if choice in ['1', 'l', 'local'] else "remote"
    
    results = []
    
    try:
        print("\n[ OS Security Scan ]")
        results = run_os_scan(config, os_scan_mode)
        
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
            print("\nNo results generated. (Windows OS는 지원하지 않습니다)")
            
    except KeyboardInterrupt:
        print("\n\n[*] Scan interrupted by user.")
    except Exception as e:
        print(f"\n[-] Fatal Error: {str(e)}")

if __name__ == "__main__":
    main()