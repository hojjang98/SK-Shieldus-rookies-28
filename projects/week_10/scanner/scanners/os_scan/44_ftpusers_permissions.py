import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, get_file_stat, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, get_file_stat, execute_command

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
            found.append((path, stat))
    return found

def _ftp_service_active(target_url, session):
    services = ["vsftpd", "proftpd", "pure-ftpd", "ftp"]
    for svc in services:
        status = execute_command(target_url, session, f"systemctl is-active {svc} 2>&1")
        if "active" in status.lower():
            return True
    return False

def _find_user_list(target_url, session):
    candidates = [
        "/etc/vsftpd.user_list",
        "/etc/vsftpd/user_list",
    ]
    found = []
    for path in candidates:
        stat = get_file_stat(target_url, session, path)
        if stat:
            found.append((path, stat))
    return found

def _read_vsftpd_config(target_url, session):
    vsftpd_conf = execute_command(target_url, session, "cat /etc/vsftpd.conf 2>/dev/null")
    vsftpd_conf_alt = execute_command(target_url, session, "cat /etc/vsftpd/vsftpd.conf 2>/dev/null")
    content = vsftpd_conf if vsftpd_conf.strip() else vsftpd_conf_alt
    return content

def _get_vsftpd_option(content, key):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith(key):
            parts = line.split("=", 1)
            if len(parts) == 2:
                return parts[1].strip().lower()
            return None
    return None

def _has_non_comment_lines(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        return True
    return False

def _read_proftpd_config(target_url, session):
    proftpd_conf = execute_command(target_url, session, "cat /etc/proftpd.conf 2>/dev/null")
    proftpd_conf_alt = execute_command(target_url, session, "cat /etc/proftpd/proftpd.conf 2>/dev/null")
    content = proftpd_conf if proftpd_conf.strip() else proftpd_conf_alt
    return content

def _get_proftpd_option(content, key):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith(key.lower()):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1].strip().lower()
    return None

