import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _has_banner(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if re.match(r'^ftpd_banner\\s*=\\s*', line):
            return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: FTP 배너 정보 노출 제한',
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
            vsftpd_conf = execute_command(target_url, session, "cat /etc/vsftpd.conf 2>/dev/null")
            vsftpd_conf_alt = execute_command(target_url, session, "cat /etc/vsftpd/vsftpd.conf 2>/dev/null")
            content = vsftpd_conf if vsftpd_conf.strip() else vsftpd_conf_alt

            if not content.strip():
                result['details'].append("[OS] vsftpd 설정 파일 없음 (FTP 미사용)")
            elif _has_banner(content):
                result['details'].append("[OS] ftpd_banner 설정: 양호")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] ftpd_banner 설정이 없음")
                result['recommendations'].append("ftpd_banner를 일반 문구로 설정")

        if not result['recommendations']:
            result['recommendation'] = '안전 - FTP 배너 정보 노출이 제한됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
