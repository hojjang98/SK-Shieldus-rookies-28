import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: .rhosts/hosts.equiv 사용 금지',
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
            hosts_equiv_stat = get_file_stat(target_url, session, "/etc/hosts.equiv")
            if hosts_equiv_stat:
                owner = hosts_equiv_stat['owner']
                perm = hosts_equiv_stat['perm']
                if owner != "root":
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/hosts.equiv 소유자 취약 (현재: {owner})")
                    result['recommendations'].append("/etc/hosts.equiv 소유자를 root로 설정")
                try:
                    perm_val = int(perm)
                    if perm_val <= 600:
                        result['details'].append(f"[OS] /etc/hosts.equiv 권한: 양호 ({perm})")
                    else:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] /etc/hosts.equiv 권한: 취약 ({perm})")
                        result['recommendations'].append("/etc/hosts.equiv 권한을 600 이하로 설정")
                except ValueError:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/hosts.equiv 권한 확인 실패 ({perm})")
                    result['recommendations'].append("/etc/hosts.equiv 권한을 600 이하로 설정")
            else:
                result['details'].append("[OS] /etc/hosts.equiv 파일 없음 (양호)")

            rhosts_output = execute_command(
                target_url,
                session,
                "find /home /root -name .rhosts -type f 2>/dev/null | head -10 2>&1"
            )
            if rhosts_output.strip():
                result['vulnerable'] = True
                result['details'].append("[OS] .rhosts 파일 발견")
                result['details'].append(rhosts_output.strip())
                result['recommendations'].append(".rhosts 파일 제거")
            else:
                result['details'].append("[OS] .rhosts 파일 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - .rhosts/hosts.equiv 사용 금지'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
