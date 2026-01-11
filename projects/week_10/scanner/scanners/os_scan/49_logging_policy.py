import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _has_logging_rules(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if "/var/log" in line or re.search(r'\\s+@', line):
            return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 정책에 따른 시스템 로깅 설정',
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
            rsyslog_conf = execute_command(target_url, session, "cat /etc/rsyslog.conf 2>/dev/null")
            rsyslog_default = execute_command(target_url, session, "cat /etc/rsyslog.d/default.conf 2>/dev/null")
            rsyslog_default_ubuntu = execute_command(target_url, session, "cat /etc/rsyslog.d/50-default.conf 2>/dev/null")
            syslog_conf = execute_command(target_url, session, "cat /etc/syslog.conf 2>/dev/null")

            content = ""
            for candidate in [rsyslog_conf, rsyslog_default, rsyslog_default_ubuntu, syslog_conf]:
                if candidate.strip():
                    content += "\n" + candidate

            if not content.strip():
                result['vulnerable'] = True
                result['details'].append("[OS] 로깅 설정 파일이 없음")
                result['recommendations'].append("로깅 정책 설정 필요")
            elif _has_logging_rules(content):
                result['details'].append("[OS] 로깅 정책 설정: 양호")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] 로깅 정책 설정 미흡")
                result['recommendations'].append("로깅 정책 설정 확인")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 로깅 정책이 설정됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
