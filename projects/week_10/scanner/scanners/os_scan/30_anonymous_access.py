import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _has_line(content, pattern):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 공유 서비스 익명 접근 제한',
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
            if _has_line(passwd_content, r'^(ftp|anonymous):'):
                result['vulnerable'] = True
                result['details'].append("[OS] ftp 또는 anonymous 계정 존재")
                result['recommendations'].append("익명 계정 삭제 또는 비활성화")

            vsftpd_conf = execute_command(target_url, session, "cat /etc/vsftpd.conf 2>/dev/null")
            vsftpd_conf_alt = execute_command(target_url, session, "cat /etc/vsftpd/vsftpd.conf 2>/dev/null")
            vsftpd_content = vsftpd_conf if vsftpd_conf.strip() else vsftpd_conf_alt
            if _has_line(vsftpd_content, r'anonymous_enable\\s*=\\s*YES'):
                result['vulnerable'] = True
                result['details'].append("[OS] vsftpd anonymous_enable 활성화")
                result['recommendations'].append("vsftpd anonymous_enable=NO 설정")

            exports_content = execute_command(target_url, session, "cat /etc/exports 2>/dev/null")
            if _has_line(exports_content, r'anonuid|anongid'):
                result['vulnerable'] = True
                result['details'].append("[OS] NFS 익명 접근 설정 존재")
                result['recommendations'].append("NFS 익명 접근 설정 제거")

            smb_conf = execute_command(target_url, session, "cat /etc/samba/smb.conf 2>/dev/null")
            if _has_line(smb_conf, r'guest\\s*ok'):
                result['vulnerable'] = True
                result['details'].append("[OS] Samba guest ok 설정 존재")
                result['recommendations'].append("Samba guest ok 설정 비활성화")

            proftpd_conf = execute_command(target_url, session, "cat /etc/proftpd.conf 2>/dev/null")
            proftpd_conf_alt = execute_command(target_url, session, "cat /etc/proftpd/proftpd.conf 2>/dev/null")
            proftpd_content = proftpd_conf if proftpd_conf.strip() else proftpd_conf_alt
            if _has_line(proftpd_content, r'<Anonymous'):
                result['vulnerable'] = True
                result['details'].append("[OS] proftpd Anonymous 설정 존재")
                result['recommendations'].append("proftpd Anonymous 설정 제거")

            if not result['vulnerable']:
                result['details'].append("[OS] 익명 접근 설정 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 공유 서비스 익명 접근이 제한됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
