import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 불필요한 automountd 제거',
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
            output = execute_command(
                target_url,
                session,
                "systemctl list-units --type=service --state=active | grep -E 'automount|autofs' 2>&1"
            )
            if output.strip():
                result['vulnerable'] = True
                result['details'].append("[OS] automount/autofs 서비스 활성화됨")
                result['recommendations'].append("불필요한 automount/autofs 서비스 비활성화")
            else:
                result['details'].append("[OS] automount/autofs 서비스 비활성화: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - automount/autofs 서비스가 비활성화됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
