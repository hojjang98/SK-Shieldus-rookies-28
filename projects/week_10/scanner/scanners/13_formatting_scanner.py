import requests
import os
import json
import re

def scan(target_url, login_info=None):
    result = {
        'name': 'Format String 취약점',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] 소스 코드 내 String.format 오남용 검사
        whitebox_result = scan_format_string_code()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        session = requests.Session()
        if login_info:
            session.post(f"{target_url}/login", data=login_info, timeout=5)
        
        # [Blackbox] 포맷 스트링 인젝션 테스트
        format_result = test_format_string_injection(target_url, session)
        if format_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(format_result['detail'])
            result['recommendations'].append("사용자 입력을 포맷 문자열로 직접 사용 금지")
        
        # [Blackbox] 민감 정보 노출 테스트
        sensitive_result = test_sensitive_info_leak(target_url, session)
        if sensitive_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(sensitive_result['detail'])
            result['recommendations'].append("String.format()에서 민감 정보 제거")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - Format String 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_project_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('project_path', '.')
    return '.'

def scan_format_string_code():
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
                lines = content.split('\n')
                filename = os.path.basename(java_file)
                
                for i, line in enumerate(lines, 1):
                    # String.format의 첫 번째 인자에 변수 연결 확인
                    if 'String.format' in line and '+' in line:
                        if re.search(r'String\.format\s*\(\s*["\'][^"\']*["\'].*?\+', line):
                            # 사용자 입력 변수명 추정
                            if any(var in line.lower() for var in ['subject', 'content', 'input', 'name', 'data']):
                                result['vulnerable'] = True
                                result['details'].append(f"[Whitebox] {filename}:{i} - 포맷 문자열에 사용자 입력 연결")
                                result['recommendations'].append("String.format() 포맷 문자열 하드코딩 권장")
                    
                    # 민감 정보가 인자로 전달되는지 확인
                    if 'String.format' in line:
                        if any(k in line for k in ['secret', 'key', 'password', 'token', 'API']):
                            result['details'].append(f"[Whitebox] {filename}:{i} - String.format에 민감 정보 포함")
        except: continue
    return result

def test_format_string_injection(target_url, session):
    result = {'vulnerable': False, 'detail': ''}
    # %2$s: 두 번째 인자를 문자열로 출력 (정보 유출 유도)
    payloads = ['%s', '%2$s', '%1$s %2$s']
    test_url = f"{target_url}/support/ticket"
    
    for payload in payloads:
        try:
            response = session.post(test_url, data={'subject': payload}, timeout=5)
            if response.status_code == 200:
                # 1. 포맷 스트링이 동작하여 내부 값(메모리 등)이 노출되는지 확인
                if payload == '%2$s' and '%2$s' not in response.text:
                     # 정상적인 텍스트(Ticket Created 등) 외에 의심스러운 패턴 확인
                    if 'Ticket Created:' in response.text:
                         result['vulnerable'] = True
                         result['detail'] = f"[Blackbox] Format String 취약: {payload} 실행됨 (값 치환 발생)"
                         return result
                
                # 2. 포맷 에러 발생 확인
                if 'Exception' in response.text or 'Error' in response.text:
                    if '%' in response.text: # 에러 메시지에 포맷 관련 내용 포함 시
                        result['vulnerable'] = True
                        result['detail'] = f"[Blackbox] Format String 취약: {payload}로 인한 예외 발생"
                        return result
        except: pass
    return result

def test_sensitive_info_leak(target_url, session):
    result = {'vulnerable': False, 'detail': ''}
    try:
        # %2$s 페이로드를 통해 메모리 내 민감 정보(API Key 등) 추출 시도
        response = session.post(f"{target_url}/support/ticket", data={'subject': '%2$s'}, timeout=5)
        if response.status_code == 200:
            patterns = [
                r'SK-[A-Z0-9\-]+',       # API Key
                r'[A-Z]+-KEY-\d+',       # Generic Key
                r'secret[_\-]?\w+',      # Secret Variables
            ]
            for pattern in patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    result['vulnerable'] = True
                    result['detail'] = f"[Blackbox] Format String 민감 정보 유출: {match.group(0)}"
                    return result
    except: pass
    return result