import requests

def scan(target_url):
    result = {
        'name': 'CSRF (Cross-Site Request Forgery)',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # CSRF 토큰 발급 여부 확인
        csrf_token_result = test_csrf_token(target_url)
        if csrf_token_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(csrf_token_result['detail'])
            result['recommendations'].append("Spring Security CSRF 보호 활성화")
        
        # POST 요청 시 CSRF 검증 여부 확인
        critical_action_result = test_critical_actions(target_url)
        if critical_action_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(critical_action_result['detail'])
            result['recommendations'].append("POST 요청에 CSRF 토큰 추가")
        
        # SameSite 쿠키 설정 확인
        samesite_result = check_samesite_cookie(target_url)
        if samesite_result['vulnerable']:
            result['details'].append(samesite_result['detail'])
            result['recommendations'].append("SameSite=Strict 쿠키 속성 설정")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - CSRF 보호가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def test_csrf_token(target_url):
    # 주요 폼 페이지에서 CSRF 토큰(_csrf) 존재 여부 확인
    result = {'vulnerable': False, 'detail': ''}
    form_pages = ['/board/write', '/user/mypage', '/support/ticket']
    session = requests.Session()
    
    for page in form_pages:
        try:
            url = f"{target_url}{page}"
            response = session.get(url, timeout=5)
            
            if response.status_code == 200:
                has_csrf = '_csrf' in response.text or 'csrf-token' in response.text
                if not has_csrf:
                    result['vulnerable'] = True
                    result['detail'] = f"[Dynamic] CSRF 토큰 미사용: {page}"
                    return result
        except:
            pass
    
    return result

def test_critical_actions(target_url):
    # 토큰 없이 중요 정보 수정(POST) 요청을 보내 방어 동작 확인
    result = {'vulnerable': False, 'detail': ''}
    session = requests.Session()
    
    try:
        write_url = f"{target_url}/user/profile"
        data = {'nickname': 'test'}
        response = session.post(write_url, data=data, timeout=5)
        
        if response.status_code == 200:
            result['vulnerable'] = True
            result['detail'] = "[Dynamic] CSRF 보호 없음: /user/profile (토큰 없이 작업 수행 가능)"
    except:
        pass
    
    return result

def check_samesite_cookie(target_url):
    # 쿠키 헤더에 SameSite 속성이 설정되어 있는지 확인
    result = {'vulnerable': False, 'detail': ''}
    
    try:
        response = requests.get(target_url, timeout=5)
        for cookie in response.cookies:
            if 'samesite' not in str(cookie).lower():
                result['vulnerable'] = True
                result['detail'] = "[Header] SameSite 쿠키 속성 미설정"
                return result
    except:
        pass
    
    return result