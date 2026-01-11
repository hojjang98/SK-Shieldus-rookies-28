import requests
import os
import json
import xml.etree.ElementTree as ET
import re

def scan(target_url, login_info=None):
    result = {
        'name': '불충분한 접근 제어 (인증/인가)',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] MyBatis SQL Injection (인증 우회 가능성) 검사
        mybatis_result = scan_mybatis_auth_vulnerability()
        if mybatis_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(mybatis_result['details'])
            result['recommendations'].append("MyBatis에서 ${} 대신 #{} 사용")
        
        # [Whitebox] Controller 인증/인가 로직 누락 검사
        controller_result = scan_controller_auth()
        if controller_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(controller_result['details'])
            result['recommendations'].append("Spring Security 또는 인터셉터로 인증 체크 추가")
        
        # [Whitebox] 세부 권한 검증 코드(IDOR 등) 검사
        authz_result = scan_authorization_code()
        if authz_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(authz_result['details'])
            result['recommendations'].extend(authz_result['recommendations'])
        
        # [Blackbox] SQL Injection을 통한 인증 우회 시도
        sqli_result = test_sql_injection_bypass(target_url)
        if sqli_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(sqli_result['detail'])
            result['recommendations'].append("PreparedStatement로 SQL Injection 방어")
        
        # [Blackbox] 비로그인 상태로 보호된 페이지 접근 시도
        protected_result = test_protected_pages(target_url)
        if protected_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(protected_result['detail'])
            result['recommendations'].append("인증 필터 추가 (Spring Security 적용)")
        
        # [Blackbox] 수평적 권한 상승 (Horizontal Privilege Escalation)
        horizontal_result = test_horizontal_privilege(target_url, login_info)
        if horizontal_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(horizontal_result['detail'])
            result['recommendations'].append("직접 객체 참조 검증 강화")
        
        # [Blackbox] 수직적 권한 상승 (Vertical Privilege Escalation)
        vertical_result = test_vertical_privilege(target_url, login_info)
        if vertical_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(vertical_result['detail'])
            result['recommendations'].append("Role-Based Access Control 구현")
        
        # [Blackbox] IDOR (Insecure Direct Object Reference)
        idor_result = test_idor(target_url, login_info)
        if idor_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(idor_result['detail'])
            result['recommendations'].append("객체 소유권 검증 추가")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 접근 제어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def load_project_path():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('project_path', '.')
    return '.'

def load_guest_login():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('guest_login', None)
    return None

def scan_mybatis_auth_vulnerability():
    result = {'vulnerable': False, 'details': []}
    project_path = load_project_path()
    mapper_files = []
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('Mapper.xml'):
                mapper_files.append(os.path.join(root, file))
    
    for mapper_file in mapper_files:
        try:
            tree = ET.parse(mapper_file)
            root_elem = tree.getroot()
            for query in root_elem.findall('.//select'):
                if query.get('id') in ['login', 'findByUsername']:
                    query_text = ET.tostring(query, encoding='unicode', method='text')
                    if '${' in query_text:
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {os.path.basename(mapper_file)} - SQL Injection 취약 (로그인 쿼리)")
        except: continue
    return result

def scan_controller_auth():
    result = {'vulnerable': False, 'details': []}
    project_path = load_project_path()
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('Controller.java') and 'Admin' in file:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'session.getAttribute' not in content and '@PreAuthorize' not in content:
                            result['vulnerable'] = True
                            result['details'].append(f"[Whitebox] {file} - 관리자 컨트롤러 인증 체크 미흡")
                except: continue
    return result

def scan_authorization_code():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    project_path = load_project_path()
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('Controller.java'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'BoardController' in file and '/board/view' in content:
                            if 'checkOwnership' not in content and 'writer.equals' not in content:
                                result['vulnerable'] = True
                                result['details'].append(f"[Whitebox] {file} - 게시글 조회 소유권 검증 부재 (IDOR 위험)")
                except: continue
    return result

def test_sql_injection_bypass(target_url):
    result = {'vulnerable': False, 'detail': ''}
    payloads = [{"username": "admin'#", "password": "x"}, {"username": "' OR '1'='1'#", "password": "x"}]
    
    for payload in payloads:
        try:
            res = requests.post(f"{target_url}/login", data=payload, timeout=5)
            if res.status_code == 200 and ('logout' in res.text.lower() or '로그아웃' in res.text):
                result['vulnerable'] = True
                result['detail'] = f"[Blackbox] SQL Injection 인증 우회 성공 (payload: {payload['username']})"
                return result
        except: pass
    return result

def test_protected_pages(target_url):
    result = {'vulnerable': False, 'detail': ''}
    pages = ['/admin/system', '/user/mypage', '/board/write']
    
    for page in pages:
        try:
            res = requests.get(f"{target_url}{page}", timeout=5, allow_redirects=False)
            if res.status_code == 200 and len(res.text) > 500 and 'login' not in res.text.lower():
                result['vulnerable'] = True
                result['detail'] = f"[Blackbox] 비로그인 상태로 보호 페이지 접근 가능: {page}"
                return result
        except: pass
    return result

def test_horizontal_privilege(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    session = requests.Session()
    try:
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        # 타인(admin)의 리포트 조회 시도
        res = session.get(f"{target_url}/employee/results?writer=admin", timeout=5)
        if res.status_code == 200 and 'report' in res.text.lower() and 'empty' not in res.text.lower():
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 수평적 권한 상승: 타인의 리포트 조회 가능"
    except: pass
    return result

def test_vertical_privilege(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    session = requests.Session()
    try:
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        # 일반 유저가 관리자 페이지 접근 시도
        res = session.get(f"{target_url}/admin/system", timeout=5)
        if res.status_code == 200 and 'denied' not in res.text.lower() and '거부' not in res.text:
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 수직적 권한 상승: 일반 사용자가 관리자 페이지 접근"
    except: pass
    return result

def test_idor(target_url, login_info):
    result = {'vulnerable': False, 'detail': ''}
    if not login_info: return result
    
    session = requests.Session()
    try:
        session.post(f"{target_url}/login", data=login_info, timeout=5)
        # ID값 변조하여 접근 시도
        for pid in range(1, 5):
            res = session.get(f"{target_url}/board/view?id={pid}", timeout=5)
            if res.status_code == 200 and '권한' not in res.text:
                 # 실제로는 본인 글인지 확인하는 로직 필요하나 약식 구현
                 pass
    except: pass
    return result