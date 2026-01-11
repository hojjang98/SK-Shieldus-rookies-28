import sys
import os
import re
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: NFS 접근 통제',
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
            stat = get_file_stat(target_url, session, "/etc/exports")
            if not stat:
                result['details'].append("[OS] /etc/exports 파일 없음 (양호)")
            else:
                owner = stat['owner']
                perm = stat['perm']
                if owner != "root":
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/exports 소유자 취약 (현재: {owner})")
                    result['recommendations'].append("/etc/exports 소유자를 root로 설정")
                try:
                    perm_val = int(perm)
                    if perm_val <= 644:
                        result['details'].append(f"[OS] /etc/exports 권한: 양호 ({perm})")
                    else:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] /etc/exports 권한: 취약 ({perm})")
                        result['recommendations'].append("/etc/exports 권한을 644 이하로 설정")
                except ValueError:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] /etc/exports 권한 확인 실패 ({perm})")
                    result['recommendations'].append("/etc/exports 권한을 644 이하로 설정")

                exports_content = execute_command(target_url, session, "cat /etc/exports 2>/dev/null")
                for line in exports_content.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if re.search(r'\\*\\s*\\(rw|\\*\\s*\\(ro', line):
                        result['vulnerable'] = True
                        result['details'].append("[OS] NFS 접근 통제 미흡: 전체 공개 설정 발견")
                        result['recommendations'].append("NFS 접근 대상을 제한된 IP로 설정")
                        break

        if not result['recommendations']:
            result['recommendation'] = '안전 - NFS 접근 통제가 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
