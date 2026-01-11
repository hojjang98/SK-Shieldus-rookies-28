import requests
import os
import re
import xml.etree.ElementTree as ET

def scan(target_url):
    result = {
        'name': 'SQL Injection',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # MyBatis Mapper 정적 분석
        whitebox_result = scan_mybatis_mappers()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].append("MyBatis에서 ${} 대신 #{} 파라미터 사용")
        
        # 로그인 SQL Injection 테스트
        login_result = test_login_sqli(target_url)
        if login_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(login_result['detail'])
            result['recommendations'].append("PreparedStatement 사용 및 입력값 검증")
        
        # 검색 기능 SQL Injection 테스트
        search_result = test_search_sqli(target_url)
        if search_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(search_result['detail'])
            result['recommendations'].append("SQL 에러 메시지 숨김 처리")
        
        # URL 파라미터 SQL Injection 테스트
        param_result = test_param_sqli(target_url)
        if param_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(param_result['detail'])
            result['recommendations'].append("URL 파라미터 검증 강화")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - SQL Injection 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def scan_mybatis_mappers():
    # MyBatis Mapper XML 파일 내 취약한 바인딩(${}) 사용 여부 검사
    result = {'vulnerable': False, 'details': []}
    
    mapper_files = set()
    search_paths = ['.', '..', '../..']
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith('Mapper.xml'):
                        mapper_files.add(os.path.abspath(os.path.join(root, file)))
    
    if not mapper_files:
        return result
    
    found_vulnerabilities = set()
    
    for mapper_file in mapper_files:
        try:
            tree = ET.parse(mapper_file)
            root_elem = tree.getroot()
            filename = os.path.basename(mapper_file)
            
            for query_type in ['select', 'insert', 'update', 'delete']:
                for query in root_elem.findall(f'.//{query_type}'):
                    query_id = query.get('id', 'unknown')
                    query_text = ET.tostring(query, encoding='unicode', method='text')
                    
                    # ${} 패턴 찾기 (SQL Injection 취약점)
                    dollar_matches = re.findall(r'\$\{([^}]+)\}', query_text)
                    if dollar_matches:
                        result['vulnerable'] = True
                        for match in dollar_matches:
                            vuln_key = f"{filename}:{query_type}#{query_id}:${{{match}}}"
                            if vuln_key not in found_vulnerabilities:
                                found_vulnerabilities.add(vuln_key)
                                result['details'].append(
                                    f"[Static] {filename} - {query_type}#{query_id} - "
                                    f"SQL Injection 취약: ${{{match}}} (#{{{match}}} 사용 필요)"
                                )
        except:
            continue
    
    return result

def test_login_sqli(target_url):
    # 로그인 폼에 인증 우회 패턴 주입 테스트
    result = {'vulnerable': False, 'detail': ''}
    
    payloads = [
        {"username": "admin'#", "password": "anything"},
        {"username": "admin' OR '1'='1", "password": "anything"},
    ]
    
    login_url = f"{target_url}/login"
    
    for payload in payloads:
        try:
            session = requests.Session()
            response = session.post(login_url, data=payload, timeout=5, allow_redirects=True)
            
            success_indicators = ['logout', 'mypage', 'admin']
            
            if response.status_code == 200:
                if any(indicator in response.text.lower() for indicator in success_indicators):
                    result['vulnerable'] = True
                    result['detail'] = f"[Dynamic] 로그인 SQL Injection 취약 (payload: {payload['username']})"
                    return result
        except:
            pass
    
    return result

def test_search_sqli(target_url):
    # 검색어 입력란에 에러 유발 및 구문 조작 패턴 주입 테스트
    result = {'vulnerable': False, 'detail': ''}
    
    payloads = ["' OR '1'='1", "'; DROP TABLE--"]
    search_endpoints = ['/employee/search', '/board/list']
    
    for endpoint in search_endpoints:
        for payload in payloads:
            try:
                url = f"{target_url}{endpoint}"
                for param_name in ['q', 'keyword']:
                    params = {param_name: payload}
                    response = requests.get(url, params=params, timeout=5)
                    
                    error_keywords = ['sql', 'syntax', 'mysql', 'error']
                    
                    if any(keyword in response.text.lower() for keyword in error_keywords):
                        result['vulnerable'] = True
                        result['detail'] = f"[Dynamic] 검색 SQL Injection 취약 ({endpoint}, param: {param_name})"
                        return result
            except:
                pass
    
    return result

def test_param_sqli(target_url):
    # URL 파라미터(GET)에 SQL 구문 주입 테스트
    result = {'vulnerable': False, 'detail': ''}
    
    payloads = ["'", "1' OR '1'='1"]
    test_urls = ['/board/view?id=', '/user/profile?id=']
    
    for test_url in test_urls:
        for payload in payloads:
            try:
                url = f"{target_url}{test_url}{payload}"
                response = requests.get(url, timeout=5)
                
                error_keywords = ['sql', 'syntax', 'error']
                
                if any(keyword in response.text.lower() for keyword in error_keywords):
                    result['vulnerable'] = True
                    result['detail'] = f"[Dynamic] URL 파라미터 SQL Injection 취약 ({test_url})"
                    return result
            except:
                pass
    
    return result