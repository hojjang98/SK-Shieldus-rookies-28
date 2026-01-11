import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 패스워드 파일 보호',
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
            # shadow 파일 존재 확인
            shadow_check = execute_command(target_url, session, "ls /etc | grep shadow 2>&1")
            
            if "shadow" in shadow_check:
                # /etc/passwd 파일 확인
                passwd_content = execute_command(target_url, session, "cat /etc/passwd 2>&1")
                
                vulnerable_lines = []
                for line in passwd_content.split('\n'):
                    if line.strip() and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) > 1 and parts[1] and parts[1][0] != 'x':
                            vulnerable_lines.append(line)
                            result['vulnerable'] = True
                
                if vulnerable_lines:
                    result['details'].append(f"[OS] 패스워드 파일 보호: 취약 (암호화되지 않은 패스워드 발견: {len(vulnerable_lines)}개)")
                    result['recommendations'].append("shadow 파일 사용 및 /etc/passwd의 패스워드 필드를 'x'로 변경")
                else:
                    result['details'].append("[OS] 패스워드 파일 보호: 양호 (모든 계정이 shadow 파일 사용)")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] 패스워드 파일 보호: 취약 (shadow 파일 미존재)")
                result['recommendations'].append("shadow 파일 생성 및 패스워드 마이그레이션")
        
        if not result['recommendations']:
            result['recommendation'] = '안전 - 패스워드 파일이 적절히 보호되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
            
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result
