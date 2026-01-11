import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _find_line(content, prefix, module_names):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(prefix) and any(name in line for name in module_names):
            return line
    return None

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 계정 잠금 임계값 설정',
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
            common_auth = execute_command(target_url, session, "cat /etc/pam.d/common-auth 2>&1")
            common_account = execute_command(target_url, session, "cat /etc/pam.d/common-account 2>&1")
            faillock_conf = execute_command(target_url, session, "cat /etc/security/faillock.conf 2>/dev/null")
            module_names = ["pam_tally.so", "pam_tally2.so", "pam_faillock.so"]

            auth_line = _find_line(common_auth, "auth", module_names)
            account_line = _find_line(common_auth, "account", module_names)
            if not account_line:
                account_line = _find_line(common_account, "account", ["pam_faillock.so"])

            if not auth_line:
                result['vulnerable'] = True
                result['details'].append("[OS] pam_tally/pam_tally2 auth 설정이 없음")
                result['recommendations'].append("common-auth에 pam_tally(2).so deny=10 unlock_time=120 no_magic_root 설정 추가")
            else:
                deny_match = re.search(r'deny=(\\d+)', auth_line)
                unlock_match = re.search(r'unlock_time=(\\d+)', auth_line)
                if not deny_match and "pam_faillock.so" in auth_line:
                    deny_match = re.search(r'^\\s*deny\\s*=\\s*(\\d+)', faillock_conf, re.MULTILINE)
                if not unlock_match and "pam_faillock.so" in auth_line:
                    unlock_match = re.search(r'^\\s*unlock_time\\s*=\\s*(\\d+)', faillock_conf, re.MULTILINE)
                no_magic_root = "no_magic_root" in auth_line
                if "pam_faillock.so" in auth_line:
                    no_magic_root = no_magic_root or ("even_deny_root" in auth_line) or ("even_deny_root" in faillock_conf)

                if deny_match and int(deny_match.group(1)) >= 10:
                    result['details'].append(f"[OS] deny 값: 양호 ({deny_match.group(1)})")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] deny 값 설정이 미흡함")
                    result['recommendations'].append("deny 값을 10 이상으로 설정")

                if unlock_match and int(unlock_match.group(1)) >= 120:
                    result['details'].append(f"[OS] unlock_time 값: 양호 ({unlock_match.group(1)})")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] unlock_time 값 설정이 미흡함")
                    result['recommendations'].append("unlock_time 값을 120 이상으로 설정")

                if no_magic_root:
                    result['details'].append("[OS] no_magic_root 설정: 양호")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] no_magic_root 설정이 없음")
                    result['recommendations'].append("no_magic_root 설정 추가")

            if not account_line:
                result['vulnerable'] = True
                result['details'].append("[OS] pam_tally/pam_tally2 account 설정이 없음")
                result['recommendations'].append("account required pam_tally(2).so no_magic_root reset 설정 추가")
            else:
                if "no_magic_root" in account_line and "reset" in account_line:
                    result['details'].append("[OS] account 설정: 양호")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] account 설정이 미흡함")
                    result['recommendations'].append("account 줄에 no_magic_root reset 옵션 추가")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 계정 잠금 임계값이 적절히 설정되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
