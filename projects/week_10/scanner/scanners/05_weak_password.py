import requests
import time

def scan(target_url):
    result = {
        'name': '약한 비밀번호 정책',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # 약한 비밀번호 허용 여부 테스트
        weak_pwd_result = test_weak_password_acceptance(target_url)
        if weak_pwd_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(weak_pwd_result['detail'])
            result['recommendations'].append("비밀번호 복잡도 검증 (최소 8자, 대소문자/숫자/특수문자 포함)")
        
        # Brute Force 방어 테스트
        bruteforce_result = test_bruteforce_protection(target_url)
        if bruteforce_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(bruteforce_result['detail'])
            result['recommendations'].append("Rate Limiting 구현 (IP당 요청 수 제한)")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 비밀번호 정책이 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def test_weak_password_acceptance(target_url):
    # 회원가입 페이지에서 단순한 비밀번호(1234 등)로 가입이 되는지 확인
    result = {'vulnerable': False, 'detail': ''}
    
    weak_passwords = ['1234', '123456', 'password']
    register_endpoints = ['/register', '/join', '/signup']
    
    for register_url in register_endpoints:
        url = f"{target_url}{register_url}"
        
        try:
            # 페이지 존재 여부 확인
            check_response = requests.get(url, timeout=5, allow_redirects=False)
            if check_response.status_code == 404:
                continue
        except:
            continue
        
        for weak_pwd in weak_passwords:
            try:
                session = requests.Session()
                unique_username = f'test_{int(time.time())}'
                
                data = {
                    'username': unique_username,
                    'password': weak_pwd,
                    'email': f'{unique_username}@test.com',
                    'nickname': unique_username
                }
                
                response = session.post(url, data=data, timeout=5, allow_redirects=True)
                
                success_indicators = ['success', '성공', 'welcome', '환영', 'registered']
                
                if response.status_code == 200 and any(indicator in response.text.lower() for indicator in success_indicators):
                    result['vulnerable'] = True
                    result['detail'] = f"[Dynamic] 약한 비밀번호 허용됨 (예: {weak_pwd})"
                    return result
            except:
                pass
    
    return result

def test_bruteforce_protection(target_url):
    # 단시간 내 다수의 로그인 실패 시도 시 차단 여부(Rate Limit) 확인
    result = {'vulnerable': False, 'detail': ''}
    
    login_url = f"{target_url}/login"
    session = requests.Session()
    
    for i in range(20):
        try:
            data = {'username': 'admin', 'password': f'wrong_password_{i}'}
            response = session.post(login_url, data=data, timeout=5)
            
            # 마지막 20번째 시도에서도 차단(429 등)되지 않으면 취약
            if i == 19:
                if response.status_code != 429 and 'lock' not in response.text.lower() and 'block' not in response.text.lower():
                    result['vulnerable'] = True
                    result['detail'] = "[Dynamic] Rate Limiting 없음 (짧은 시간에 20회 요청 가능)"
        except:
            pass
    
    return result