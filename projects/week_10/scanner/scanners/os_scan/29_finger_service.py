import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _inetd_enabled(content, service_name):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(service_name):
            return True
    return False

def _xinetd_enabled(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith("disable") and "no" in line:
            return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: Finger 서비스 비활성화',
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
            inetd_conf = execute_command(target_url, session, "cat /etc/inetd.conf 2>/dev/null")
            xinetd_finger = execute_command(target_url, session, "cat /etc/xinetd.d/finger 2>/dev/null")

            inetd_on = _inetd_enabled(inetd_conf, "finger")
            xinetd_on = _xinetd_enabled(xinetd_finger) if xinetd_finger.strip() else False

            if inetd_on or xinetd_on:
                result['vulnerable'] = True
                result['details'].append("[OS] Finger 서비스가 활성화되어 있음")
                result['recommendations'].append("Finger 서비스 비활성화 필요")
            else:
                result['details'].append("[OS] Finger 서비스 비활성화: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - Finger 서비스가 비활성화됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
