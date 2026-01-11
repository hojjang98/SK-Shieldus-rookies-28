import requests
import os

def scan(target_url):
    result = {
        'name': '경로 조작 (Path Traversal)',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }
    
    try:
        # [Whitebox] 소스 코드 내 파일 경로 처리 로직 검증
        whitebox_result = scan_file_path_handling()
        if whitebox_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].extend(whitebox_result['details'])
            result['recommendations'].extend(whitebox_result['recommendations'])
        
        # [Blackbox] 파일 다운로드 경로 조작 테스트
        download_result = test_path_traversal_download(target_url)
        if download_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(download_result['detail'])
            result['recommendations'].append("파일 경로 정규화 및 검증")
        
        # [Blackbox] 파일 읽기 경로 조작 테스트
        read_result = test_path_traversal_read(target_url)
        if read_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(read_result['detail'])
            result['recommendations'].append("화이트리스트 기반 경로 제한")
        
        # [Blackbox] 상위 디렉토리 접근 테스트
        archive_result = test_archive_traversal(target_url)
        if archive_result['vulnerable']:
            result['vulnerable'] = True
            result['details'].append(archive_result['detail'])
            result['recommendations'].append("업로드 디렉토리 외부 접근 차단")
        
        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = '안전 - 경로 조작 방어가 올바르게 구현되어 있음'
        
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'
    
    return result

def scan_file_path_handling():
    result = {'vulnerable': False, 'details': [], 'recommendations': []}
    
    java_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    
    for java_file in java_files:
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 파일 처리 관련 로직이 있는지 확인
                if 'download' in content.lower() or 'file' in content.lower():
                    filename = os.path.basename(java_file)
                    
                    # 경로 정규화(normalize) 메서드 사용 여부 확인
                    has_normalize = any(pattern in content for pattern in ['normalize()', 'getCanonicalPath()'])
                    if not has_normalize:
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {filename} - 경로 정규화 로직 부재")
                        result['recommendations'].append("경로 정규화 구현 (normalize)")
                    
                    # 상위 경로(..) 포함 여부 검증 확인
                    has_validation = any(pattern in content for pattern in ['startsWith(', 'contains("..")'])
                    if not has_validation:
                        result['vulnerable'] = True
                        result['details'].append(f"[Whitebox] {filename} - 경로 검증 로직 부재")
                        result['recommendations'].append("경로 검증 추가 (.. 패턴 차단)")
        except: continue
    
    return result

def test_path_traversal_download(target_url):
    result = {'vulnerable': False, 'detail': ''}
    payloads = ['../../../etc/passwd', '../../application.properties']
    endpoints = ['/file/download', '/libs/download', '/board/download']
    
    for endpoint in endpoints:
        for payload in payloads:
            try:
                url = f"{target_url}{endpoint}"
                params = {'file': payload, 'filename': payload}
                response = requests.get(url, params=params, timeout=5)
                
                # 시스템 파일 내용 유출 확인
                sensitive_keywords = ['root:', 'password', 'jdbc']
                if any(keyword in response.text for keyword in sensitive_keywords):
                    result['vulnerable'] = True
                    result['detail'] = f"[Blackbox] 시스템 파일 접근 가능 ({endpoint})"
                    return result
            except: pass
    return result

def test_path_traversal_read(target_url):
    result = {'vulnerable': False, 'detail': ''}
    payloads = ['../../../config/database.yml', '../../application.properties']
    endpoints = ['/file/view', '/read']
    
    for endpoint in endpoints:
        for payload in payloads:
            try:
                url = f"{target_url}{endpoint}"
                params = {'path': payload, 'file': payload}
                response = requests.get(url, params=params, timeout=5)
                
                # 설정 파일 내용 유출 확인
                if any(k in response.text.lower() for k in ['password', 'jdbc', 'database']):
                    result['vulnerable'] = True
                    result['detail'] = f"[Blackbox] 설정 파일 노출 확인 ({endpoint})"
                    return result
            except: pass
    return result

def test_archive_traversal(target_url):
    result = {'vulnerable': False, 'detail': ''}
    try:
        url = f"{target_url}/libs/archive"
        params = {'path': '../../../'}
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200 and ('etc' in response.text or 'config' in response.text):
            result['vulnerable'] = True
            result['detail'] = "[Blackbox] 상위 디렉토리 리스팅 가능"
    except: pass
    return result