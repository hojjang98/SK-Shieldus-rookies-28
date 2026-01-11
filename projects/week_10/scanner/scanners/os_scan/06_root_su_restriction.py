import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, parse_group
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, parse_group

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 사용자 계정 su 기능 제한',
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
            su_config = execute_command(target_url, session, "cat /etc/pam.d/su 2>&1")
            wheel_line = None
            for line in su_config.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if "pam_wheel.so" in line and line.startswith("auth"):
                    wheel_line = line
                    break

            if not wheel_line:
                result['vulnerable'] = True
                result['details'].append("[OS] pam_wheel.so 설정이 없음")
                result['recommendations'].append("/etc/pam.d/su에 pam_wheel.so 설정 추가")
            else:
                group_content = execute_command(target_url, session, "cat /etc/group 2>&1")
                groups = parse_group(group_content)
                group_names = {g['name'] for g in groups if g['name']}

                group_name = None
                group_match = re.search(r'group=([\\w-]+)', wheel_line)
                if group_match:
                    group_name = group_match.group(1)
                else:
                    if "wheel" in group_names:
                        group_name = "wheel"
                    elif "sudo" in group_names:
                        group_name = "sudo"

                group_entry = next((g for g in groups if g['name'] == group_name), None) if group_name else None

                if group_entry and group_entry['members']:
                    result['details'].append(f"[OS] su 제한 그룹 설정: 양호 ({group_name})")
                else:
                    result['vulnerable'] = True
                    if group_name:
                        result['details'].append(f"[OS] su 제한 그룹 미구성: {group_name}")
                        result['recommendations'].append(f"{group_name} 그룹에 관리자 계정 추가")
                    else:
                        result['details'].append("[OS] su 제한 그룹을 확인할 수 없음")
                        result['recommendations'].append("su 제한 그룹 설정 확인")

        if not result['recommendations']:
            result['recommendation'] = '안전 - su 명령이 특정 그룹으로 제한되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
