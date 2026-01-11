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
        'name': 'OS: 안전한 비밀번호 암호화 알고리즘 사용',
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
            login_defs = execute_command(target_url, session, "cat /etc/login.defs 2>&1")
            encrypt_method = None
            for line in login_defs.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith("ENCRYPT_METHOD"):
                    parts = line.split()
                    if len(parts) >= 2:
                        encrypt_method = parts[1].upper()
                        break

            if encrypt_method in ["SHA512", "SHA256", "SHA-512", "SHA-256", "YESCRYPT"]:
                result['details'].append(f"[OS] ENCRYPT_METHOD: 양호 ({encrypt_method})")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] ENCRYPT_METHOD 설정이 미흡함")
                result['recommendations'].append("ENCRYPT_METHOD를 SHA-2 이상으로 설정")

            common_password = execute_command(target_url, session, "cat /etc/pam.d/common-password 2>&1")
            pam_unix_line = None
            for line in common_password.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if "pam_unix.so" in line and line.startswith("password"):
                    pam_unix_line = line
                    break

            algo_ok = False
            if pam_unix_line:
                lower_line = pam_unix_line.lower()
                if "sha512" in lower_line or "sha256" in lower_line or "yescrypt" in lower_line:
                    algo_ok = True
                elif encrypt_method in ["SHA512", "SHA256", "SHA-512", "SHA-256", "YESCRYPT"]:
                    algo_ok = True

            if pam_unix_line and algo_ok:
                result['details'].append("[OS] pam_unix.so SHA-2/YESCRYPT 설정: 양호")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] pam_unix.so SHA-2/YESCRYPT 설정이 없음")
                result['recommendations'].append("pam_unix.so에 SHA-2 이상 알고리즘 설정 추가")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 안전한 비밀번호 암호화 알고리즘이 설정됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
