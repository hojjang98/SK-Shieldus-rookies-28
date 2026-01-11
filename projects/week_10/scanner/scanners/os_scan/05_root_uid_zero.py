import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: root 이외 UID 0 금지',
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
            uid_zero_users = [e['name'] for e in entries if e['uid'] == 0 and e['name'] != 'root']

            if uid_zero_users:
                result['vulnerable'] = True
                result['details'].append(f"[OS] UID 0 계정 발견: {', '.join(uid_zero_users)}")
                result['recommendations'].append("root 이외 UID 0 계정 제거 또는 UID 변경")
            else:
                result['details'].append("[OS] root 이외 UID 0 계정 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - root 이외 UID 0 계정이 없음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
