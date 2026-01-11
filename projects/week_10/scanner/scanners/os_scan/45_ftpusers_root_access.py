import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command, get_file_stat

def _find_ftpusers(target_url, session):
    candidates = [
        "/etc/ftpusers",
        "/etc/ftpd/ftpusers",
        "/etc/vsftpd/ftpusers",
        "/etc/vsftpd.ftpusers",
    ]
    found = []
    for path in candidates:
        stat = get_file_stat(target_url, session, path)
        if stat:
            found.append(path)
    return found

def _ftp_service_active(target_url, session):
    services = ["vsftpd", "proftpd", "pure-ftpd", "ftp"]
    for svc in services:
        status = execute_command(target_url, session, f"systemctl is-active {svc} 2>&1")
        if "active" in status.lower():
            return True
    return False


def scan(target_url, login_info=None):
    result = {
        'name': 'OS: Ftpusers 파일 설정',
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
            ftpusers_paths = _find_ftpusers(target_url, session)
            if not ftpusers_paths:
                if _ftp_service_active(target_url, session):
                    result['vulnerable'] = True
                    result['details'].append("[OS] ftpusers 파일 없음")
                    result['recommendations'].append("ftpusers 파일에 root 계정 차단 설정 추가")
                else:
                    result['details'].append("[OS] ftpusers 파일 없음 (FTP 미사용)")
            else:
                missing_root_paths = []
                for path in ftpusers_paths:
                    content = execute_command(target_url, session, f"cat {path} 2>&1")
                    has_root = False
                    for line in content.splitlines():
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if line == "root":
                            has_root = True
                            break
                    if has_root:
                        result['details'].append(f"[OS] {path}에 root 차단 설정 존재 (양호)")
                    else:
                        missing_root_paths.append(path)

                if missing_root_paths:
                    result['vulnerable'] = True
                    result['details'].append(f"[OS] root 차단 설정 없음: {', '.join(missing_root_paths)}")
                    result['recommendations'].append("ftpusers에 root 계정 추가")

        if not result['recommendations']:
            result['recommendation'] = '안전 - ftpusers 설정이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
