import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

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
        'name': 'OS: 사용자 환경변수 파일 소유자 및 권한 설정',
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
            current_user = execute_command(target_url, session, "whoami 2>&1").strip()
            home_dir = execute_command(target_url, session, "echo $HOME 2>&1").strip()
            file_list = [
                ".profile", ".kshrc", ".cshrc", ".bashrc", ".bash_profile",
                ".login", ".exrc", ".netrc"
            ]

            issues = []
            for file_name in file_list:
                path = f"{home_dir}/{file_name}"
                stat = get_file_stat(target_url, session, path)
                if not stat:
                    continue
                owner = stat['owner']
                perm = stat['perm']
                if owner not in [current_user, "root"]:
                    issues.append(f"{path} (owner={owner})")
                elif _has_write_permission(perm):
                    issues.append(f"{path} (perm={perm})")

            if issues:
                result['vulnerable'] = True
                result['details'].append("[OS] 사용자 환경파일 권한/소유자 문제 발견")
                for item in issues[:5]:
                    result['details'].append(f"  - {item}")
                result['recommendations'].append("환경파일 소유자 및 권한을 적절히 설정")
            else:
                result['details'].append("[OS] 사용자 환경변수 파일 권한: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 사용자 환경변수 파일 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
