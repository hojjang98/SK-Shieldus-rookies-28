import requests
from urllib.parse import urljoin, urlparse

def scan(target_url, crawl_result=None):
    result = {
        'name': '에러 페이지 적용 미흡',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }

    # 스캔 대상 URL 목록 생성 (기본 URL + 크롤링된 URL 일부)
    base_candidates = [target_url]
    if crawl_result and hasattr(crawl_result, "urls"):
        base_candidates.extend(list(crawl_result.urls)[:10])

    # 존재하지 않을 법한 경로 테스트
    test_paths = ["/this_should_404_zzzz", "/%ZZ", "/error_test_1234"]
    common_ok_paths = {"/", "/login", "/signin", "/home", "/index", "/main"}

    sess = requests.Session()
    if crawl_result and hasattr(crawl_result, "cookies"):
        sess.cookies.update(crawl_result.cookies)

    try:
        for base in base_candidates:
            for p in test_paths:
                url = urljoin(base.rstrip("/") + "/", p.lstrip("/"))
                
                try:
                    r = sess.get(url, timeout=5, allow_redirects=True)
                    body_lower = (r.text or "").lower()
                    final_path = urlparse(r.url).path or "/"

                    # 1. Soft-404 탐지 (없는 페이지인데 200 OK 반환)
                    if r.status_code == 200:
                        # 단순히 메인 페이지 등으로 리다이렉트 된 경우 확인
                        if final_path.rstrip("/") in common_ok_paths:
                            result['vulnerable'] = True
                            result['details'].append(f"[Blackbox] 없는 경로가 메인/로그인 페이지로 리다이렉트됨 (Soft-404): {url}")
                        else:
                            result['vulnerable'] = True
                            result['details'].append(f"[Blackbox] 없는 경로 요청에 200 OK 응답 (Soft-404 의심): {url}")

                    # 2. 스택 트레이스 및 시스템 정보 노출 탐지
                    error_keywords = [
                        "exception", "stack trace", "whitelabel error page",
                        "traceback", "org.springframework", "apache tomcat",
                        "syntax error", "sql syntax"
                    ]
                    
                    if any(k in body_lower for k in error_keywords):
                        result['vulnerable'] = True
                        result['details'].append(f"[Blackbox] 에러 페이지 내 기술 정보/스택 트레이스 노출: {url}")

                    # 3. 상태 코드 불일치 (본문은 404인데 상태 코드는 정상)
                    if r.status_code < 400 and any(k in body_lower for k in ["not found", "page not found", "찾을 수 없습니다"]):
                        if r.status_code != 200: # Soft-404와 중복 방지
                            result['vulnerable'] = True
                            result['details'].append(f"[Blackbox] 상태 코드({r.status_code})와 에러 메시지 불일치")

                except requests.RequestException:
                    continue
                    
    except Exception as e:
        result['details'].append(f"오류: {str(e)}")

    if result['vulnerable']:
        result['recommendations'].append("존재하지 않는 페이지 요청 시 404 상태 코드 반환")
        result['recommendations'].append("운영 환경에서 스택 트레이스 및 상세 에러 메시지 노출 차단 (Custom Error Page 적용)")

    if not result['recommendations']:
        result['recommendation'] = '안전 - 에러 처리가 올바르게 구현되어 있음'
    else:
        result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    return result