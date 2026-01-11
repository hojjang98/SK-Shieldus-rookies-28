import requests
import os
import json
import re

def scan(target_url, login_info=None):
    result = {
        'name': 'SSRF (Server-Side Request Forgery)',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] URL 요청 및 커맨드 실행 코드 분석
        whitebox_url = scan_url_request_code()
        if whitebox_url['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_url['details'])
            result['recommendations'].extend(whitebox_url['recommendations'])

        whitebox_cmd = scan_command_injection()
        if whitebox_cmd['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_cmd['details'])
            result['recommendations'].extend(whitebox_cmd['recommendations'])
        
        session = requests.Session()
        if login_info:
            session.post(f"{target_url}/login", data=login_info, timeout=5)
        
        # [Blackbox] SSRF 및 OS Command Injection 공격 테스트
        ssrf_result = test_ssrf_vulnerability(target_url, session)
        if ssrf_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(ssrf_result['detail'])
            result['recommendations'].append("입력값 검증 및 명령어 인젝션 방어")
        
        # [Blackbox] 내부망(Loopback) 접근 테스트
        internal_result = test_internal_network_access(target_url, session)
        if internal_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(internal_result['detail'])
            result['recommendations'].append("내부 IP 대역 접근 차단")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - SSRF 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_project_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('project_path', '.')
    return '.'

def scan_command_injection():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    project_path = load_project_path()
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        filename = os.path.basename(file)
                        
                        for i, line in enumerate(lines, 1):
                            # Runtime.exec()에 사용자 입력이 연결되는지 확인
                            if ('Runtime.getRuntime().exec' in line or 'ProcessBuilder' in line) and ('+' in line or 'concat' in line):
                                if any(var in line.lower() for var in ['target', 'command', 'input', 'param']):
                                    result['vulnerable'] = True
                                    result['details'].append(f"[Whitebox] {filename}:{i} - Command Injection 위험 (exec에 입력값 연결)")
                                    result['recommendations'].append("Runtime.exec() 사용 금지 또는 화이트리스트 검증")
                except: continue
    return result

def scan_url_request_code():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    project_path = load_project_path()
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if any(x in content for x in ['new URL(', 'HttpClient', 'RestTemplate']):
                            # URL 요청 코드 주변에 검증 로직이 있는지 확인
                            if not any(v in content for v in ['whitelist', 'isValidUrl', 'allowedDomains']):
                                filename = os.path.basename(file)
                                result['vulnerable'] = True
                                result['details'].append(f"[Whitebox] {filename} - SSRF 위험 (URL 검증 로직 부재)")
                                result['recommendations'].append("URL 화이트리스트 검증 적용")
                except: continue
    return result

def test_ssrf_vulnerability(target_url, session):
    result = {'vulnerable': False, 'detail': ''}
    endpoints = [('/employee/partner-link', 'GET', 'url'), ('/admin/system/ping', 'POST', 'target')]
    internal_ip = '127.0.0.1'
    
    # OS Command Injection 결합 테스트 페이로드
    payloads = [
        f"{internal_ip}",
        f"{internal_ip} & dir", 
        f"{internal_ip}; ls", 
        f"{internal_ip} | id"
    ]
    
    for endpoint, method, param in endpoints:
        url = f"{target_url}{endpoint}"
        for payload in payloads:
            try:
                if method == 'POST':
                    res = session.post(url, data={param: payload}, timeout=5)
                else:
                    res = session.get(url, params={param: payload}, timeout=5)
                
                # Ping 결과나 시스템 명령어 실행 결과 확인
                if res.status_code == 200:
                    if any(k in res.text for k in ['TTL=', 'bytes=', 'uid=', 'Directory of']):
                        result['vulnerable'] = True
                        result['detail'] = f"[Blackbox] Command Injection/SSRF 취약: {endpoint} (payload: {payload})"
                        return result
            except: pass
    return result

def test_internal_network_access(target_url, session):
    result = {'vulnerable': False, 'detail': ''}
    try:
        # Ping 기능을 통한 Loopback 접근 테스트
        res = session.post(f"{target_url}/admin/system/ping", data={'target': '127.0.0.1'}, timeout=5)
        if res.status_code == 200 and ('TTL=' in res.text or 'Reply from' in res.text):
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 내부망(Loopback) 접근 가능: /admin/system/ping"
    except: pass
    return result