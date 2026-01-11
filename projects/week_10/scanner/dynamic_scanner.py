import requests
from crawler import WebCrawler
from urllib.parse import urlparse, parse_qs
import re

class DynamicScanner:
    """크롤링 데이터 기반 동적 취약점 스캐너"""
    
    def __init__(self, target_url, login_info=None):
        self.target_url = target_url
        self.login_info = login_info
        # 크롤러 초기화 및 세션 공유
        self.crawler = WebCrawler(target_url, login_info)
        self.session = self.crawler.session
        
        self.scan_stats = {
            'xss_tests': 0, 'sqli_tests': 0, 'csrf_checks': 0, 
            'url_sqli_tests': 0, 'auth_checks': 0
        }

    def scan_all(self):
        """전체 스캔 프로세스 실행"""
        # 1. 웹사이트 크롤링 수행
        crawl_results = self.crawler.start(max_pages=50)
        
        result = {
            'name': 'Dynamic Scan',
            'vulnerable': False,
            'details': [],
            'recommendations': []
        }
        
        # 2. 수집된 폼 대상 공격 시뮬레이션
        # XSS
        xss_vulns = self.scan_forms_for_xss(crawl_results.forms)
        if xss_vulns:
            result['vulnerable'] = True
            result['details'].extend(xss_vulns)
            result['recommendations'].append("Input HTML escaping (th:text)")
            
        # SQL Injection (Form)
        sqli_vulns = self.scan_forms_for_sqli(crawl_results.forms)
        if sqli_vulns:
            result['vulnerable'] = True
            result['details'].extend(sqli_vulns)
            result['recommendations'].append("Use PreparedStatement")
            
        # CSRF
        csrf_vulns = self.scan_forms_for_csrf(crawl_results.forms)
        if csrf_vulns:
            result['vulnerable'] = True
            result['details'].extend(csrf_vulns)
            result['recommendations'].append("Implement CSRF token")

        # 3. URL 파라미터 대상 공격 시뮬레이션
        # SQL Injection (URL)
        url_sqli_vulns = self.scan_urls_for_sqli(crawl_results.urls)
        if url_sqli_vulns:
            result['vulnerable'] = True
            result['details'].extend(url_sqli_vulns)
            result['recommendations'].append("URL parameter validation")
            
        # Authorization (Admin page access)
        auth_vulns = self.scan_for_authorization(crawl_results.urls)
        if auth_vulns:
            result['vulnerable'] = True
            result['details'].extend(auth_vulns)
            result['recommendations'].append("Access control enforcement")

        if result['recommendations']:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))
        else:
            result['recommendation'] = 'Safe - No dynamic vulnerabilities found'
            
        return result

    def scan_forms_for_xss(self, forms):
        vulnerabilities = []
        payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
        
        for form in forms:
            for payload in payloads:
                try:
                    self.scan_stats['xss_tests'] += 1
                    data = {inp.name: payload for inp in form.inputs if inp.type not in ['submit', 'hidden']}
                    if not data: continue
                    
                    if form.method == 'POST':
                        res = self.session.post(form.action, data=data, timeout=5)
                    else:
                        res = self.session.get(form.action, params=data, timeout=5)
                        
                    if payload in res.text and '<' in res.text:
                        vulnerabilities.append(f"[Dynamic] XSS found: {form.action}")
                        break
                except: continue
        return vulnerabilities

    def scan_forms_for_sqli(self, forms):
        vulnerabilities = []
        payloads = ["'", "' OR '1'='1"]
        
        for form in forms:
            for payload in payloads:
                try:
                    self.scan_stats['sqli_tests'] += 1
                    data = {inp.name: payload for inp in form.inputs if inp.type not in ['submit', 'hidden']}
                    if not data: continue
                    
                    if form.method == 'POST':
                        res = self.session.post(form.action, data=data, timeout=5)
                    else:
                        res = self.session.get(form.action, params=data, timeout=5)
                    
                    if any(k in res.text.lower() for k in ['sql', 'syntax', 'mysql', 'error']):
                        vulnerabilities.append(f"[Dynamic] SQL Injection found: {form.action}")
                        break
                except: continue
        return vulnerabilities

    def scan_forms_for_csrf(self, forms):
        vulnerabilities = []
        target_actions = ['write', 'edit', 'delete', 'update', 'password']
        
        for form in forms:
            self.scan_stats['csrf_checks'] += 1
            # POST 요청이면서 CSRF 토큰 필드가 없고, 중요한 기능을 수행하는 경우
            has_csrf_field = any('csrf' in (inp.name or '').lower() for inp in form.inputs)
            
            if form.method == 'POST' and not has_csrf_field:
                if any(k in form.action.lower() for k in target_actions):
                    vulnerabilities.append(f"[Dynamic] CSRF token missing: {form.action}")
        return vulnerabilities

    def scan_urls_for_sqli(self, urls):
        vulnerabilities = []
        payload = "'"
        
        for url in urls:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            if not params: continue
            
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            for k in params.keys():
                try:
                    self.scan_stats['url_sqli_tests'] += 1
                    test_params = params.copy()
                    test_params[k] = payload
                    # parse_qs 결과는 리스트이므로 첫 번째 값만 사용하도록 변환
                    clean_params = {pk: pv[0] if isinstance(pv, list) else pv for pk, pv in test_params.items()}
                    
                    res = self.session.get(base_url, params=clean_params, timeout=5)
                    if any(err in res.text.lower() for err in ['sql', 'syntax', 'mysql']):
                        vulnerabilities.append(f"[Dynamic] URL SQLi found: {base_url}?{k}=")
                        break
                except: continue
        return vulnerabilities

    def scan_for_authorization(self, urls):
        vulnerabilities = []
        admin_paths = ['/admin', '/manager', '/system']
        
        for url in urls:
            if any(path in url.lower() for path in admin_paths):
                try:
                    self.scan_stats['auth_checks'] += 1
                    # 새 세션(비로그인 상태)으로 접근 시도
                    anon_session = requests.Session()
                    res = anon_session.get(url, timeout=5, allow_redirects=False)
                    
                    if res.status_code == 200 and 'login' not in res.text.lower():
                        vulnerabilities.append(f"[Dynamic] Unauthorized Admin Access: {url}")
                except: continue
        return vulnerabilities