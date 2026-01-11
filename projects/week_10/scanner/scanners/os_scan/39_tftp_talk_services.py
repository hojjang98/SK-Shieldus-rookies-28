import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _inetd_enabled(content, service_names):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if any(re.match(r'^' + name + r'\\b', line) for name in service_names):
            return True
    return False

def _xinetd_enabled(content):
    has_disable = False
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith("disable"):
            has_disable = True
            if "no" in line:
                return True
    return not has_disable

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: tftp/talk 서비스 비활성화',
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
            services = ["tftp", "talk", "ntalk"]
            inetd_conf = execute_command(target_url, session, "cat /etc/inetd.conf 2>/dev/null")
            inetd_on = _inetd_enabled(inetd_conf, services)

            xinetd_on = False
            for svc in services:
                svc_conf = execute_command(target_url, session, f"cat /etc/xinetd.d/{svc} 2>/dev/null")
                if svc_conf.strip() and _xinetd_enabled(svc_conf):
                    xinetd_on = True
                    break

            systemd_output = execute_command(
                target_url,
                session,
                "systemctl list-units --type=service --state=active | grep -E 'tftp|talk|ntalk' 2>&1"
            )
            systemd_on = bool(systemd_output.strip())

            if inetd_on or xinetd_on or systemd_on:
                result['vulnerable'] = True
                result['details'].append("[OS] tftp/talk 서비스 활성화됨")
                result['recommendations'].append("tftp/talk 서비스 비활성화")
            else:
                result['details'].append("[OS] tftp/talk 서비스 비활성화: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - tftp/talk 서비스가 비활성화됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
