import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd, parse_group
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd, parse_group

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 계정이 존재하지 않는 GID',
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
            group_content = execute_command(target_url, session, "cat /etc/group 2>&1")
            passwd_entries = parse_passwd(passwd_content)
            group_entries = parse_group(group_content)
            group_gids = {g['gid'] for g in group_entries if g['gid'] is not None}

            invalid_gid_users = []
            for entry in passwd_entries:
                if entry['gid'] is None:
                    continue
                if entry['gid'] not in group_gids:
                    invalid_gid_users.append(f"{entry['name']}({entry['gid']})")

            if invalid_gid_users:
                result['vulnerable'] = True
                result['details'].append(f"[OS] 존재하지 않는 GID 사용 계정: {', '.join(invalid_gid_users)}")
                result['recommendations'].append("계정의 GID를 유효한 그룹으로 변경")
            else:
                result['details'].append("[OS] 존재하지 않는 GID 사용 계정 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - GID 설정이 유효함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
