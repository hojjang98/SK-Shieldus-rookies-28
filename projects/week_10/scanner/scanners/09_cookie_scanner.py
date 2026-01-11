import requests
import os
import json

def scan(target_url, login_info=None):
    result = {
        'name': '쿠키 변조',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Blackbox] 실제 쿠키 값 변조를 통한 권한 상승 테스트 (우선)
        guest_login = load_guest_login()
        test_login = guest_login if guest_login else login_info
        
        if test_login:
            manipulation_result = test_cookie_manipulation(target_url, test_login)
            if manipulation_result['vulnerable']:
                result['vulnerable'] = True
                result['details'].append(manipulation_result['detail'])
                result['recommendations'].append("쿠키 서명(HMAC) 구현 또는 세션 기반 권한 관리")
        
        # [Whitebox] 쿠키 보안 설정(HttpOnly, Secure 등) 확인 (항상 실행)
        whitebox_result = scan_cookie_security_config()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        # [Whitebox] 소스 코드 상 쿠키 기반 권한 검증 로직 확인 (항상 실행)
        code_result = scan_cookie_based_authorization()
        if code_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(code_result['details'])
            result['recommendations'].extend(code_result['recommendations'])
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 쿠키 보안이 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_guest_login():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('guest_login', None)
    return None

def scan_cookie_security_config():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    config_paths = ['./application.properties', './application.yaml', '../application.properties']
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'http-only' not in content.lower():
                        result['vulnerable'] = True
                        result['details'].append("[Whitebox] 설정 파일 내 HttpOnly 플래그 미설정")
                        result['recommendations'].append("HttpOnly 플래그 활성화")
                    if 'secure' not in content.lower() and 'https' in content:
                        result['details'].append("[Whitebox] 설정 파일 내 Secure 플래그 미설정")
                    if 'samesite' not in content.lower():
                        result['details'].append("[Whitebox] 설정 파일 내 SameSite 속성 미설정")
            except: pass
    return result

def scan_cookie_based_authorization():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    project_path = '.'
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            project_path = json.load(f).get('project_path', '.')
    
    java_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java') and 'Controller' in file:
                java_files.append(os.path.join(root, file))
    
    for java_file in java_files:
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Cookie' in content and 'role' in content.lower():
                    # 쿠키 값을 사용하는데 검증(HMAC/Verify) 로직이 없는 경우 탐지
                    if not any(k in content for k in ['verify', 'HMAC', 'signature', 'sign']):
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {os.path.basename(java_file)} - 검증 없는 쿠키 기반 권한 제어 의심")
                        result['recommendations'].append("쿠키 값 변조 방지(서명) 적용")
        except: continue
    return result

def test_cookie_manipulation(target_url, login_info):
    """쿠키 값 변조를 통한 권한 상승 테스트"""
    result = {'vulnerable': False, 'detail': ''}
    
    if not login_info:
        return result
    
    try:
        session = requests.Session()
        
        # 1. 로그인하여 기본 쿠키 획득
        login_response = session.post(f"{target_url}/login", data=login_info, timeout=5, allow_redirects=True)
        original_cookies = session.cookies.get_dict()
        
        # 로그인 실패 시 종료
        if not original_cookies:
            return result
        
        # 2. 테스트할 관리자 페이지 목록
        admin_pages = ['/admin/system', '/admin/dna/applications', '/admin']
        
        # 3. 테스트할 role 값들
        test_roles = ['admin', 'administrator', 'root', 'ADMIN', 'Admin']
        
        for admin_page in admin_pages:
            for new_role in test_roles:
                try:
                    # 새로운 세션 생성
                    test_session = requests.Session()
                    
                    # 기존 쿠키 전부 복사
                    for cookie_name, cookie_value in original_cookies.items():
                        test_session.cookies.set(cookie_name, cookie_value)
                    
                    # role 쿠키 설정/변조
                    test_session.cookies.set('role', new_role)
                    
                    # 관리자 페이지 접근 시도
                    res = test_session.get(f"{target_url}{admin_page}", timeout=5, allow_redirects=True)
                    
                    # 성공 조건 체크
                    if res.status_code == 200:
                        response_text_lower = res.text.lower()
                        
                        # 실패 키워드 확인
                        failure_keywords = [
                            'access denied', '접근 거부', '접근이 거부',
                            'forbidden', 'unauthorized', '권한이 없',
                            'login', '로그인', 'sign in'
                        ]
                        
                        has_failure = any(keyword in response_text_lower for keyword in failure_keywords)
                        
                        # 성공 키워드 확인 (관리자 페이지 특징)
                        success_keywords = ['admin', '관리자', 'system', 'dashboard', 'users', 'settings']
                        has_success = any(keyword in response_text_lower for keyword in success_keywords)
                        
                        # 충분한 컨텐츠가 있고, 실패 메시지가 없으면 취약
                        if len(res.text) > 500 and not has_failure and has_success:
                            result['vulnerable'] = True
                            result['detail'] = f"[Blackbox] 쿠키 변조로 관리자 페이지 접근 성공: {admin_page} (role={new_role})"
                            return result
                            
                except requests.RequestException:
                    continue
                    
    except Exception:
        pass
    
    return result