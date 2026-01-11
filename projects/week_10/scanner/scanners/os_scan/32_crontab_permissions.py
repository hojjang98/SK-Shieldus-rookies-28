import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, get_file_stat

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: crontab 설정파일 권한 설정 미흡',
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
            targets = [
                "/etc/crontab",
                "/etc/cron.allow",
                "/etc/cron.deny",
                "/etc/at.allow",
                "/etc/at.deny",
            ]
            issues = []
            for path in targets:
                stat = get_file_stat(target_url, session, path)
                if not stat:
                    continue
                owner = stat['owner']
                perm = stat['perm']
                try:
                    perm_val = int(perm)
                except ValueError:
                    perm_val = None

                if owner != "root" or (perm_val is not None and perm_val > 640):
                    issues.append(f"{path} (owner={owner}, perm={perm})")

            if issues:
                result['vulnerable'] = True
                result['details'].append("[OS] cron/at 관련 파일 권한 취약")
                for item in issues[:5]:
                    result['details'].append(f"  - {item}")
                result['recommendations'].append("cron/at 관련 파일 소유자 root 및 권한 640 이하 설정")
            else:
                result['details'].append("[OS] cron/at 관련 파일 권한: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - cron/at 파일 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
