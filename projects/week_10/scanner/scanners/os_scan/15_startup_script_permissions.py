import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

def _collect_paths(target_url, session, command):
    output = execute_command(target_url, session, command)
    paths = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if "No such file" in line or "cannot" in line:
            continue
        paths.append(line)
    return sorted(set(paths))

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
        'name': 'OS: 시스템 시작 스크립트 권한 설정',
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
            rc_paths = _collect_paths(target_url, session, "readlink -f /etc/rc.d/*/* 2>/dev/null")
            systemd_paths = _collect_paths(target_url, session, "readlink -f /etc/systemd/system/* 2>/dev/null")
            all_paths = rc_paths + systemd_paths

            issues = []
            for path in all_paths:
                if path == "/dev/null":
                    continue
                stat = get_file_stat(target_url, session, path)
                if not stat:
                    continue
                owner = stat['owner']
                perm = stat['perm']
                if owner != "root" or _has_write_permission(perm):
                    issues.append(f"{path} (owner={owner}, perm={perm})")

            if issues:
                result['vulnerable'] = True
                result['details'].append("[OS] 시스템 시작 스크립트 권한 취약")
                for item in issues[:5]:
                    result['details'].append(f"  - {item}")
                result['recommendations'].append("시작 스크립트 소유자를 root로 설정하고 쓰기 권한 제거")
            else:
                result['details'].append("[OS] 시스템 시작 스크립트 권한: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 시스템 시작 스크립트 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
