import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _get_login_defs_value(content, key):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(key):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1]
    return None

def _get_conf_int(content, key):
    pattern = re.compile(r'^\\s*' + re.escape(key) + r'\\s*=\\s*(-?\\d+)')
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = pattern.match(line)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
    return None

def _has_setting_line(content, keyword):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if keyword in line:
            return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 비밀번호 관리정책 설정',
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
            pass_max_days = _get_login_defs_value(login_defs, "PASS_MAX_DAYS")
            pass_min_days = _get_login_defs_value(login_defs, "PASS_MIN_DAYS")

            if pass_max_days is None:
                result['vulnerable'] = True
                result['details'].append("[OS] PASS_MAX_DAYS 설정이 없음")
                result['recommendations'].append("PASS_MAX_DAYS를 90 이상으로 설정")
            else:
                try:
                    pass_max_days_val = int(pass_max_days)
                    if pass_max_days_val >= 90:
                        result['details'].append(f"[OS] PASS_MAX_DAYS: 양호 (현재값: {pass_max_days_val})")
                    else:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] PASS_MAX_DAYS: 취약 (현재값: {pass_max_days_val})")
                        result['recommendations'].append("PASS_MAX_DAYS를 90 이상으로 설정")
                except ValueError:
                    result['vulnerable'] = True
                    result['details'].append("[OS] PASS_MAX_DAYS 값이 숫자가 아님")
                    result['recommendations'].append("PASS_MAX_DAYS를 90 이상으로 설정")

            if pass_min_days is None:
                result['vulnerable'] = True
                result['details'].append("[OS] PASS_MIN_DAYS 설정이 없음")
                result['recommendations'].append("PASS_MIN_DAYS를 0 이상으로 설정")
            else:
                try:
                    pass_min_days_val = int(pass_min_days)
                    if pass_min_days_val >= 0:
                        result['details'].append(f"[OS] PASS_MIN_DAYS: 양호 (현재값: {pass_min_days_val})")
                    else:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] PASS_MIN_DAYS: 취약 (현재값: {pass_min_days_val})")
                        result['recommendations'].append("PASS_MIN_DAYS를 0 이상으로 설정")
                except ValueError:
                    result['vulnerable'] = True
                    result['details'].append("[OS] PASS_MIN_DAYS 값이 숫자가 아님")
                    result['recommendations'].append("PASS_MIN_DAYS를 0 이상으로 설정")

            pwquality_conf = execute_command(target_url, session, "cat /etc/security/pwquality.conf 2>&1")
            required_settings = {
                "minlen": 8,
                "dcredit": -1,
                "ucredit": -1,
                "lcredit": -1,
                "ocredit": -1,
            }

            for key, expected in required_settings.items():
                value = _get_conf_int(pwquality_conf, key)
                if value is None:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] {key} 설정이 없음")
                    result['recommendations'].append(f"{key}를 {expected} 이상으로 설정")
                elif value >= expected:
                    result['details'].append(f"[OS] {key}: 양호 (현재값: {value})")
                else:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] {key}: 취약 (현재값: {value})")
                    result['recommendations'].append(f"{key}를 {expected} 이상으로 설정")

            common_password = execute_command(target_url, session, "cat /etc/pam.d/common-password 2>&1")
            enforce_in_pwquality = _has_setting_line(pwquality_conf, "enforce_for_root")
            enforce_in_common = _has_setting_line(common_password, "enforce_for_root")
            if enforce_in_pwquality or enforce_in_common:
                result['details'].append("[OS] enforce_for_root: 양호")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] enforce_for_root 설정이 없음")
                result['recommendations'].append("pwquality.conf에 enforce_for_root 추가")

            pwquality_idx = None
            pwhistory_idx = None
            unix_idx = None
            for idx, line in enumerate(common_password.splitlines()):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if "pam_pwquality.so" in line:
                    pwquality_idx = idx
                if "pam_pwhistory.so" in line:
                    pwhistory_idx = idx
                if "pam_unix.so" in line:
                    unix_idx = idx

            if unix_idx is None:
                result['vulnerable'] = True
                result['details'].append("[OS] pam_unix.so 모듈이 없음")
                result['recommendations'].append("/etc/pam.d/common-password 설정 확인")
            else:
                if pwquality_idx is None or pwquality_idx > unix_idx:
                    result['vulnerable'] = True
                    result['details'].append("[OS] pam_pwquality.so 위치가 pam_unix.so보다 뒤에 있음")
                    result['recommendations'].append("pam_pwquality.so를 pam_unix.so 위로 이동")
                else:
                    result['details'].append("[OS] pam_pwquality.so 위치: 양호")

                if pwhistory_idx is None or pwhistory_idx > unix_idx:
                    result['vulnerable'] = True
                    result['details'].append("[OS] pam_pwhistory.so 위치가 pam_unix.so보다 뒤에 있음")
                    result['recommendations'].append("pam_pwhistory.so를 pam_unix.so 위로 이동")
                else:
                    result['details'].append("[OS] pam_pwhistory.so 위치: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 비밀번호 관리정책이 적절히 설정되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
