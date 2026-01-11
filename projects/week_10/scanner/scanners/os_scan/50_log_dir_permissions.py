import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 로그 디렉터리 소유자 및 권한 설정',
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
            log_files = execute_command(
                target_url,
                session,
                "find /var/log -maxdepth 1 -type f -printf '%u\\t%g\\t%m\\t%p\\t' 2>/dev/null"
            )
            issues = []
            flattened = log_files.replace("\n", "\t")
            parts = [p for p in flattened.split("\t") if p]
            for idx in range(0, len(parts), 4):
                if idx + 3 >= len(parts):
                    break
                owner = parts[idx].strip()
                perm = parts[idx + 2].strip()
                path = parts[idx + 3].strip()
                if not path:
                    continue
                base_name = os.path.basename(path)
                max_perm = 644
                if base_name.startswith("btmp"):
                    max_perm = 660
                elif base_name.startswith("wtmp") or base_name.startswith("lastlog"):
                    max_perm = 664
                try:
                    perm_val = int(perm)
                except ValueError:
                    perm_val = None
                if owner != "root" or (perm_val is not None and perm_val > max_perm):
                    issues.append(f"{path} (owner={owner}, perm={perm})")

            if issues:
                result['vulnerable'] = True
                result['details'].append("[OS] 로그 파일 소유자/권한 문제 발견")
                for item in issues[:5]:
                    result['details'].append(f"  - {item}")
                result['recommendations'].append("로그 파일 소유자를 root로, 권한을 644 이하로 설정")
            else:
                result['details'].append("[OS] 로그 파일 소유자 및 권한: 양호")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 로그 디렉터리 권한이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
