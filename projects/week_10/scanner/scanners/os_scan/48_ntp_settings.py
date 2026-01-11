import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: NTP 및 시각 동기화 설정',
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
            services = ["chronyd", "ntpd", "ntp", "systemd-timesyncd"]
            active = []
            for svc in services:
                status = execute_command(target_url, session, f"systemctl is-active {svc} 2>&1")
                if "active" in status.lower():
                    active.append(svc)

            sync_status = execute_command(target_url, session, "timedatectl show -p NTPSynchronized --value 2>/dev/null")
            if sync_status.strip().lower() == "yes":
                active.append("timedatectl")

            if active:
                result['details'].append(f"[OS] NTP 동기화 서비스 활성화: {', '.join(active)}")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] NTP 동기화 서비스 비활성화")
                result['recommendations'].append("NTP 또는 시각 동기화 서비스 활성화")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 시각 동기화 설정이 적용됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
