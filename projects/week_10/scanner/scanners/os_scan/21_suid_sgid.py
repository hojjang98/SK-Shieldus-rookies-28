import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: SUID, SGID 설정 파일 점검',
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
            output = execute_command(
                target_url,
                session,
                "find / -xdev \\( -path /var/lib/docker -o -path /var/lib/docker/* \\) -prune "
                "-o -user root -type f \\( -perm -04000 -o -perm -02000 \\) "
                "-printf '%M %n %u %g %s %TY-%Tm-%Td %TH:%TM %p\\n' 2>/dev/null | head -20 2>&1"
            )
            if output.strip():
                result['vulnerable'] = True
                result['details'].append("[OS] SUID/SGID 설정 파일 발견 (점검 필요)")
                for line in output.splitlines():
                    line = line.strip()
                    if line:
                        result['details'].append(line)
                result['recommendations'].append("불필요한 SUID/SGID 파일 권한 제거")
            else:
                result['details'].append("[OS] SUID/SGID 설정 파일 없음 (양호)")

        if not result['recommendations']:
            result['recommendation'] = '안전 - SUID/SGID 설정이 적절히 관리됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
