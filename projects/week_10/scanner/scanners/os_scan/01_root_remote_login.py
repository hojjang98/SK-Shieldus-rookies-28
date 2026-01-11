import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: Root 원격 로그인 제한',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        session = get_session_with_admin_auth(target_url, login_info)
        os_type = detect_os(target_url, session)
        
        if os_type == "Windows":
            result['details'].append("[OS] Windows는 지원하지 않습니다")
            result['recommendation'] = 'Windows는 지원하지 않습니다'
            return result
        
        if os_type == "Linux":
            # SSH 프로세스 확인
            ssh_running = execute_command(target_url, session, "ps aux | grep -v grep | grep sshd 2>&1")
            telnet_running = execute_command(target_url, session, "ps aux | grep -v grep | grep telnet 2>&1")
            
            # SSH 체크
            if "sshd" in ssh_running.lower():
                # SSH 설정 확인 (Ubuntu는 sshd_config.d 포함)
                sshd_config = execute_command(
                    target_url,
                    session,
                    "cat /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null"
                )
                permit_root = None
                for line in sshd_config.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if re.match(r'^PermitRootLogin\\s+', line, re.IGNORECASE):
                        permit_root = line.split()[-1].lower()
                if permit_root == "no":
                    result['details'].append("[OS] SSH root 원격 로그인이 제한되어 있음 (PermitRootLogin no)")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] SSH root 원격 로그인이 허용되어 있음")
                    result['recommendations'].append("sshd_config에서 PermitRootLogin no 설정")
            else:
                result['details'].append("[OS] SSH가 실행되고 있지 않음")
            
            # Telnet 체크
            if "telnet" in telnet_running.lower():
                # Telnet 설정 확인
                pam_login = execute_command(target_url, session, "cat /etc/pam.d/login 2>&1")
                securetty = execute_command(target_url, session, "cat /etc/securetty 2>&1")
                
                pam_securetty = False
                for line in pam_login.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if "pam_securetty.so" in line and line.startswith("auth"):
                        pam_securetty = True
                        break
                if pam_securetty:
                    result['details'].append("[OS] Telnet root 접속 제한 설정이 있음")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] Telnet root 접속 제한 설정이 없음")
                    result['recommendations'].append("/etc/pam.d/login에 pam_securetty.so 모듈 추가")
                
                insecure_pts = []
                for line in securetty.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if line.startswith("pts") or "pts/" in line:
                        insecure_pts.append(line)
                if insecure_pts:
                    result['vulnerable'] = True
                    result['details'].append("[OS] /etc/securetty에 pts 설정이 존재함")
                    result['recommendations'].append("/etc/securetty에서 pts 설정 제거")
                else:
                    result['details'].append("[OS] /etc/securetty에 pts 설정이 없음 (양호)")
            else:
                result['details'].append("[OS] Telnet이 실행되고 있지 않음")
        
        if not result['recommendations']:
            result['recommendation'] = '안전 - Root 원격 로그인이 제한되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
            
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result
