import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class CrawledInput:
    """스캐너 호환성을 위한 입력 필드 객체"""
    def __init__(self, tag):
        self.tag = tag.name
        self.type = tag.get('type', 'text')
        self.name = tag.get('name')
        self.value = tag.get('value', '')
        self.id = tag.get('id')

class CrawledForm:
    """스캐너 호환성을 위한 폼 객체"""
    def __init__(self, action, method, inputs):
        self.action = action
        self.method = method
        self.inputs = inputs

class WebCrawler:
    def __init__(self, target_url, login_info=None):
        self.target_url = target_url
        self.login_info = login_info
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'SecurityScanner/1.0'})
        
        # 결과 저장소
        self.visited = set()
        self.urls = set()
        self.forms = []
        self.cookies = {}

    def start(self, max_pages=100):
        # 1. 로그인 시도
        if self.login_info:
            try:
                self.session.get(urljoin(self.target_url, '/login'), timeout=5)
                self.session.post(urljoin(self.target_url, '/login'), data=self.login_info, timeout=5)
                self.cookies = self.session.cookies.get_dict()
            except: pass

        # 2. 방문 큐 초기화 (기본 URL + 주요 엔드포인트)
        queue = [self.target_url]
        common_paths = [
            '/board/list', '/board/write', '/employee/search', '/support/ticket',
            '/user/mypage', '/admin/system', '/libs/archive', '/join'
        ]
        for path in common_paths:
            queue.append(urljoin(self.target_url, path))

        # 3. BFS 크롤링
        while queue and len(self.visited) < max_pages:
            url = queue.pop(0)
            
            if url in self.visited or not self._is_target_domain(url):
                continue
            
            self.visited.add(url)
            self.urls.add(url)
            
            try:
                res = self.session.get(url, timeout=3)
                if res.status_code == 200 and 'text/html' in res.headers.get('Content-Type', ''):
                    self._parse_page(url, res.text, queue)
            except: continue
        
        return self # 결과 객체 반환

    def _is_target_domain(self, url):
        try:
            return urlparse(self.target_url).netloc == urlparse(url).netloc
        except: return False

    def _parse_page(self, base_url, html, queue):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 링크 추출
            for a in soup.find_all('a', href=True):
                full_url = urljoin(base_url, a['href']).split('#')[0]
                if self._is_valid_link(full_url):
                    queue.append(full_url)

            # 폼 추출 (다른 스캐너에서 사용)
            for form in soup.find_all('form'):
                action = urljoin(base_url, form.get('action', ''))
                method = form.get('method', 'get').upper()
                inputs = [CrawledInput(tag) for tag in form.find_all(['input', 'textarea', 'select'])]
                self.forms.append(CrawledForm(action, method, inputs))
        except: pass

    def _is_valid_link(self, url):
        skip_ext = ['.css', '.js', '.png', '.jpg', '.gif', '.pdf', '.zip']
        if any(url.lower().endswith(ext) for ext in skip_ext): return False
        if any(p in url for p in ['javascript:', 'mailto:', 'tel:']): return False
        return True