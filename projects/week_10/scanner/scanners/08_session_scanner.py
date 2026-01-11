import requests
import os
import re

def scan(target_url, login_info=None):
    result = {
        'name': '불충분한 세션 관리',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] 설정 파일에서 세션 타임아웃 및 보안 설정 확인
        whitebox_result = scan_session_config()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        # [Blackbox] 로그아웃 후 세션 무효화 테스트
        logout_result = test_logout_session(target_url, login_info)
        if logout_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(logout_result['detail'])
            result['recommendations'].append("로그아웃 시 세션 무효화 구현")
        
        # [Blackbox] 세션 고정(Session Fixation) 취약점 테스트
        fixation_result = test_session_fixation(target_url, login_info)
        if fixation_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(fixation_result['detail'])
            result['recommendations'].append("로그인 후 세션 ID 재생성")
        
        # [Blackbox] 쿠키 보안 플래그(HttpOnly) 확인
        cookie_result = test_cookie_flags(target_url, login_info)
        if cookie_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(cookie_result['detail'])
            result['recommendations'].append("HttpOnly/Secure 쿠키 플래그 설정")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 세션 관리가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def scan_session_config():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    config_paths = ['./application.properties', '../application.properties']
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 타임아웃 설정 확인 (1800초/30분 초과 시 취약)
                    timeout_match = re.search(r'session\.timeout\s*=\s*(\d+)', content)
                    if timeout_match:
                        timeout_value = int(timeout_match.group(1))
                        if timeout_value > 1800:
                            result['vulnerable'] = True
                            result['details'].append(f"[Whitebox] 세션 타임아웃 과도하게 김: {timeout_value}초")
                            result['recommendations'].append("세션 타임아웃 15분(900초)으로 설정")
                    
                    if 'http-only' not in content.lower():
                        result['details'].append("[Whitebox] 설정 파일 내 HttpOnly 플래그 미설정")
            except: pass
    return result

def test_logout_session(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    session = requests.Session()
    try:
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        # 로그아웃 수행
        session.get(f"{target_url}/logout", timeout=5)
        # 로그아웃 후 보호된 페이지 재접근 시도
        res = session.get(f"{target_url}/user/mypage", timeout=5)
        
        if res.status_code == 200 and 'login' not in res.url:
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 로그아웃 후에도 이전 세션 유효 (세션 무효화 미흡)"
    except: pass
    return result

def test_session_fixation(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    try:
        session = requests.Session()
        # 로그인 전 세션 ID 획득
        session.get(f"{target_url}/", timeout=5)
        cookies_before = session.cookies.get_dict()
        
        # 로그인 수행
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        cookies_after = session.cookies.get_dict()
        
        # 세션 ID가 변하지 않았다면 취약
        if cookies_before == cookies_after and cookies_before:
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 세션 고정 취약: 로그인 전후 세션 ID 동일"
    except: pass
    return result

def test_cookie_flags(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    try:
        session = requests.Session()
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        
        for cookie in session.cookies:
            # requests의 cookie 객체는 has_nonstandard_attr로 플래그 확인 가능
            if not cookie.has_nonstandard_attr('HttpOnly'):
                result['vulnerable'] = True
                result['detail'] = "[Blackbox] 세션 쿠키에 HttpOnly 플래그 미설정"
                return result
    except: pass
    return result