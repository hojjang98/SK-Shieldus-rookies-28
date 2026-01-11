import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: Root 홈, PATH 설정',
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
            path_output = execute_command(target_url, session, "echo $PATH 2>&1")
            path_value = path_output.strip()
            path_parts = path_value.split(':') if path_value else []

            has_dot = False
            if path_parts:
                if path_parts[0] == ".":
                    has_dot = True
                if "." in path_parts[1:]:
                    has_dot = True
                if "" in path_parts:
                    has_dot = True

            if has_dot:
                result['vulnerable'] = True
                result['details'].append(f"[OS] PATH에 현재 디렉터리 포함: {path_value}")
                result['recommendations'].append("PATH에서 현재 디렉터리(.) 제거")
            else:
                result['details'].append("[OS] PATH에 현재 디렉터리가 포함되지 않음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - PATH 설정이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
