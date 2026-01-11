import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 사용자 shell 점검',
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
            passwd_content = execute_command(target_url, session, "cat /etc/passwd 2>&1")
            entries = parse_passwd(passwd_content)

            target_users = {
                "daemon", "bin", "sys", "adm", "listen", "nobody", "nobody4",
                "noaccess", "diag", "operator", "games", "gopher"
            }
            allowed_shells = {"/bin/false", "/sbin/nologin", "/usr/sbin/nologin"}

            vulnerable_users = []
            for entry in entries:
                if entry['name'] == "admin":
                    continue
                if entry['name'] in target_users and entry['shell'] not in allowed_shells:
                    vulnerable_users.append(f"{entry['name']}({entry['shell']})")

            if vulnerable_users:
                result['vulnerable'] = True
                result['details'].append(f"[OS] 로그인 불필요 계정에 쉘 부여됨: {', '.join(vulnerable_users)}")
                result['recommendations'].append("불필요 계정의 쉘을 /bin/false 또는 /sbin/nologin으로 변경")
            else:
                result['details'].append("[OS] 로그인 불필요 계정 쉘 설정: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 로그인 불필요 계정의 쉘이 제한됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
