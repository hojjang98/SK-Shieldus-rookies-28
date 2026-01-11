import requests
import os
import json
import platform
from urllib.parse import urljoin

def scan(target_url, crawl_result):
    result = {
        'name': '파일 전송 취약점',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Blackbox] 파일 업로드 취약점 테스트
        upload_result = test_file_upload(target_url, crawl_result)
        if upload_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(upload_result['details'])
            result['recommendations'].extend(upload_result['recommendations'])
        
        # [Blackbox] 파일 다운로드 경로 조작 테스트
        download_result = test_path_traversal_download(target_url, crawl_result)
        if download_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(download_result['details'])
            result['recommendations'].extend(download_result['recommendations'])
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 파일 전송 보안이 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def test_file_upload(target_url, crawl_result):
    """악성 파일 업로드 테스트"""
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    
    # 로그인 정보 로드
    login_info = load_login_info()
    
    # 업로드 엔드포인트 목록
    upload_endpoints = [
        '/upload',
        '/file/upload',
        '/board/upload',
        '/libs/upload',
        '/employee/upload',
        '/board/write',
    ]
    
    # OS별 위험한 확장자
    windows_dangerous = [
        ('malware.exe', b'MZ\x90\x00' + b'\x00' * 60, 'application/octet-stream'),
        ('script.ps1', b'Write-Host "test"', 'text/plain'),
        ('batch.bat', b'@echo off\necho test', 'application/octet-stream'),
    ]
    
    linux_dangerous = [
        ('shell.sh', b'#!/bin/bash\necho test', 'application/x-sh'),
        ('Malicious.java', b'public class Malicious { }', 'text/plain'),
        ('webshell.jsp', b'<% out.println("test"); %>', 'text/plain'),
    ]
    
    # 현재 OS 확인
    current_os = platform.system().lower()
    if 'windows' in current_os:
        test_files = windows_dangerous
    else:
        test_files = linux_dangerous
    
    # 인증된 세션 생성
    session = requests.Session()
    
    # 로그인 시도
    if login_info:
        try:
            session.post(f"{target_url}/login", data=login_info, timeout=5)
        except:
            pass
    
    # crawl_result 쿠키도 추가
    if crawl_result and hasattr(crawl_result, 'cookies'):
        session.cookies.update(crawl_result.cookies)
    
    for endpoint in upload_endpoints:
        url = urljoin(target_url, endpoint)
        
        for filename, content, mime_type in test_files:
            try:
                # multipart/form-data로 파일 업로드
                files = {'file': (filename, content, mime_type)}
                data = {'title': 'test', 'content': 'test', 'description': 'test'}
                
                response = session.post(url, files=files, data=data, timeout=10, allow_redirects=True)
                
                # 업로드 성공 확인
                if response.status_code in [200, 201, 302]:
                    response_lower = response.text.lower()
                    
                    # 성공 지표 확인
                    success_indicators = [
                        'success', '성공', 'uploaded', '업로드',
                        'complete', '완료', 'saved', '저장',
                        filename.lower(), os.path.splitext(filename)[0].lower()
                    ]
                    
                    # 실패 지표 확인
                    failure_indicators = [
                        'not allowed', '허용되지 않', 'forbidden', 'denied',
                        'invalid', '유효하지 않', 'error'
                    ]
                    
                    has_success = any(indicator in response_lower for indicator in success_indicators)
                    has_failure = any(indicator in response_lower for indicator in failure_indicators)
                    
                    # 성공 표시 있거나, 실패 표시 없으면 취약으로 판단
                    if has_success or (not has_failure and response.status_code == 200):
                        result['vulnerable'] = True
                        ext = os.path.splitext(filename)[1]
                        result['details'].append(
                            f"[Blackbox] 위험한 파일 업로드 가능: {filename} ({endpoint}) - {response.status_code}"
                        )
                        result['recommendations'].append(
                            f"실행 가능한 확장자({ext}) 업로드 차단"
                        )
                        result['recommendations'].append("파일명 난수화 및 확장자 화이트리스트 적용")
                        return result
                            
            except requests.RequestException:
                continue
    
    return result

def load_login_info():
    """config.json에서 로그인 정보 로드"""
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('guest_login') or config.get('normal_login') or config.get('login')
    except:
        pass
    return None

def test_path_traversal_download(target_url, crawl_result):
    """파일 다운로드 경로 조작 테스트"""
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    
    # 다운로드 엔드포인트
    download_endpoints = [
        '/download',
        '/file/download',
        '/files/download',
        '/libs/download',
        '/board/download'
    ]
    
    # 경로 조작 페이로드
    traversal_payloads = [
        # Windows
        ('..\\..\\..\\Windows\\win.ini', ['[fonts]', '[extensions]']),
        ('..\\..\\..\\..\\Windows\\system.ini', ['[drivers]', '[boot]']),
        # Linux
        ('../../../etc/passwd', ['root:', 'bin:', 'daemon:']),
        ('../../../../etc/passwd', ['root:x:0:0:']),
        ('../../../etc/hosts', ['localhost', '127.0.0.1']),
        # 설정 파일
        ('../application.properties', ['spring', 'datasource', 'password']),
        ('../../application.yml', ['spring:', 'datasource:']),
        ('../config/database.yml', ['host:', 'password:']),
    ]
    
    session = requests.Session()
    if crawl_result and hasattr(crawl_result, 'cookies'):
        session.cookies.update(crawl_result.cookies)
    
    for endpoint in download_endpoints:
        url = urljoin(target_url, endpoint)
        
        for payload, markers in traversal_payloads:
            # 다양한 파라미터명 시도
            param_names = ['path', 'file', 'filename', 'filepath', 'name']
            
            for param_name in param_names:
                try:
                    # GET 요청
                    params = {param_name: payload}
                    response = session.get(url, params=params, timeout=5)
                    
                    if response.status_code == 200:
                        response_lower = response.text.lower()
                        
                        # 시스템 파일 내용 확인
                        if any(marker.lower() in response_lower for marker in markers):
                            result['vulnerable'] = True
                            file_type = 'Windows 시스템 파일' if 'win.ini' in payload or 'system.ini' in payload else \
                                       '설정 파일' if 'application' in payload or 'database' in payload else \
                                       'Linux 시스템 파일'
                            
                            result['details'].append(
                                f"[Blackbox] 경로 조작으로 {file_type} 접근 성공: {endpoint}?{param_name}={payload}"
                            )
                            result['recommendations'].append("경로 정규화(normalize) 및 상위 디렉토리 이동(..) 차단")
                            result['recommendations'].append("다운로드 가능 경로를 화이트리스트로 제한")
                            return result
                            
                except requests.RequestException:
                    continue
    
    return result