def _limit_login_allows(content):
    in_block = False
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith("<limit login"):
            in_block = True
            continue
        if in_block and line.lower().startswith("</limit"):
            in_block = False
            continue
        if in_block:
            lower = line.lower()
            if lower.startswith("allowuser"):
                return True
            if lower.startswith("allow") and "from" in lower:
                return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: FTP 접근 제어 설정',
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
            ftpusers_files = _find_ftpusers(target_url, session)
            if not ftpusers_files:
                if _ftp_service_active(target_url, session):
                    result['vulnerable'] = True
                    result['details'].append("[OS] ftpusers 파일 없음")
                    result['recommendations'].append("ftpusers 파일 생성 및 권한 설정")
                else:
                    result['details'].append("[OS] ftpusers 파일 없음 (FTP 미사용)")
            else:
                for path, stat in ftpusers_files:
                    owner = stat['owner']
                    perm = stat['perm']
                    if owner != "root":
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] {path} 소유자 취약 (현재: {owner})")
                        result['recommendations'].append("ftpusers 소유자를 root로 설정")
                    try:
                        perm_val = int(perm)
                        if perm_val <= 640:
                            result['details'].append(f"[OS] {path} 권한: 양호 ({perm})")
                        else:
                            result['vulnerable'] = True
                            result['details'].append(f"[OS] {path} 권한: 취약 ({perm})")
                            result['recommendations'].append("ftpusers 권한을 640 이하로 설정")
                    except ValueError:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] {path} 권한 확인 실패 ({perm})")
                        result['recommendations'].append("ftpusers 권한을 640 이하로 설정")

            # vsftpd user_list 설정 확인
            vsftpd_content = _read_vsftpd_config(target_url, session)
            if vsftpd_content.strip():
                userlist_enable = _get_vsftpd_option(vsftpd_content, "userlist_enable")
                if userlist_enable == "yes":
                    result['details'].append("[OS] vsftpd userlist_enable=YES 설정: 양호")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] vsftpd userlist_enable 설정이 YES가 아님")
                    result['recommendations'].append("vsftpd userlist_enable=YES 설정")

                userlist_deny = _get_vsftpd_option(vsftpd_content, "userlist_deny")
                if userlist_deny in ["yes", "no"]:
                    result['details'].append(f"[OS] vsftpd userlist_deny 설정: {userlist_deny}")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] vsftpd userlist_deny 설정이 없음")
                    result['recommendations'].append("vsftpd userlist_deny 옵션 설정")

                user_list_files = _find_user_list(target_url, session)
                if not user_list_files:
                    result['vulnerable'] = True
                    result['details'].append("[OS] vsftpd user_list 파일 없음")
                    result['recommendations'].append("user_list 파일 생성 및 권한 설정")
                else:
                    for path, stat in user_list_files:
                        owner = stat['owner']
                        perm = stat['perm']
                        if owner != "root":
                            result['vulnerable'] = True
                            result['details'].append(f"[OS] {path} 소유자 취약 (현재: {owner})")
                            result['recommendations'].append("user_list 소유자를 root로 설정")
                        try:
                            perm_val = int(perm)
                            if perm_val <= 640:
                                result['details'].append(f"[OS] {path} 권한: 양호 ({perm})")
                            else:
                                result['vulnerable'] = True
                                result['details'].append(f"[OS] {path} 권한: 취약 ({perm})")
                                result['recommendations'].append("user_list 권한을 640 이하로 설정")
                        except ValueError:
                            result['vulnerable'] = True
                            result['details'].append(f"[OS] {path} 권한 확인 실패 ({perm})")
                            result['recommendations'].append("user_list 권한을 640 이하로 설정")

                        content = execute_command(target_url, session, f"cat {path} 2>/dev/null")
                        if not _has_non_comment_lines(content):
                            result['vulnerable'] = True
                            result['details'].append(f"[OS] {path} 접근 제한 설정이 없음")
                            result['recommendations'].append("user_list에 접근 허용/차단 사용자 설정")

            # proftpd 설정 확인
            proftpd_content = _read_proftpd_config(target_url, session)
            if proftpd_content.strip():
                use_ftpusers = _get_proftpd_option(proftpd_content, "UseFtpUsers")
                if use_ftpusers == "on":
                    result['details'].append("[OS] proftpd UseFtpUsers on 설정: 양호")
                    if ftpusers_files:
                        has_entries = False
                        for path, _ in ftpusers_files:
                            content = execute_command(target_url, session, f"cat {path} 2>/dev/null")
                            if _has_non_comment_lines(content):
                                has_entries = True
                                break
                        if not has_entries:
                            result['vulnerable'] = True
                            result['details'].append("[OS] ftpusers 접근 제한 설정이 없음")
                            result['recommendations'].append("ftpusers 파일에 접근 차단 사용자 설정")
                elif use_ftpusers == "off":
                    result['details'].append("[OS] proftpd UseFtpUsers off 설정: 확인 필요")
                    if not _limit_login_allows(proftpd_content):
                        result['vulnerable'] = True
                        result['details'].append("[OS] proftpd <Limit LOGIN> 접근 제한 설정 없음")
                        result['recommendations'].append("proftpd.conf에 <Limit LOGIN> 접근 제한 설정 추가")
                else:
                    result['vulnerable'] = True
                    result['details'].append("[OS] proftpd UseFtpUsers 설정이 없음")
                    result['recommendations'].append("proftpd UseFtpUsers 설정 확인")

                for conf_path in ["/etc/proftpd.conf", "/etc/proftpd/proftpd.conf"]:
                    stat = get_file_stat(target_url, session, conf_path)
                    if not stat:
                        continue
                    owner = stat['owner']
                    perm = stat['perm']
                    if owner != "root":
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] {conf_path} 소유자 취약 (현재: {owner})")
                        result['recommendations'].append("proftpd.conf 소유자를 root로 설정")
                    try:
                        perm_val = int(perm)
                        if perm_val <= 640:
                            result['details'].append(f"[OS] {conf_path} 권한: 양호 ({perm})")
                        else:
                            result['vulnerable'] = True
                            result['details'].append(f"[OS] {conf_path} 권한: 취약 ({perm})")
                            result['recommendations'].append("proftpd.conf 권한을 640 이하로 설정")
                    except ValueError:
                        result['vulnerable'] = True
                        result['details'].append(f"[OS] {conf_path} 권한 확인 실패 ({perm})")
                        result['recommendations'].append("proftpd.conf 권한을 640 이하로 설정")

        if not result['recommendations']:
            result['recommendation'] = '안전 - FTP 접근 제어 설정이 적절함'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
