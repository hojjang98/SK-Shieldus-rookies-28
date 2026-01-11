import requests
import os
import json

def scan(target_url):
    result = {
        'name': '취약한 비밀번호 복구 절차',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] 비밀번호 재설정 로직(토큰, 만료시간) 코드 분석
        whitebox_result = scan_password_reset_code()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        # [Blackbox] 비밀번호 복구 페이지 존재 여부 확인
        reset_exists = check_password_reset_exists(target_url)
        
        if not reset_exists:
            if not result['vulnerable']:
                result['details'].append("[Blackbox] 비밀번호 복구 기능 미발견")
        else:
            # 기능 존재 시 취약점 점검
            reset_result = test_password_reset_security(target_url)
            if reset_result['vulnerable']:
                result['vulnerable'] = True
                result['details'].append(reset_result['detail'])
                result['recommendations'].append("이메일 인증 토큰 사용")
            
            security_question_result = test_security_questions(target_url)
            if security_question_result['vulnerable']:
                result['vulnerable'] = True
                result['details'].append(security_question_result['detail'])
                result['recommendations'].append("보안 질문 제거 (토큰 기반 재설정만 허용)")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 비밀번호 복구 절차가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_project_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('project_path', '.')
    return '.'

def scan_password_reset_code():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    project_path = load_project_path()
    
    java_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    
    for java_file in java_files:
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 비밀번호 재설정 관련 파일인지 확인
                if 'password' in content.lower() and any(k in content.lower() for k in ['reset', 'recovery', 'find']):
                    filename = os.path.basename(java_file)
                    
                    # 안전한 난수 생성(UUID 등) 여부 확인
                    has_token = any(pattern in content for pattern in ['UUID', 'SecureRandom', 'randomUUID'])
                    if not has_token:
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {filename} - 안전한 토큰 생성 로직 부재")
                        result['recommendations'].append("UUID/SecureRandom으로 안전한 토큰 생성")
                    
                    # 만료 시간 설정 여부 확인
                    has_expiry = any(pattern in content for pattern in ['Timestamp', 'LocalDateTime', 'expiry', 'expire'])
                    if not has_expiry:
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {filename} - 토큰 만료 시간 로직 부재")
                        result['recommendations'].append("토큰 유효 시간 제한 (15분)")
        except: continue
    return result

def check_password_reset_exists(target_url):
    endpoints = ['/password/reset', '/password/forgot', '/user/reset', '/forgot-password', '/find-password']
    for endpoint in endpoints:
        try:
            if requests.get(f"{target_url}{endpoint}", timeout=5, allow_redirects=False).status_code == 200:
                return True
        except: continue
    return False

def test_password_reset_security(target_url):
    result = {'vulnerable': False, 'detail': ''}
    endpoints = ['/password/reset', '/password/forgot', '/find-password']
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{target_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                # 페이지 내에 토큰이나 코드 입력 필드가 없는 경우 취약으로 간주
                if 'token' not in response.text.lower() and 'code' not in response.text.lower():
                    result['vulnerable'] = True
                    result['detail'] = f"[Blackbox] 비밀번호 재설정 토큰 검증 미흡: {endpoint}"
                    return result
        except: pass
    return result

def test_security_questions(target_url):
    result = {'vulnerable': False, 'detail': ''}
    # 단순한 값으로 재설정 시도 (보안 질문 우회 시뮬레이션)
    weak_payload = {'username': 'admin', 'security_answer': 'admin'}
    endpoints = ['/password/reset', '/find-password']
    
    for endpoint in endpoints:
        try:
            res = requests.post(f"{target_url}{endpoint}", data=weak_payload, timeout=5)
            if res.status_code == 200 and ('success' in res.text.lower() or 'changed' in res.text.lower()):
                result['vulnerable'] = True
                result['detail'] = "[Blackbox] 예측 가능한 정보로 비밀번호 재설정 가능 (보안 질문 취약)"
                return result
        except: pass
    return result