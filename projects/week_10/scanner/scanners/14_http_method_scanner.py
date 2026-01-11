import requests
from urllib.parse import urlparse

def scan(target_url, crawl_result):
    result = {
        'name': '불필요한 HTTP Method 악용',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }

    # 스캔 대상 URL 선정 (Target URL + 크롤링된 URL 일부)
    urls = [target_url]
    if crawl_result and hasattr(crawl_result, "urls"):
        urls.extend(list(crawl_result.urls)[:5])

    # Path 기준 중복 제거 (효율성)
    unique_urls = []
    seen_paths = set()
    for u in urls:
        path = urlparse(u).path
        if path not in seen_paths:
            seen_paths.add(path)
            unique_urls.append(u)

    risky_methods = ["TRACE", "PUT", "DELETE", "PATCH", "OPTIONS"]
    sess = requests.Session()
    if crawl_result and hasattr(crawl_result, "cookies"):
        sess.cookies.update(crawl_result.cookies)

    try:
        for url in unique_urls:
            for method in risky_methods:
                try:
                    # 리다이렉트 방지(allow_redirects=False)가 중요
                    res = sess.request(method, url, timeout=5, allow_redirects=False)

                    # 1. TRACE/TRACK: XST(Cross-Site Tracing) 취약점 확인
                    if method == "TRACE" and res.status_code == 200:
                        result['vulnerable'] = True
                        result['details'].append(f"[Blackbox] TRACE 메서드 활성화됨 (XST 위험): {url}")

                    # 2. PUT/DELETE: 리소스 조작 가능성 확인
                    elif method in ["PUT", "DELETE", "PATCH"] and res.status_code in [200, 201, 202, 204]:
                        result['vulnerable'] = True
                        result['details'].append(f"[Blackbox] {method} 메서드 허용됨 (리소스 조작 위험): {url}")

                    # 3. OPTIONS: 허용된 메서드 정보 노출 확인
                    elif method == "OPTIONS" and "Allow" in res.headers:
                        allow_header = res.headers['Allow'].upper()
                        if any(m in allow_header for m in ["TRACE", "PUT", "DELETE"]):
                            result['details'].append(f"[Info] OPTIONS Allow 헤더 노출({allow_header}): {url}")

                except: continue

        if result['vulnerable']:
            result['recommendations'].append("웹 서버 설정에서 불필요한 HTTP Method 비활성화")
            result['recommendations'].append("필요한 메서드는 철저한 인증/인가 로직 적용")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 불필요한 HTTP Method가 차단되어 있음'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result