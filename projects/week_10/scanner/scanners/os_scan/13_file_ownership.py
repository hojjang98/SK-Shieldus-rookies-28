import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, is_local_mode
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, is_local_mode

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 파일 및 디렉터리 소유자 설정',
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
            find_command = (
                "find / -xdev \\( -path /var/lib/docker -o -path /var/lib/docker/* \\) -prune "
                "-o \\( -nouser -o -nogroup \\) -ls 2>/dev/null | head -20 2>&1"
            )
            find_output = execute_command(
                target_url,
                session,
                find_command
            )
            if find_output.strip():
                result['vulnerable'] = True
                result['details'].append("[OS] 소유자 또는 그룹이 없는 파일/디렉터리 발견")
                result['details'].append(find_output.strip())
                result['recommendations'].append("소유자 및 그룹이 없는 파일/디렉터리 정리")
            else:
                result['details'].append("[OS] 소유자/그룹 미지정 파일 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 소유자 및 그룹이 적절히 설정됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
