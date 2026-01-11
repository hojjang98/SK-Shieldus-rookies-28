import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_passwd

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 홈 디렉토리 존재 여부',
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
            missing_homes = []

            for entry in entries:
                home_dir = entry['home']
                if not home_dir or home_dir in ["/", "/nonexistent"]:
                    continue
                if not home_dir.startswith("/home/"):
                    continue
                check = execute_command(target_url, session, f"test -d {home_dir} && echo ok || echo missing 2>&1")
                if "missing" in check:
                    missing_homes.append(f"{entry['name']}:{home_dir}")

            if missing_homes:
                result['vulnerable'] = True
                result['details'].append(f"[OS] 홈 디렉토리 없음: {', '.join(missing_homes)}")
                result['recommendations'].append("홈 디렉토리 생성 또는 계정 정리")
            else:
                result['details'].append("[OS] 홈 디렉토리 존재 여부: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 홈 디렉토리가 모두 존재함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
