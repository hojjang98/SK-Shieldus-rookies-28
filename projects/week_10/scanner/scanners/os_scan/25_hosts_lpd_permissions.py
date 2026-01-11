import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, get_file_stat

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: hosts.lpd 파일 소유자 및 권한 설정',
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
            stat = get_file_stat(target_url, session, "/etc/hosts.lpd")
            if not stat:
                result['details'].append("[OS] /etc/hosts.lpd 파일 없음 (양호)")
            else:
                owner = stat['owner']
                perm = stat['perm']
                if owner != "root":
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/hosts.lpd 소유자 취약 (현재: {owner})")
                    result['recommendations'].append("/etc/hosts.lpd 소유자를 root로 설정")
                else:
                    result['details'].append("[OS] /etc/hosts.lpd 소유자: 양호 (root)")

                try:
                    perm_val = int(perm)
                    if perm_val <= 600:
                        result['details'].append(f"[OS] /etc/hosts.lpd 권한: 양호 ({perm})")
                    else:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] /etc/hosts.lpd 권한: 취약 ({perm})")
                        result['recommendations'].append("/etc/hosts.lpd 권한을 600 이하로 설정")
                except ValueError:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/hosts.lpd 권한 확인 실패 ({perm})")
                    result['recommendations'].append("/etc/hosts.lpd 권한을 600 이하로 설정")

        if not result['recommendations']:
            result['recommendation'] = '안전 - hosts.lpd 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
