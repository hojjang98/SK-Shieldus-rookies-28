import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd, get_file_stat

def _has_write_permission(perm_value):
    perm_str = perm_value[-3:] if len(perm_value) >= 3 else perm_value
    try:
        group_digit = int(perm_str[-2])
        other_digit = int(perm_str[-1])
    except (ValueError, IndexError):
        return True
    return (group_digit & 2) != 0 or (other_digit & 2) != 0

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 홈디렉토리 소유자 및 권한 설정',
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
            issues = []

            for entry in entries:
                home_dir = entry['home']
                if not home_dir or home_dir in ["/", "/nonexistent"]:
                    continue
                if not home_dir.startswith("/home/"):
                    continue
                stat = get_file_stat(target_url, session, home_dir)
                if not stat:
                    continue
                owner = stat['owner']
                perm = stat['perm']
                if owner != entry['name'] or _has_write_permission(perm):
                    issues.append(f"{entry['name']}:{home_dir} (owner={owner}, perm={perm})")

            if issues:
                result['vulnerable'] = True
                result['details'].append("[OS] 홈디렉토리 소유자/권한 문제 발견")
                for item in issues[:5]:
                    result['details'].append(f"  - {item}")
                result['recommendations'].append("홈디렉토리 소유자 및 권한 설정")
            else:
                result['details'].append("[OS] 홈디렉토리 소유자 및 권한: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 홈디렉토리 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
