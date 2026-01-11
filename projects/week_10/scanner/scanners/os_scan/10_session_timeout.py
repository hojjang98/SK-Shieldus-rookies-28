import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 세션 종료 시간 설정',
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
            profile_content = execute_command(
                target_url,
                session,
                "cat /etc/profile /etc/profile.d/*.sh /etc/bash.bashrc 2>/dev/null"
            )
            tmout_value = None
            for line in profile_content.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                match = re.match(r'^(export\\s+)?TMOUT\\s*=\\s*(\\d+)', line)
                if match:
                    tmout_value = int(match.group(2))

            if tmout_value is None:
                result['vulnerable'] = True
                result['details'].append("[OS] TMOUT 설정이 없음")
                result['recommendations'].append("TMOUT을 600 이하로 설정")
            elif tmout_value <= 600:
                result['details'].append(f"[OS] TMOUT 설정: 양호 ({tmout_value}초)")
            else:
                result['vulnerable'] = True
                result['details'].append(f"[OS] TMOUT 설정: 취약 ({tmout_value}초)")
                result['recommendations'].append("TMOUT을 600 이하로 설정")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 세션 종료 시간이 적절히 설정됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
