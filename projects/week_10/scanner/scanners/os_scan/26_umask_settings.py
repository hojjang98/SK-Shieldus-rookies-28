import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _parse_umask_value(content):
    value = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.search(r'\\bumask\\s+(\\d+)', line)
        if match:
            value = match.group(1)
    return value

def _parse_key_value(content, key):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(key):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1]
    return None

def _parse_octal(value):
    try:
        return int(value, 8)
    except Exception:
        return None

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: UMASK 설정 관리',
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
            expected = 0o22

            profile_content = execute_command(target_url, session, "cat /etc/profile 2>&1")
            profile_umask = _parse_umask_value(profile_content)
            profile_umask_val = _parse_octal(profile_umask) if profile_umask else None
            if profile_umask_val is None:
                result['vulnerable'] = True
                result['details'].append("[OS] /etc/profile umask 설정 없음")
                result['recommendations'].append("/etc/profile에 umask 022 이상 설정")
            elif profile_umask_val >= expected:
                result['details'].append(f"[OS] /etc/profile umask: 양호 ({profile_umask})")
            else:
                result['vulnerable'] = True
                result['details'].append(f"[OS] /etc/profile umask: 취약 ({profile_umask})")
                result['recommendations'].append("/etc/profile에 umask 022 이상 설정")

            login_defs = execute_command(target_url, session, "cat /etc/login.defs 2>&1")
            login_umask = _parse_key_value(login_defs, "UMASK")
            login_umask_val = _parse_octal(login_umask) if login_umask else None
            if login_umask_val is None:
                result['vulnerable'] = True
                result['details'].append("[OS] /etc/login.defs UMASK 설정 없음")
                result['recommendations'].append("/etc/login.defs에 UMASK 022 이상 설정")
            elif login_umask_val >= expected:
                result['details'].append(f"[OS] /etc/login.defs UMASK: 양호 ({login_umask})")
            else:
                result['vulnerable'] = True
                result['details'].append(f"[OS] /etc/login.defs UMASK: 취약 ({login_umask})")
                result['recommendations'].append("/etc/login.defs에 UMASK 022 이상 설정")

            vsftpd_conf = execute_command(target_url, session, "cat /etc/vsftpd.conf 2>/dev/null")
            vsftpd_conf_alt = execute_command(target_url, session, "cat /etc/vsftpd/vsftpd.conf 2>/dev/null")
            vsftpd_content = vsftpd_conf if vsftpd_conf.strip() else vsftpd_conf_alt
            if vsftpd_content.strip():
                local_umask_match = re.search(r'local_umask\\s*=\\s*(\\d+)', vsftpd_content)
                local_umask_val = _parse_octal(local_umask_match.group(1)) if local_umask_match else None
                if local_umask_val is None:
                    result['vulnerable'] = True
                    result['details'].append("[OS] vsftpd local_umask 설정 없음")
                    result['recommendations'].append("vsftpd local_umask 022 이상 설정")
                elif local_umask_val >= expected:
                    result['details'].append(f"[OS] vsftpd local_umask: 양호 ({local_umask_match.group(1)})")
                else:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] vsftpd local_umask: 취약 ({local_umask_match.group(1)})")
                    result['recommendations'].append("vsftpd local_umask 022 이상 설정")

            proftpd_conf = execute_command(target_url, session, "cat /etc/proftpd.conf 2>/dev/null")
            proftpd_conf_alt = execute_command(target_url, session, "cat /etc/proftpd/proftpd.conf 2>/dev/null")
            proftpd_content = proftpd_conf if proftpd_conf.strip() else proftpd_conf_alt
            if proftpd_content.strip():
                umask_match = re.search(r'\\bUmask\\s+(\\d+)', proftpd_content)
                umask_val = _parse_octal(umask_match.group(1)) if umask_match else None
                if umask_val is None:
                    result['vulnerable'] = True
                    result['details'].append("[OS] proftpd Umask 설정 없음")
                    result['recommendations'].append("proftpd Umask 022 이상 설정")
                elif umask_val >= expected:
                    result['details'].append(f"[OS] proftpd Umask: 양호 ({umask_match.group(1)})")
                else:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] proftpd Umask: 취약 ({umask_match.group(1)})")
                    result['recommendations'].append("proftpd Umask 022 이상 설정")

        if not result['recommendations']:
            result['recommendation'] = '안전 - UMASK 설정이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
