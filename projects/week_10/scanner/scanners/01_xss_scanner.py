import requests
import os
import re

def scan(target_url, login_info=None):
    result = {
        'name': 'XSS (Cross-Site Scripting)',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # Thymeleaf 템플릿 정적 분석
        whitebox_result = scan_thymeleaf_xss()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        session = requests.Session()
        
        # 로그인 수행
        if login_info:
            login_url = f"{target_url}/login"
            session.post(login_url, data=login_info, timeout=5)
        
        # Stored XSS 점검
        stored_result = test_stored_xss(target_url, session)
        if stored_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(stored_result['detail'])
            result['recommendations'].append("입력값 HTML 이스케이프 처리 (th:text 사용)")
        
        # Reflected XSS 점검
        reflected_result = test_reflected_xss(target_url, session)
        if reflected_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(reflected_result['detail'])
            result['recommendations'].append("출력값 검증 및 이스케이프 처리")
        
        # DOM XSS 점검
        dom_result = test_dom_xss(target_url, session)
        if dom_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(dom_result['detail'])
            result['recommendations'].append("JavaScript 내 사용자 입력 안전 처리")
        
        # CSP 헤더 점검
        csp_result = check_csp_header(target_url)
        if csp_result['vulnerable']:
            result['details'].append(csp_result['detail'])
            result['recommendations'].append("CSP (Content-Security-Policy) 헤더 설정")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - XSS 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패 - 수동 확인 필요'
    
    return result

def scan_thymeleaf_xss():
    # Thymeleaf 템플릿 파일 내 취약한 태그(th:utext 등) 사용 여부 검사
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    
    html_files = set()
    search_paths = ['./templates', '../templates', './src/main/resources/templates']
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith('.html'):
                        html_files.add(os.path.abspath(os.path.join(root, file)))
    
    if not html_files:
        return result
    
    found_vulnerabilities = set()
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            filename = os.path.basename(html_file)
            
            for i, line in enumerate(lines, 1):
                if 'th:utext' in line:
                    vuln_key = f"{filename}:{i}:utext"
                    if vuln_key not in found_vulnerabilities:
                        found_vulnerabilities.add(vuln_key)
                        result['vulnerable'] = True
                        result['details'].append(f"[Static] {filename}:{i} - th:utext 사용")
                        if "th:utext를 th:text로 변경" not in result['recommendations']:
                            result['recommendations'].append("th:utext를 th:text로 변경")
                
                if re.search(r'\[\[\$\{[^}]+\}\]\]', line):
                    vuln_key = f"{filename}:{i}:inline"
                    if vuln_key not in found_vulnerabilities:
                        found_vulnerabilities.add(vuln_key)
                        result['vulnerable'] = True
                        result['details'].append(f"[Static] {filename}:{i} - 인라인 표현식 사용")
        except:
            continue
    
    return result

def test_stored_xss(target_url, session):
    # 게시판 글쓰기 POST 요청을 통한 Stored XSS 테스트
    result = {'vulnerable': False, 'detail': ''}
    
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
    ]
    
    write_endpoints = ['/board/write', '/support/ticket']
    
    for endpoint in write_endpoints:
        for payload in payloads:
            try:
                url = f"{target_url}{endpoint}"
                data = {'title': 'test', 'content': payload, 'subject': payload}
                response = session.post(url, data=data, timeout=5, allow_redirects=True)
                
                if payload in response.text and '<' in response.text:
                    result['vulnerable'] = True
                    result['detail'] = f"[Dynamic] Stored XSS 취약 ({endpoint})"
                    return result
            except:
                pass
    
    return result

def test_reflected_xss(target_url, session):
    # 검색 파라미터 GET 요청을 통한 Reflected XSS 테스트
    result = {'vulnerable': False, 'detail': ''}
    
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
    search_endpoints = ['/employee/search', '/board/list', '/board/search']
    
    for endpoint in search_endpoints:
        for payload in payloads:
            try:
                url = f"{target_url}{endpoint}"
                for param_name in ['q', 'search', 'keyword']:
                    params = {param_name: payload}
                    response = session.get(url, params=params, timeout=5)
                    
                    if payload in response.text and '<' in response.text:
                        result['vulnerable'] = True
                        result['detail'] = f"[Dynamic] Reflected XSS 취약 ({endpoint}, param: {param_name})"
                        return result
            except:
                pass
    
    return result

def test_dom_xss(target_url, session):
    # 클라이언트 사이드 스크립트 내 DOM 조작 패턴 확인
    result = {'vulnerable': False, 'detail': ''}
    
    test_urls = ['/board/list', '/employee/search']
    
    for test_url in test_urls:
        try:
            url = f"{target_url}{test_url}"
            response = session.get(url, timeout=5)
            
            if 'location.hash' in response.text and 'innerHTML' in response.text:
                result['vulnerable'] = True
                result['detail'] = f"[Dynamic] DOM-based XSS 가능성 ({test_url})"
                return result
        except:
            pass
    
    return result

def check_csp_header(target_url):
    # HTTP 응답 헤더 내 Content-Security-Policy 설정 여부 확인
    result = {'vulnerable': False, 'detail': ''}
    
    try:
        response = requests.get(target_url, timeout=5)
        if 'Content-Security-Policy' not in response.headers:
            result['vulnerable'] = True
            result['detail'] = "[Header] CSP 헤더 미설정"
    except:
        pass
    
    return result